from langchain_core.tools import tool

@tool
def finance_agent(query: str) -> str:
    """Handles finance related questions"""
    print(f"\nTOOL: Finance agent received query: {query}")
    return f"Finance analysis: {query}"

@tool
def marketing_agent(query: str) -> str:
    """Handles marketing related questions"""
    print(f"\nTOOL: Marketing agent received query: {query}")

    return f"Marketing analysis: {query}"

@tool
def tech_agent(query: str) -> str:
    """Handles technical troubleshooting questions"""
    print(f"\nTOOL: Tech agent received query: {query}")
    return f"Technical troubleshooting steps for: {query}"
