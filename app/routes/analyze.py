from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.graph_multi_agent import workflow

router = APIRouter(prefix="/api")

class AnalyzeRequest(BaseModel):
    repo_url: str
    query: str

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    """
    Calls the LangGraph agent pipeline.
    """
    result = workflow.invoke({
        "repo_url": req.repo_url,
        "query": req.query
    })

    return result
