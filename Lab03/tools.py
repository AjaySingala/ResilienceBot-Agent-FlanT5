from langchain_core.tools import tool
from rag_index import load_vector_store
import sqlite3
from log_tool import log_search

vectorstore = load_vector_store()

DB_PATH = "database/incidents.db"


@tool
def incident_search(query: str) -> str:
    """Search past incidents using semantic similarity"""

    docs = vectorstore.similarity_search(query, k=3)

    if not docs:
        return "No incidents found."

    formatted = []

    for d in docs:
        text = d.page_content

        lines = text.split("\n")

        incident = lines[0].replace("Incident:", "").strip()
        root_cause = ""
        impact = ""

        for l in lines:
            if "Root Cause:" in l:
                root_cause = l.replace("Root Cause:", "").strip()
            if "Impact:" in l:
                impact = l.replace("Impact:", "").strip()

        formatted.append(
            f"Incident: {incident}. Root cause: {root_cause}. Impact: {impact}."
        )

    return "\n".join(formatted)

@tool
def sql_query(query: str) -> str:
    """Execute SQL queries on incident database"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
                return "No results found."

        formatted = []

        for r in rows:
            formatted.append(
                f"Service: {r[0]}, Date: {r[1]}, Root Cause: {r[2]}"
            )

        return "\n".join(formatted)
    except Exception as e:
        return f"SQL Error: {e}"

    finally:
        conn.close()
