from langchain_core.tools import tool
from rag_index import load_vector_store

vectorstore = load_vector_store()

@tool
def incident_search(query: str) -> str:
    """
    Search past incidents, outages, and root causes from the incident knowledge base.
    """

    docs = vectorstore.similarity_search(query, k=3)

    results = "\n".join([doc.page_content for doc in docs])

    return results
