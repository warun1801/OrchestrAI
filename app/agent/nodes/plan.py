def plan(state, llm):
    prompt = f"""
You are a senior software architect.

Create a multi-step plan to address the following query:

Query: {state.query}

Return a concise, structured plan.
    """
    res = llm.invoke(prompt)
    state.plan = res.content
    return state
