from langchain_openai import ChatOpenAI
import json

class WorkerAgent:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def run(self, state):
        for attempt in range(2):  # retry loop
            prompt = f"""
You are a software engineer. Given this PLAN and CONTEXT, produce a JSON array of tasks.

PLAN:
{state.plan}

CONTEXT:
{state.context}

Output MUST be valid JSON.
"""
            res = self.llm.invoke(prompt)
            try:
                tasks = json.loads(res.content)
                state.tasks = tasks
                return state
            except json.JSONDecodeError:
                print("[WORKER] Invalid JSON, retrying...")
                continue
        raise ValueError("Worker Agent failed to produce valid JSON")
