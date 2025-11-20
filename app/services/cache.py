import json
from pathlib import Path

CACHE_FILE = Path("./repos/cache_metadata.json")

def load_cache():
    if not CACHE_FILE.exists():
        return {}
    return json.loads(CACHE_FILE.read_text())

def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def get_repo_cache(repo_url):
    cache = load_cache()
    return cache.get(repo_url, None)

def update_repo_cache(repo_url, data):
    cache = load_cache()
    cache[repo_url] = data
    save_cache(cache)
