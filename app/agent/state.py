from pydantic import BaseModel
from typing import List, Optional

class AgentState(BaseModel):
    repo_url: str
    query: str

    repo_path: Optional[str] = ""
    context: Optional[str] = ""
    plan: Optional[str] = ""
    tasks: List[dict] = []
