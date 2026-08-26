"""Streamlit view for safe PDF resume ingestion."""

import streamlit as st

from app.services.pdf_processor import extract_text
from app.services.resume_parser import parse_resume
from app.services.text_preprocessor import normalize_text
from app.models.schemas import ResumeProfile
from app.utils.validators import validate_resume_upload


def render_resume_uploader() -> ResumeProfile | None:
    """Upload, validate, extract, and preview a PDF resume.

    Returns the extracted profile, or ``None`` when there is no valid uploaded
    document.
    """
    with st.container(border=True):
        st.subheader("Upload resume")
        st.caption("Upload a text-based PDF resume up to 10 MB.")
        uploaded_file = st.file_uploader(
            "Choose a PDF resume",
            type=["pdf"],
            help="Only PDF resumes can be analyzed.",
        )

    if uploaded_file is None:
        st.info("Choose a PDF resume to begin the analysis.")
        return None

    try:
        validate_resume_upload(uploaded_file.name, uploaded_file.size)
        extracted_text = extract_text(uploaded_file)
        normalized_text = normalize_text(extracted_text)
        profile = parse_resume(normalized_text)
    except ValueError as error:
        st.error(str(error))
        return None

    st.success(f"Resume processed successfully: {uploaded_file.name}")
    st.caption("The extracted text is shown below, followed by your analysis results.")
    with st.expander("Preview extracted resume text", expanded=True):
        st.text_area(
            "Extracted text",
            value=extracted_text,
            height=320,
            disabled=True,
            label_visibility="collapsed",
        )

    return profile
