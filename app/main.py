"""Streamlit entry point for ResumeIQ."""

from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.dashboard.components import render_page_header
from app.dashboard.results_view import render_empty_results
from app.dashboard.upload_view import render_upload_placeholder
from app.data.database import initialize_database


def main() -> None:
    """Configure and render the Phase 1 application shell."""
    st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")
    initialize_database()

    render_page_header()
    render_upload_placeholder()
    render_empty_results()


if __name__ == "__main__":
    main()
