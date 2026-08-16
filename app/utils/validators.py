"""Input validation helpers."""

from pathlib import Path

from app.utils.constants import ALLOWED_RESUME_EXTENSIONS


def is_supported_resume(filename: str) -> bool:
    """Return whether a filename has a supported resume extension."""
    return Path(filename).suffix.lower().lstrip(".") in ALLOWED_RESUME_EXTENSIONS
