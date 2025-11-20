import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4.1"  # can switch later
EMBED_MODEL = "text-embedding-3-large"
CHROMA_PATH = "./chroma_db"
