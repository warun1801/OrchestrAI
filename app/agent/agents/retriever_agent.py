from langchain_openai import ChatOpenAI

class RetrieverAgent:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def retrieve(self, query, repo_url, top_k=5):
        # embed query & perform semantic search
        docs = self.vectorstore.similarity_search(query, top_k=top_k, filter={"repo": repo_url})
        return "\n".join([d.page_content for d in docs])
