"""Explainable, deterministic ATS-style scoring for extracted profiles."""

from app.models.schemas import ATSScoreResult, ResumeProfile, ScoreCategory


SKILLS_MAXIMUM = 40
CERTIFICATIONS_MAXIMUM = 20
PROJECTS_MAXIMUM = 25
EDUCATION_MAXIMUM = 15


def _score_skills(profile: ResumeProfile) -> ScoreCategory:
    """Score detected skills at five points each, up to the category cap."""
    skill_count = len(profile.skills)
    points = min(SKILLS_MAXIMUM, skill_count * 5)
    return ScoreCategory(
        name="Skills",
        points=points,
        maximum_points=SKILLS_MAXIMUM,
        rationale=f"{skill_count} detected skill(s) at 5 points each, capped at {SKILLS_MAXIMUM}.",
        improvement_tip=(
            "Add clearly demonstrated technical skills to the resume."
            if skill_count == 0
            else "Add more relevant, demonstrated skills until this category reaches its cap."
        ),
    )


def _score_certifications(profile: ResumeProfile) -> ScoreCategory:
    """Score detected certification entries at ten points each, up to the cap."""
    certification_count = len(profile.certifications)
    points = min(CERTIFICATIONS_MAXIMUM, certification_count * 10)
    return ScoreCategory(
        name="Certifications",
        points=points,
        maximum_points=CERTIFICATIONS_MAXIMUM,
        rationale=(
            f"{certification_count} detected certification(s) at 10 points each, "
            f"capped at {CERTIFICATIONS_MAXIMUM}."
        ),
        improvement_tip=(
            "Add relevant completed certifications to a clearly labeled Certifications section."
            if certification_count == 0
            else "Add another relevant completed certification to reach this category's cap."
        ),
    )


def _score_projects(profile: ResumeProfile) -> ScoreCategory:
    """Score explicit project entries without evaluating their quality."""
    project_count = len(profile.projects)
    points = min(PROJECTS_MAXIMUM, project_count * 13)
    return ScoreCategory(
        name="Projects",
        points=points,
        maximum_points=PROJECTS_MAXIMUM,
        rationale=f"{project_count} detected project entry/entries at 13 points each, capped at {PROJECTS_MAXIMUM}.",
        improvement_tip=(
            "Add academic or personal projects with the technologies and outcomes stated."
            if project_count == 0
            else "Add another clearly described project to strengthen this category."
        ),
    )


def _score_education(profile: ResumeProfile) -> ScoreCategory:
    """Award points only when an education section was detected."""
    has_education = bool(profile.education)
    return ScoreCategory(
        name="Education",
        points=EDUCATION_MAXIMUM if has_education else 0,
        maximum_points=EDUCATION_MAXIMUM,
        rationale=(
            "An education section with resume details was detected."
            if has_education
            else "No education section was detected."
        ),
        improvement_tip=(
            "Keep degree, institution, graduation date, and relevant academic details current."
            if has_education
            else "Add an Education section with your degree and institution."
        ),
    )


def calculate_score(profile: ResumeProfile) -> ATSScoreResult:
    """Calculate a transparent ATS-style score out of 100.

    The score evaluates only extracted resume content. It does not use target
    roles, skill-gap logic, or external data, which belong to later phases.
    """
    categories = (
        _score_skills(profile),
        _score_certifications(profile),
        _score_projects(profile),
        _score_education(profile),
    )
    return ATSScoreResult(
        total_score=sum(category.points for category in categories),
        categories=categories,
    )
