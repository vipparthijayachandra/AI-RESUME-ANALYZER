"""Contract for future skill-gap recommendations."""

from app.models.schemas import ResumeProfile


def recommend_skills(_profile: ResumeProfile, _role_name: str) -> list[str]:
    """Recommend missing skills in Phase 6."""
    raise NotImplementedError("Skill recommendations are planned for Phase 6.")
