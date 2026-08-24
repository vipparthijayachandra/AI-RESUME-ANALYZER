"""Views for extracted resume-profile information."""

import streamlit as st

from app.models.schemas import ATSScoreResult, ResumeProfile, RoleMatchResult


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


def _render_role_skills(title: str, skills: tuple[str, ...], marker: str, empty_message: str) -> None:
    """Render catalog-derived skill evidence without adding recommendations."""
    st.markdown(f"**{title}**")
    if skills:
        st.markdown("\n".join(f"{marker} {skill}" for skill in skills))
    else:
        st.caption(empty_message)


def render_role_matches(role_matches: list[RoleMatchResult]) -> None:
    """Display deterministic role matches with matching and missing skills."""
    st.subheader("Recommended job roles")
    st.caption("Match % = matching required skills / total required skills × 100.")

    if not role_matches:
        st.info("No supported roles are currently available in the role-skill catalog.")
        return

    for role_match in role_matches:
        title = f"{role_match.role_name} — {role_match.match_percentage}% match"
        with st.expander(title, expanded=False):
            _render_role_skills(
                "Matching skills",
                role_match.matching_skills,
                "✓",
                "No required skills from this role were detected.",
            )
            _render_role_skills(
                "Missing skills",
                role_match.missing_skills,
                "•",
                "No required skills are missing for this role.",
            )


def render_empty_results() -> None:
    """Describe the profile view before a valid resume is uploaded."""
    st.subheader("Extracted resume profile")
    st.write("Upload a readable PDF resume to view its detected profile information and ATS-style score.")
