from transformers import pipeline
from tools import incident_search

# import warnings
# warnings.filterwarnings("ignore")

# from transformers.utils import logging
# logging.set_verbosity_error()

print("Loading FLAN-T5 model...")

llm = pipeline(
    task="text-generation",
    model="google/flan-t5-base",
    max_new_tokens=256,
    temperature=0.01,
    do_sample=True,
)

print("Model loaded.\n")


def run_agent(query):

    prompt = f"""
You are ResilienceBot.

You can use this tool:
incident_search(query) → searches past system incidents.

User Question: {query}

If the question is about incidents respond with:
TOOL: incident_search(query)

Otherwise answer directly.
"""

    response = llm(prompt)[0]["generated_text"]

    if "TOOL:" in response:

        tool_result = incident_search.invoke({"query": query})

        final_prompt = f"""
User Question: {query}

Incident Data:
{tool_result}

"""

        final_answer = llm(final_prompt)[0]["generated_text"]

        return final_answer

    return response
