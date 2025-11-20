import json
import git
from pathlib import Path
from openai import OpenAI
from app.utils.chunk import chunk_text
from app.utils.file_hash import hash_file_content
from app.services.vectorstore import vectorstore

client = OpenAI()


def load_index(path: Path):
    index_file = path / ".index.json"
    if not index_file.exists():
        return {"commit": None, "files": {}}
    return json.loads(index_file.read_text())


def save_index(path: Path, index: dict):
    (path / ".index.json").write_text(json.dumps(index, indent=2))


def ingest_repo(repo_url: str) -> str:
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    local_path = Path(f"./repos/{repo_name}")

    # Clone or pull repo
    if not local_path.exists():
        print(f"[INGEST] Cloning repo {repo_url}")
        git.Repo.clone_from(repo_url, local_path)
    else:
        print(f"[INGEST] Pulling latest changes...")
        repo = git.Repo(local_path)
        repo.remotes.origin.pull()

    repo = git.Repo(local_path)
    latest_commit = repo.head.commit.hexsha

    # Load previous index
    index = load_index(local_path)
    prev_commit = index.get("commit")
    prev_files = index.get("files", {})

    # If commit unchanged => fully skip ingestion
    if prev_commit == latest_commit:
        print("[CACHE] Repo unchanged. Skipping ingestion.")
        return str(local_path)

    print(f"[INGEST] Commit changed. Running incremental ingestion...")

    # --- STEP 1: SCAN FILESYSTEM ---
    current_files = {}
    modified_files = []
    deleted_files = []
    new_files = []

    for file in local_path.rglob("*.*"):
        if file.suffix not in {".py", ".java", ".js", ".ts", ".go", ".md"}:
            continue

        text = file.read_text(errors="ignore")
        file_hash = hash_file_content(text)
        rel = str(file.relative_to(local_path))

        current_files[rel] = file_hash

        if rel not in prev_files:
            new_files.append((rel, text))
        elif prev_files[rel] != file_hash:
            modified_files.append((rel, text))

    # Detect deleted files
    for old_file in prev_files:
        if old_file not in current_files:
            deleted_files.append(old_file)

    print(f"[INGEST] New files: {len(new_files)}")
    print(f"[INGEST] Modified files: {len(modified_files)}")
    print(f"[INGEST] Deleted files: {len(deleted_files)}")

    # --- STEP 2: HANDLE DELETIONS ---
    for rel in deleted_files:
        vectorstore.delete(where={"file": rel, "repo": repo_url})

    # --- STEP 3: ADD / UPDATE FILES ---
    files_to_embed = new_files + modified_files

    for rel, text in files_to_embed:
        chunks = chunk_text(text)
        embeddings = client.embeddings.create(
            model="text-embedding-3-large",
            input=chunks
        ).data

        for emb, chunk in zip(embeddings, chunks):
            vectorstore.add(
                embeddings=[emb.embedding],
                documents=[chunk],
                metadatas=[{
                    "file": rel,
                    "repo": repo_url
                }],
                ids=[f"{repo_url}-{rel}-{hash(chunk)}"]
            )

    # --- STEP 4: UPDATE INDEX ---
    save_index(local_path, {
        "commit": latest_commit,
        "files": current_files
    })

    print(f"[INGEST] Incremental ingestion complete.")

    return str(local_path)
