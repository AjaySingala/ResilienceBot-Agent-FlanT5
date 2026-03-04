from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tools import incident_search, sql_query, log_search

# -----------------------------
# Load FLAN-T5
# -----------------------------
print("Loading FLAN-T5 model...")
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Model loaded.")

# Safe tool call with retries and error handling.
def safe_tool_call(tool_func, tool_name, args, retries=2):
    for attempt in range(retries):
        try:
            result = tool_func.invoke(args)
            if result and str(result).strip():
                return result
        except Exception as e:
            print(f"{tool_name} failed (attempt {attempt+1}):", e)

    print(f"{tool_name} failed after retries")
    return None

# -----------------------------
# LLM Generation Helper
# -----------------------------
def llm_generate(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# -----------------------------
# SQL Query Generator
# -----------------------------
def generate_sql(question):
    q = question.lower()

    if "sla" in q or "breach" in q:
        return """
        SELECT service, date, root_cause
        FROM incidents
        WHERE sla_breach = 1
        """

    if "payment" in q:
        return """
        SELECT service, date, root_cause
        FROM incidents
        WHERE service = 'payment'
        """

    if "login" in q:
        return """
        SELECT service, date, root_cause
        FROM incidents
        WHERE service = 'login'
        """

    return "SELECT service, date, root_cause FROM incidents"

# -----------------------------
# Agent Planning
# -----------------------------
def plan_steps(question):
    q = question.lower()

    # multi-system investigation
    if "after" in q or "correlate" in q or "relationship" in q:
        return ["sql", "log", "rag"]

    # SLA + log correlation
    if "sla" in q and "log" in q:
        return ["sql", "log"]

    # log analysis
    if "error" in q or "spike" in q or "logs" in q:
        return ["log"]

    # SQL queries
    if "sla" in q or "which service" in q:
        return ["sql"]

    # default
    return ["rag"]

# -----------------------------
# Final Answer Generation
# -----------------------------
def final_answer(question, evidence):

    prompt = f"""
You are a site reliability engineer analyzing incidents.

Use the evidence to explain the system behavior.

Question:
{question}

Evidence:
{evidence}

Write a detailed explanation using 2–3 sentences.
Do NOT answer with only "Yes" or "No".
Explain what happened using the evidence.

Explanation:
"""

    return llm_generate(prompt)

# -----------------------------
# Main Agent Execution
# -----------------------------
def run_agent(query):
    steps = plan_steps(query)
    print("Agent Plan →", " → ".join(steps).upper())

    sql_data = ""
    log_data = ""
    rag_data = ""

    for step in steps:
        if step == "sql":
            sql = generate_sql(query)
            print("Running SQL step")

            # result = sql_query.invoke({"query": sql})
            # sql_data = result
            sql_data = safe_tool_call(
                sql_query,
                "SQL Tool",
                {"query": sql}
            )
        elif step == "log":
            print("Analyzing logs")

            # result = log_search.invoke({"query": query})
            # log_data = result
            log_data = safe_tool_call(
                log_search,
                "Log Search Tool",
                {"query": query}
            )
        elif step == "rag":
            print("Searching incident knowledge base")
            
            # result = incident_search.invoke({"query": query})
            # rag_data = result
            rag_data = safe_tool_call(
                incident_search,
                "RAG Tool",
                {"query": query}
            )
    # Structured evidence for reasoning
    evidence = ""

    if sql_data:
        evidence += f"\nINCIDENT RECORDS:\n{sql_data}\n"

    if log_data:
        evidence += f"\nLOG ANALYSIS:\n{log_data}\n"

    if rag_data:
        evidence += f"\nINCIDENT DESCRIPTION:\n{rag_data}\n"

    if not evidence.strip():
        return "The system tools did not return sufficient data to answer the question."

    return final_answer(query, evidence)
