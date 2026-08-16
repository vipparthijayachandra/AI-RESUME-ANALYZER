"""Input validation helpers."""

from pathlib import Path

from app.utils.constants import ALLOWED_RESUME_EXTENSIONS, MAX_UPLOAD_SIZE_BYTES


def is_supported_resume(filename: str) -> bool:
    """Return whether a filename has a supported resume extension."""
    return Path(filename).suffix.lower().lstrip(".") in ALLOWED_RESUME_EXTENSIONS


def validate_resume_upload(filename: str, size_bytes: int) -> None:
    """Validate upload metadata before attempting PDF extraction.

    The PDF parser performs the final content validation because filenames and
    browser-provided MIME types alone cannot prove a file is a readable PDF.
    """
    if not filename or not is_supported_resume(filename):
        raise ValueError("Please upload a resume in PDF format.")
    if size_bytes <= 0:
        raise ValueError("The uploaded PDF is empty.")
    if size_bytes > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError("The uploaded PDF exceeds the 10 MB size limit.")
