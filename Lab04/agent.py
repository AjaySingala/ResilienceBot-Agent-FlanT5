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
# Add a planning step to the agent.
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
    # Plan the steps based on the query.
    steps = plan_steps(query)
    print("Agent Plan →", " → ".join(steps).upper())

    sql_data = ""
    log_data = ""
    rag_data = ""

    # Execute the planned steps and collect evidence.
    for step in steps:
        if step == "sql":
            sql = generate_sql(query)
            print("Running SQL step")
            result = sql_query.invoke({"query": sql})
            sql_data = result
        elif step == "log":
            print("Analyzing logs")
            result = log_search.invoke({"query": query})
            log_data = result
        elif step == "rag":
            print("Searching incident knowledge base")
            result = incident_search.invoke({"query": query})
            rag_data = result

    # Structured evidence for reasoning
    evidence = f"""
INCIDENT RECORDS (SQL):
{sql_data}

LOG ANALYSIS:
{log_data}

INCIDENT DESCRIPTION (RAG):
{rag_data}
"""

    return final_answer(query, evidence)
