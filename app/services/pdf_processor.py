"""PDF text extraction utilities built on PyMuPDF."""

from typing import BinaryIO

import fitz


def extract_text(pdf_file: BinaryIO) -> str:
    """Return text from every page in an uploaded PDF file.

    Raises:
        ValueError: If the file is empty, unreadable, or has no extractable text.
    """
    content = pdf_file.read()
    if not content:
        raise ValueError("The uploaded PDF is empty.")

    try:
        with fitz.open(stream=content, filetype="pdf") as document:
            text = "\n".join(page.get_text("text") for page in document)
    except (fitz.FileDataError, RuntimeError) as error:
        raise ValueError("The uploaded file could not be read as a PDF.") from error

    if not text.strip():
        raise ValueError("No readable text was found in the PDF.")
    return text
