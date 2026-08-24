"""Views for extracted resume-profile information."""

import streamlit as st

from app.models.schemas import ATSScoreResult, ResumeProfile


def _render_profile_items(title: str, items: list[str]) -> None:
    """Render a profile field without implying information was found."""
    st.markdown(f"#### {title}")
    if items:
        st.markdown("\n".join(f"- {item}" for item in items))
    else:
        st.caption(f"No {title.lower()} detected.")


def render_profile_summary(profile: ResumeProfile) -> None:
    """Display the deterministic profile extracted from an uploaded resume."""
    st.subheader("Extracted resume profile")
    st.caption("These fields are detected directly from the uploaded resume.")
    left_column, right_column = st.columns(2)

    with left_column:
        _render_profile_items("Skills", profile.skills)
        _render_profile_items("Education", profile.education)
        _render_profile_items("Projects", profile.projects)

    with right_column:
        _render_profile_items("Work experience", profile.experience)
        _render_profile_items("Certifications", profile.certifications)


def render_ats_score(score_result: ATSScoreResult) -> None:
    """Display the score and its transparent, category-level explanation."""
    st.subheader("ATS-style score")
    st.metric("Resume score", f"{score_result.total_score} / 100")
    st.caption("This score reflects only the extracted resume content and the rubric shown below.")

    for category in score_result.categories:
        st.markdown(f"#### {category.name}: {category.points} / {category.maximum_points}")
        st.write(category.rationale)
        st.caption(f"Improve: {category.improvement_tip}")


def render_empty_results() -> None:
    """Describe the profile view before a valid resume is uploaded."""
    st.subheader("Extracted resume profile")
    st.write("Upload a readable PDF resume to view its detected profile information and ATS-style score.")
