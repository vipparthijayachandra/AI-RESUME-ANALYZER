"""Contract for the future job-role matching engine."""

from app.models.schemas import ResumeProfile


def recommend_roles(_profile: ResumeProfile) -> list[str]:
    """Recommend roles in Phase 6."""
    raise NotImplementedError("Role matching is planned for Phase 6.")
