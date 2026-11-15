"""Gemini multimodal reasoning and embedding service.

Isolates the Google Gemini SDK (`google-genai`) behind deterministic,
testable functions. When `GEMINI_API_KEY` is not set or equals a placeholder,
functions fall back to a deterministic offline policy so unit and integration
tests never make live network calls unless explicitly configured.
"""
from __future__ import annotations

import hashlib
import math
import os
import re

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_EMBEDDING_MODEL = "text-embedding-004"
DEFAULT_EMBEDDING_DIM = 8

_PDF_PAGE_PATTERN = re.compile(rb"/Type\s*/Page\b(?![sS])")


def split_visual_chunks(payload: bytes, mime_type: str = "image/png") -> list[bytes]:
    """Split a visual payload into per-page byte chunks (pure helper).

    For PDF payloads (`application/pdf` or `%PDF-` header) containing multiple
    `/Type /Page` objects, returns one deterministic byte slice per page so each
    page is captioned, embedded, and indexed independently. Single-page PDFs and
    raster/SVG images return `[payload]`.
    """
    if not payload:
        raise ValueError("payload must not be empty")

    is_pdf = mime_type == "application/pdf" or payload.startswith(b"%PDF-")
    if not is_pdf:
        return [payload]

    matches = list(_PDF_PAGE_PATTERN.finditer(payload))
    if len(matches) <= 1:
        return [payload]

    chunks: list[bytes] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(payload)
        chunks.append(b"%PDF-page-" + str(idx + 1).encode("ascii") + b":" + payload[start:end])
    return chunks


def _get_live_api_key() -> str | None:
    """Return a live API key if configured, or None when running in offline/mock mode."""
    if os.environ.get("GEMINI_MOCK", "").lower() in {"1", "true", "yes"}:
        return None
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key or key in {"your-gemini-key", "test-key", "mock"}:
        return None
    return key


def _deterministic_vector(text: str, dim: int = DEFAULT_EMBEDDING_DIM) -> list[float]:
    """Build a deterministic unit-normalized vector from text for offline execution."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    raw = [((digest[i % len(digest)] / 255.0) * 2.0 - 1.0) for i in range(dim)]
    norm = math.sqrt(sum(v * v for v in raw)) or 1.0
    return [round(v / norm, 6) for v in raw]


def caption_image(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """Extract a textual caption and structured data summary from visual document bytes."""
    if not image_bytes:
        raise ValueError("image_bytes must not be empty")

    api_key = _get_live_api_key()
    if api_key is None:
        digest = hashlib.sha256(image_bytes).hexdigest()[:8]
        return f"Visual document summary (hash={digest}, bytes={len(image_bytes)})"

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    model_name = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    response = client.models.generate_content(
        model=model_name,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            (
                "Describe this visual document accurately. Extract all chart titles, "
                "axes, labels, series values, and key relationships as concise text."
            ),
        ],
    )
    return (response.text or "").strip()


def embed_text(text: str, dim: int = DEFAULT_EMBEDDING_DIM) -> list[float]:
    """Embed text into a float vector of length `dim`."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("text must not be empty")

    api_key = _get_live_api_key()
    if api_key is None:
        return _deterministic_vector(cleaned, dim=dim)

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    embed_model = os.environ.get("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    result = client.models.embed_content(
        model=embed_model,
        contents=cleaned,
        config=types.EmbedContentConfig(output_dimensionality=dim),
    )
    embeddings = result.embeddings
    if not embeddings or not embeddings[0].values:
        raise RuntimeError("Gemini embedding response returned no vector values")
    return list(embeddings[0].values)


def answer(
    question: str,
    context: list[str],
    image_bytes: bytes | None = None,
    mime_type: str = "image/png",
) -> str:
    """Generate a grounded answer from retrieved context and optional visual input."""
    cleaned_question = question.strip()
    if not cleaned_question:
        raise ValueError("question must not be empty")

    api_key = _get_live_api_key()
    if api_key is None:
        ctx_summary = " | ".join(context) if context else "no retrieved context"
        img_tag = f" [with image: {len(image_bytes)} bytes]" if image_bytes else ""
        return f"Grounded answer to '{cleaned_question}'{img_tag} using: {ctx_summary}"

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    model_name = os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    context_block = "\n".join(f"- {chunk}" for chunk in context) if context else "None provided."
    prompt = (
        "Answer the user's question using only the retrieved context and attached image "
        "(if present). Do not invent facts outside the provided evidence.\n\n"
        f"Retrieved context:\n{context_block}\n\n"
        f"Question: {cleaned_question}"
    )
    contents: list[object] = []
    if image_bytes:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
    contents.append(prompt)

    response = client.models.generate_content(model=model_name, contents=contents)
    return (response.text or "").strip()
