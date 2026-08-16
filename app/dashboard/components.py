"""Reusable Streamlit interface components."""

import streamlit as st


def render_page_header() -> None:
    """Render the application title and current development status."""
    st.title("ResumeIQ")
    st.caption("AI-powered resume insights for students")
    st.info("Foundation setup is complete. Resume analysis features will be added in upcoming phases.")
