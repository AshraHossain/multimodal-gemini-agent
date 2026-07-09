from fastapi import FastAPI
from app.routers import ingest, ask

app = FastAPI(title="Multimodal Gemini Agent")
app.include_router(ingest.router)
app.include_router(ask.router)

@app.get("/health")
def health():
    return {"status": "ok"}
