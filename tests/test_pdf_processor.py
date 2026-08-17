"""Tests for Phase 3 PDF ingestion services."""

from io import BytesIO

import fitz
import pytest

from app.services.pdf_processor import extract_text
from app.services.text_preprocessor import normalize_text
from app.utils.constants import MAX_UPLOAD_SIZE_BYTES
from app.utils.validators import is_supported_resume, validate_resume_upload


def _make_pdf_with_text(text: str) -> BytesIO:
    """Create an in-memory PDF fixture containing readable text."""
    with fitz.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), text)
        return BytesIO(document.tobytes())


def test_extract_text_returns_text_from_a_valid_pdf() -> None:
    """A text-based PDF produces readable content."""
    pdf_file = _make_pdf_with_text("Python developer")

    assert "Python developer" in extract_text(pdf_file)


def test_extract_text_rejects_empty_pdf_upload() -> None:
    """Empty uploads receive a clear validation error."""
    with pytest.raises(ValueError, match="empty"):
        extract_text(BytesIO())


def test_extract_text_rejects_corrupted_pdf() -> None:
    """Unreadable bytes cannot be treated as a PDF."""
    with pytest.raises(ValueError, match="could not be read"):
        extract_text(BytesIO(b"not a PDF"))


def test_extract_text_rejects_pdf_without_readable_text() -> None:
    """A valid but textless PDF cannot yet be analyzed."""
    with fitz.open() as document:
        document.new_page()
        empty_pdf = BytesIO(document.tobytes())

    with pytest.raises(ValueError, match="No readable text"):
        extract_text(empty_pdf)


def test_validate_resume_upload_accepts_pdf_metadata() -> None:
    """A reasonably sized PDF filename is accepted for extraction."""
    validate_resume_upload("student_resume.PDF", 1024)


@pytest.mark.parametrize("filename", ["resume.docx", "resume.txt", "resume"])
def test_validate_resume_upload_rejects_non_pdf_filenames(filename: str) -> None:
    """Only PDF filenames pass metadata validation."""
    with pytest.raises(ValueError, match="PDF format"):
        validate_resume_upload(filename, 1024)


def test_validate_resume_upload_rejects_empty_or_oversized_files() -> None:
    """Empty and oversized uploads are rejected before parsing."""
    with pytest.raises(ValueError, match="empty"):
        validate_resume_upload("resume.pdf", 0)
    with pytest.raises(ValueError, match="size limit"):
        validate_resume_upload("resume.pdf", MAX_UPLOAD_SIZE_BYTES + 1)


def test_preprocessing_normalizes_extracted_text() -> None:
    """Normalized text is ready for the later profile extraction phase."""
    assert normalize_text("  Python\n\n  SQL  ") == "Python\nSQL"
    assert is_supported_resume("resume.pdf")
