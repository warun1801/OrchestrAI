import hashlib

def hash_file_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
