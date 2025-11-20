from app.services.vectorstore import retrieve_embeddings

class RetrieverAgent:
    """
    Retriever Agent for OrchestrAI.
    Responsible for fetching relevant code/context from the vectorstore.
    """

    def __init__(self, top_k: int = 5):
        """
        Args:
            top_k: Number of top relevant documents to retrieve
        """
        self.top_k = top_k

    def retrieve(self, query: str, repo_url: str) -> str:
        """
        Retrieves the top_k relevant code chunks for a query.

        Args:
            query: User query or subtask description
            repo_url: Repository identifier for filtering

        Returns:
            A single concatenated string of the retrieved code chunks
        """
        results = retrieve_embeddings(query=query, repo_url=repo_url, top_k=self.top_k)

        # Combine retrieved document content into a single string for LLM input
        context = "\n".join([doc.page_content for doc in results])
        return context
