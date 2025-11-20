from app.services.vectorstore import vectorstore
from openai import OpenAI
from app.config import EMBED_MODEL

client = OpenAI()

def search_vectors(query: str, k=3):
    emb = client.embeddings.create(
        model=EMBED_MODEL,
        input=query
    ).data[0].embedding

    results = vectorstore.query(
        query_embeddings=[emb],
        n_results=k
    )

    return results["documents"][0] if results["documents"] else []
