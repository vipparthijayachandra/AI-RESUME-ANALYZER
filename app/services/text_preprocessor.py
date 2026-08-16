"""Text-normalization interface for the future NLP pipeline."""


def normalize_text(text: str) -> str:
    """Apply safe whitespace normalization before later NLP processing."""
    return " ".join(text.split())
