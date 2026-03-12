from dotenv import load_dotenv
import os

load_dotenv()
#print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from tools import finance_agent, marketing_agent, tech_agent

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# list of agents (tools)
tools = [finance_agent, marketing_agent, tech_agent]

# create agent
agent = create_react_agent(llm, tools)
