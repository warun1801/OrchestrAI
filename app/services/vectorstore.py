from pathlib import Path
from langchain_chroma import Chroma
from langchain_openai.embeddings.base import OpenAIEmbeddings
from app.config import OPENAI_API_KEY, EMBED_MODEL
from typing import List, Dict

# ===========================
# Configuration
# ===========================
PERSIST_DIR = Path("./chroma_db")
COLLECTION_NAME = "repo_docs"

embeddings = OpenAIEmbeddings(model=EMBED_MODEL, openai_api_key=OPENAI_API_KEY)


# Initialize Chroma vectorstore (with persistence if directory exists)
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIR) if PERSIST_DIR.exists() else None
)

# ===========================
# Helper Functions
# ===========================
def add_embeddings(chunks: List[str], metadatas: List[Dict], ids: List[str]):
    """
    Add embeddings to the vectorstore.

    Args:
        chunks: list of text chunks to embed
        metadatas: list of dict metadata for each chunk (e.g., {"repo": repo_url, "file": file_path})
        ids: list of unique IDs for each chunk
    """
    vectorstore.add(
        documents=chunks,
        embeddings=[embeddings.embed_text(c) for c in chunks],
        metadatas=metadatas,
        ids=ids
    )

def delete_embeddings(where: Dict):
    """
    Delete embeddings based on metadata filter.

    Args:
        where: dictionary with metadata key-value pairs for deletion
               e.g., {"repo": repo_url, "file": file_path}
    """
    vectorstore.delete(where=where)

def retrieve_embeddings(query: str, repo_url: str = None, top_k: int = 5):
    """
    Retrieve top_k relevant embeddings.

    Args:
        query: the query string for semantic search
        repo_url: optional repo filter
        top_k: number of results to return

    Returns:
        List of LangChain Document objects
    """
    filter_metadata = {"repo": repo_url} if repo_url else None
    results = vectorstore.similarity_search(
        query=query,
        k=top_k,
        filter=filter_metadata
    )
    return results

def persist():
    """
    Persist the vectorstore to disk (if using persist_directory).
    """
    if PERSIST_DIR.exists():
        vectorstore.persist()
