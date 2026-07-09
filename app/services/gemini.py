"""Gemini multimodal + embedding wrapper. TODO: implement."""
def caption_image(image_bytes: bytes) -> str: raise NotImplementedError
def embed_text(text: str) -> list[float]: raise NotImplementedError
def answer(question: str, context: list[str], image_bytes: bytes | None = None) -> str: raise NotImplementedError
