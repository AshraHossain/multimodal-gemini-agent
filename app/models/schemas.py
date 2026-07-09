"""Pydantic request/response schemas."""
from pydantic import BaseModel
from typing import Optional

class IngestResponse(BaseModel):
    doc_id: str
    chunks: int

class AskRequest(BaseModel):
    question: str
    image_b64: Optional[str] = None
    top_k: int = 4

class AskResponse(BaseModel):
    answer: str
    sources: list[str] = []
