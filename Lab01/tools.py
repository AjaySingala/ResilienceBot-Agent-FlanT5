from langchain_core.tools import tool
from rag_index import load_vector_store

# Load the Vector Database.
# This loads the existing Chroma DB stored on disk.
vectorstore = load_vector_store()

# Define the Tool.
@tool
def incident_search(query: str) -> str:
    # Tool Description.
    """
    Search past incidents, outages, and root causes from the incident knowledge base.
    """

    # Perform Similarity Search.
    docs = vectorstore.similarity_search(query, k=3)

    # Combine Results into Text.
    results = "\n".join([doc.page_content for doc in docs])

    return results
