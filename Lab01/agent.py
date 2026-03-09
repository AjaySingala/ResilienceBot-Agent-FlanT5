# From the Hugging Face Transformers library.
from transformers import pipeline
# Import the Tool.
from tools import incident_search

# import warnings
# warnings.filterwarnings("ignore")

# from transformers.utils import logging
# logging.set_verbosity_error()

print("Loading FLAN-T5 model...")

# Create the LLM.
llm = pipeline(
    task="text-generation",
    model="google/flan-t5-base",
    max_new_tokens=256,
    temperature=0.01,
    do_sample=True,     # Allows sampling during generation.
)

print("Model loaded.\n")

# Main Agent Function.
# Simple AI agent loop.
def run_agent(query):
    # Build the Agent Prompt.
    prompt = f"""
You are ResilienceBot.

You can use this tool:
incident_search(query) → searches past system incidents.

User Question: {query}

If the question is about incidents respond with:
TOOL: incident_search(query)

Otherwise answer directly.
"""

    # Generate the Model Response.
    response = llm(prompt)[0]["generated_text"]

    # Check If Tool Should Be Used.
    if "TOOL:" in response:
        # Execute the Tool.
        tool_result = incident_search.invoke({"query": query})

        # Build the Final Prompt.
        final_prompt = f"""
User Question: {query}

Incident Data:
{tool_result}

"""
        # Generate Final Answer.
        final_answer = llm(final_prompt)[0]["generated_text"]

        return final_answer

    return response
