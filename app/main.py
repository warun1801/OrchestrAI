from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="Agentic Codebase Analyzer",
    version="1.0.0"
)

app.include_router(analyze_router)

@app.get("/")
def root():
    return {"message": "Agentic backend is running"}
