from app.agent.tools.search_vectors import search_vectors

def retrieve(state):
    docs = search_vectors(state.query, k=5)
    state.context = "\n\n".join([d for d in docs])
    return state
