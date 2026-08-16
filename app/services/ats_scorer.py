"""Contract for the explainable ATS scoring engine."""

from app.models.schemas import ResumeProfile


def calculate_score(_profile: ResumeProfile) -> int:
    """Calculate the ATS-style score in Phase 5."""
    raise NotImplementedError("ATS scoring is planned for Phase 5.")
