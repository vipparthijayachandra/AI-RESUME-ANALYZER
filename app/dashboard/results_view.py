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
    """Display the extracted profile in a compact, scannable layout."""
    st.subheader("A. Resume Profile")
    st.caption("The following information was detected directly from the uploaded resume.")

    summary_columns = st.columns(4)
    summary_columns[0].metric("Skills", len(profile.skills))
    summary_columns[1].metric("Education entries", len(profile.education))
    summary_columns[2].metric("Projects", len(profile.projects))
    summary_columns[3].metric("Experience entries", len(profile.experience))

    left_column, right_column = st.columns(2)

    with left_column:
        _render_profile_items("Skills", profile.skills)
        _render_profile_items("Education", profile.education)
        _render_profile_items("Projects", profile.projects)

    with right_column:
        _render_profile_items("Work experience", profile.experience)
        _render_profile_items("Certifications", profile.certifications)


def render_ats_score(score_result: ATSScoreResult) -> None:
    """Display the unchanged score with an easier-to-scan breakdown."""
    st.subheader("B. ATS Score")
    score_column, description_column = st.columns((1, 3))
    with score_column:
        st.metric("Overall ATS-style score", f"{score_result.total_score} / 100")
        st.progress(score_result.total_score)
    with description_column:
        st.caption("This score reflects only the extracted resume content and the existing scoring rubric.")
        st.write("Review each category below to understand its contribution and the existing improvement guidance.")

    category_columns = st.columns(len(score_result.categories))
    for column, category in zip(category_columns, score_result.categories, strict=True):
        with column:
            st.metric(category.name, f"{category.points} / {category.maximum_points}")

    for category in score_result.categories:
        with st.expander(f"{category.name} details", expanded=False):
            st.write(category.rationale)
            st.caption(f"Improve: {category.improvement_tip}")


def _render_role_skills(title: str, skills: tuple[str, ...], empty_message: str) -> None:
    """Render catalog-derived skill evidence without adding recommendations."""
    st.markdown(f"#### {title}")
    if skills:
        st.markdown("\n".join(f"- {skill}" for skill in skills))
    else:
        st.caption(empty_message)


def render_role_matches(role_matches: list[RoleMatchResult]) -> None:
    """Display the existing deterministic role-match ranking as summary cards."""
    st.subheader("C. Recommended Job Roles")
    st.caption("Match % = matching required skills / total required skills × 100.")

    if not role_matches:
        st.info("No supported roles are currently available in the role-skill catalog.")
        return

    for role_match in role_matches:
        with st.container(border=True):
            title_column, match_column = st.columns((3, 1))
            with title_column:
                st.markdown(f"#### {role_match.role_name}")
                st.caption("Required-skill overlap with the extracted resume profile.")
            with match_column:
                st.metric("Role match", f"{role_match.match_percentage}%")
            st.progress(role_match.match_percentage)


def render_skill_gaps(role_matches: list[RoleMatchResult]) -> None:
    """Display catalog-based matching and missing skills for every role."""
    st.subheader("D. Skills / Gaps")
    st.caption("Skills are listed exactly from the role catalog after Phase 4 normalization.")

    if not role_matches:
        st.info("Role skill gaps will appear when supported roles are available.")
        return

    for role_match in role_matches:
        with st.expander(f"{role_match.role_name} skill alignment", expanded=False):
            matching_column, missing_column = st.columns(2)
            with matching_column:
                _render_role_skills(
                    "Matching skills",
                    role_match.matching_skills,
                    "No required skills from this role were detected.",
                )
            with missing_column:
                _render_role_skills(
                    "Missing skills",
                    role_match.missing_skills,
                    "No required skills are missing for this role.",
                )


def render_empty_results() -> None:
    """Provide a clear starting state before a valid resume is available."""
    with st.container(border=True):
        st.subheader("Your analysis workspace")
        st.write("Upload a readable PDF resume to view your profile, ATS-style score, role matches, and skill gaps.")
        st.caption("The analysis uses only information detected from your uploaded resume and the local role catalog.")
