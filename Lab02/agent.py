from tools import incident_search, sql_query

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

print("Loading FLAN-T5 model...")

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Model loaded.")

def llm_generate(prompt):

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=120,
        temperature=0.1,
        do_sample=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def choose_tool(question):

    q = question.lower()

    # SQL type queries
    if "sla" in q or "which services" in q or "how many" in q or "incidents" in q:
        return "sql"

    # RAG type queries
    if "cause" in q or "why" in q or "explain" in q or "outage" in q:
        return "rag"

    return "rag"

def run_agent(query):

    tool = choose_tool(query)
    print("Agent Decision →", tool.upper())

    if tool == "sql":

        sql = generate_sql(query)
        print("Executing SQL query:", sql)

        result = sql_query.invoke({"query": sql})
        return final_answer(query, result)

    else:

        print("Using RAG search")

        result = incident_search.invoke({"query": query})
        return final_answer(query, result)
    
def generate_sql(question):

    q = question.lower()

    # SLA queries
    if "sla" in q or "violated" in q:
        return """
        SELECT service, date, root_cause
        FROM incidents
        WHERE sla_breach = 1
        """

    # payment incidents
    if "payment" in q:
        return """
        SELECT service, date, root_cause
        FROM incidents
        WHERE service = 'payment'
        """

    # checkout incidents
    if "checkout" in q:
        return """
        SELECT service, date, root_cause
        FROM incidents
        WHERE service = 'checkout'
        """

    # default
    return "SELECT * FROM incidents LIMIT 5"

def final_answer(question, data):

    prompt = f"""
You are a reliability engineering assistant.

Use the incident information below to answer the question clearly.

Question:
{question}

Incident Information:
{data}

Write a short explanation of the incident.
"""

    response = llm_generate(prompt)

    return response.strip()
