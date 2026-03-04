import os
from agent import run_agent
from rag_index import build_vector_store

# Set env vars from config.py.
import sys
import os

# Add the folder path (use absolute or relative path)
folder_path = os.path.join(os.path.dirname(__file__), '../')
sys.path.insert(0, folder_path)

import config

print("ResilienceBot Ready")

# Start.
# Build vector DB if it doesn't exist
# if not os.path.exists("chroma_db"):
#     print("Building vector database...")
#     build_vector_store()

# Build vector DB every time for demo purposes. 
# In production, you would typically build it once and then load it (above commented code).
print("Building vector database...")
build_vector_store()

while True:

    query = input("\nAsk ('exit' to Stop): ")

    if query.lower() == "exit":
        break

    answer = run_agent(query)

    print("\nResilienceBot:\n", answer)
