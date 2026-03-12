from agent import agent

query = "How can we improve customer retention in digital marketing?"

response = agent.invoke({
    "messages": [("user", query)]
})

print(response["messages"][-1].content)
