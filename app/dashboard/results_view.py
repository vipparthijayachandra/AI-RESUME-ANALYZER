"""Results view placeholder for later analysis phases."""

import streamlit as st


def render_empty_results() -> None:
    """Describe the results that later phases will populate."""
    st.subheader("Analysis results")
    st.write("Your ATS score, recommended roles, and skill gaps will appear here.")
