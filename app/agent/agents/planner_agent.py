from langchain_openai import ChatOpenAI
from app.agent.agents.retriever_agent import RetrieverAgent

class PlannerAgent:
    def __init__(self, llm: ChatOpenAI, retriever: RetrieverAgent):
        self.llm = llm
        self.retriever = retriever

    def run(self, state):
        # Step 1: retrieve context if empty
        if not state.context:
            state.context = self.retriever.retrieve(state.query, state.repo_url)

        # Step 2: generate plan
        prompt = f"""
You are a senior software architect. Break down the following query into a detailed, actionable plan.

Query: {state.query}

Context: {state.context}

Output an ordered list of sub-tasks.
"""
        res = self.llm.invoke(prompt)
        state.plan = res.content
        return state
