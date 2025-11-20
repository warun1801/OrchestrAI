from app.services.ingest import ingest_repo

def ingest(state):
    """
    LangGraph node responsible for ensuring the repo is cloned
    and indexed into the vector database.

    It saves the local repo path into state.repo_path.
    """
    print(f"[INGEST] Starting ingestion for: {state.repo_url}")

    repo_path = ingest_repo(state.repo_url)
    state.repo_path = repo_path

    print(f"[INGEST] Completed ingestion. Local path: {repo_path}")

    return state
