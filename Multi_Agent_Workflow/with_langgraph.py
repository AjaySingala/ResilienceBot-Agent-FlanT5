# LangGraph-style (no if-else)
from langgraph import Graph

graph = Graph()
graph.add_node("supervisor", supervisor_agent)
graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)
graph.add_conditional_edges("supervisor", lambda state: state["next"])  # LLM decides

graph.add_edge(START, "supervisor")  		# Entry point
graph.add_edge("researcher", "supervisor")  # Loop back
graph.add_edge("writer", END)  				# Exit

app = graph.compile()  # Executable workflow

result = app.invoke({"input": "your query"})  # Runs with state

# ===
# Simple Breakdown of "add_conditional_edges":
# ---
# graph.add_conditional_edges("supervisor", lambda state: state["next"])

# Think of it like a magic traffic light:
# - Supervisor agent runs first (it's an LLM that thinks "should I send this to researcher or writer?").
# - Supervisor writes its decision in the shared notebook: state["next"] = "researcher" (or "writer").
# - This line reads that decision and automatically routes to whatever the supervisor chose.
