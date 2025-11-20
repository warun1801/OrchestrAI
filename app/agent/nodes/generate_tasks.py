def generate_tasks(state, llm):
    prompt = f"""
You are a senior engineer.

Context:
{state.context}

Plan:
{state.plan}

Generate a JSON array of tasks with:
- title
- description
- related_files
- acceptance_criteria
    """

    res = llm.invoke(prompt)
    state.tasks = res.content  # will parse later
    return state
