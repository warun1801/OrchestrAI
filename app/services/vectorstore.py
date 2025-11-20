import chromadb
from chromadb.config import Settings
from app.config import CHROMA_PATH

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=CHROMA_PATH
))

vectorstore = client.get_or_create_collection(
    name="codebase",
    metadata={"hnsw:space": "cosine"}
)
