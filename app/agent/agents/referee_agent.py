from langchain_openai import ChatOpenAI
import json

class RefereeAgent:
    def __init__(self, llm: ChatOpenAI, worker_agent):
        self.llm = llm
        self.worker_agent = worker_agent

    def run(self, state):
        prompt = f"""
You are an expert reviewer. Examine this task output and ensure it matches the PLAN and CONTEXT.

PLAN:
{state.plan}

CONTEXT:
{state.context}

TASKS:
{state.tasks}

If issues are found, instruct the Worker Agent to revise.
Output only the corrected JSON array of tasks.
"""
        res = self.llm.invoke(prompt)
        try:
            state.tasks = json.loads(res.content)
        except json.JSONDecodeError:
            # fallback to worker agent revision
            print("[REFEREE] Invalid JSON, asking Worker to revise...")
            state = self.worker_agent.run(state)
        return state
