"""Streamlit entry point for ResumeIQ."""

from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.dashboard.components import render_page_header
from app.dashboard.results_view import render_ats_score, render_empty_results, render_profile_summary
from app.dashboard.upload_view import render_resume_uploader
from app.data.database import initialize_database
from app.services.ats_scorer import calculate_score


def main() -> None:
    """Configure and render the ResumeIQ application shell."""
    st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")
    initialize_database()

    render_page_header()
    profile = render_resume_uploader()
    if profile is None:
        render_empty_results()
    else:
        render_profile_summary(profile)
        render_ats_score(calculate_score(profile))


if __name__ == "__main__":
    main()
