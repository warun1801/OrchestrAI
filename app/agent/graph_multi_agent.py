from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from app.agent.state import AgentState
from app.services.vectorstore import vectorstore
from app.agent.nodes.ingest import ingest
from app.agent.agents.retriever_agent import RetrieverAgent
from app.agent.agents.planner_agent import PlannerAgent
from app.agent.agents.worker_agent import WorkerAgent
from app.agent.agents.referee_agent import RefereeAgent

llm = ChatOpenAI(model="gpt-4.1")
retriever = RetrieverAgent(vectorstore)
planner = PlannerAgent(llm, retriever)
worker = WorkerAgent(llm)
referee = RefereeAgent(llm, worker)

graph = StateGraph(AgentState)

graph.add_node("ingest", ingest)
graph.add_node("planner_agent", lambda s: planner.run(s))
graph.add_node("worker_agent", lambda s: worker.run(s))
graph.add_node("referee_agent", lambda s: referee.run(s))

graph.set_entry_point("ingest")
graph.add_edge("ingest", "planner_agent")
graph.add_edge("planner_agent", "worker_agent")
graph.add_edge("worker_agent", "referee_agent")
graph.add_edge("referee_agent", END)

workflow = graph.compile()
