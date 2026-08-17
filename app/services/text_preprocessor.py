"""Text-normalization interface for the future NLP pipeline."""

import re


def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving line boundaries for section parsing."""
    normalized_lines = (re.sub(r"[\t ]+", " ", line).strip() for line in text.splitlines())
    return "\n".join(line for line in normalized_lines if line)
