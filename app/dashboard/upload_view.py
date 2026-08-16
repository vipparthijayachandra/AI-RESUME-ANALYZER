"""Streamlit view for safe PDF resume ingestion."""

import streamlit as st

from app.services.pdf_processor import extract_text
from app.services.text_preprocessor import normalize_text
from app.utils.validators import validate_resume_upload


def render_resume_uploader() -> str | None:
    """Upload, validate, extract, and preview a PDF resume.

    Returns the normalized text for later analysis phases, or ``None`` when
    there is no valid uploaded document.
    """
    st.subheader("Upload resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF resume",
        type=["pdf"],
        help="Upload a text-based PDF resume up to 10 MB.",
    )

    if uploaded_file is None:
        st.caption("Only PDF resumes up to 10 MB are accepted.")
        return None

    try:
        validate_resume_upload(uploaded_file.name, uploaded_file.size)
        extracted_text = extract_text(uploaded_file)
        normalized_text = normalize_text(extracted_text)
    except ValueError as error:
        st.error(str(error))
        return None

    st.success(f"Extracted readable text from {uploaded_file.name}.")
    st.caption("The text has been normalized and is ready for profile extraction in Phase 4.")
    with st.expander("Preview extracted resume text", expanded=True):
        st.text_area(
            "Extracted text",
            value=extracted_text,
            height=320,
            disabled=True,
            label_visibility="collapsed",
        )

    return normalized_text
