"""Pydantic request/response schemas (frozen/immutable DTOs)."""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class IngestRequest(BaseModel):
    """JSON payload alternative for ingesting a base64-encoded document."""

    model_config = ConfigDict(frozen=True)

    image_b64: str = Field(..., min_length=1, description="Base64-encoded image or PDF page bytes")
    source_id: str | None = Field(default=None, description="Optional caller-supplied document ID")
    mime_type: str = Field(default="image/png", description="MIME type of the visual asset")


class IngestResponse(BaseModel):
    """Response returned after captioning, embedding, and storing a visual asset."""

    model_config = ConfigDict(frozen=True)

    doc_id: str = Field(..., min_length=1)
    chunks: int = Field(..., ge=1)


class AskRequest(BaseModel):
    """Multimodal question request grounded against retrieved Atlas context."""

    model_config = ConfigDict(frozen=True)

    question: str = Field(..., min_length=1)
    image_b64: str | None = None
    top_k: int = Field(default=4, ge=1, le=50)


class AskResponse(BaseModel):
    """Grounded answer with source document references."""

    model_config = ConfigDict(frozen=True)

    answer: str
    sources: list[str] = Field(default_factory=list)
