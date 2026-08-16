"""Resume upload view placeholder for the ingestion phase."""

import streamlit as st


def render_upload_placeholder() -> None:
    """Reserve the upload area without starting resume ingestion."""
    st.subheader("Upload resume")
    st.caption("PDF upload and validation will be available in Phase 3.")
