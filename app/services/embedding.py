"""Embedding helpers.

``to_vector`` calls Gemini (needs an API key in live mode) and is implemented in
the gemini service. The ranking helpers below are pure math used to order
retrieved candidates locally; they have no external dependency and are unit-tested.
"""
from __future__ import annotations

import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must be the same length")
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def rank_by_similarity(query: list[float], candidates: list[dict], k: int = 4) -> list[dict]:
    """Return the top-k candidates (each having an 'embedding') by cosine sim.

    Each returned dict gets a 'score' field. Useful as a local fallback when not
    delegating ranking to Atlas $vectorSearch.
    """
    scored = []
    for c in candidates:
        score = cosine_similarity(query, c["embedding"])
        scored.append({**c, "score": score})
    scored.sort(key=lambda c: c["score"], reverse=True)
    return scored[:k]


def to_vector(text: str) -> list[float]:
    """Delegate to the Gemini embedding service."""
    from app.services.gemini import embed_text

    return embed_text(text)
