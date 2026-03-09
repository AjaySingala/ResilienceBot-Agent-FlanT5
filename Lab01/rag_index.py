# Imports.
from langchain_chroma import Chroma
# Converts text into numerical vectors (embeddings) using a HuggingFace model.
from langchain_huggingface import HuggingFaceEmbeddings
# Split large documents into smaller chunks.
# Split by Paragraphs, then Sentences, then Words, and then Characters.
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Represents text as Document objects.
from langchain_core.documents import Document

# Creates the vector database from scratch.
def build_vector_store():

    with open("data/incidents.txt", "r") as f:
        text = f.read()

    # Split the text into chunks.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )

    # Split text.
    docs = splitter.split_text(text)

    # Convert to LangChain Documents.
    documents = [Document(page_content=d) for d in docs]

    # Create embedding model.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create vector database.
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    print("Vector database built with", len(documents), "documents")

# Loads the existing vector database instead of rebuilding it.
def load_vector_store():
    # Load embedding model again.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load the database.
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    return vectorstore
