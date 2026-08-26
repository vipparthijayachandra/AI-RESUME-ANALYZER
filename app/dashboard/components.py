"""Reusable Streamlit interface components."""

import streamlit as st


def render_page_header() -> None:
    """Render the ResumeIQ dashboard header."""
    st.title("ResumeIQ")
    st.caption("Resume analysis for student placement preparation")
    st.info("Upload a PDF resume to review your profile, ATS-style score, and role-skill alignment.")
