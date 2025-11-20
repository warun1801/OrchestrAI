from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from app.agent.state import AgentState
from app.agent.nodes.ingest import ingest
from app.agent.nodes.retrieve import retrieve
from app.agent.nodes.plan import plan
from app.agent.nodes.generate_tasks import generate_tasks

llm = ChatOpenAI(model="gpt-4.1")

graph = StateGraph(AgentState)

graph.add_node("ingest", ingest)
graph.add_node("retrieve", retrieve)
graph.add_node("plan", lambda state: plan(state, llm))
graph.add_node("generate_tasks", lambda state: generate_tasks(state, llm))

graph.set_entry_point("ingest")
graph.add_edge('ingest', "retrieve")
graph.add_edge("retrieve", "plan")
graph.add_edge("plan", "generate_tasks")
graph.add_edge("generate_tasks", END)

workflow = graph.compile()
