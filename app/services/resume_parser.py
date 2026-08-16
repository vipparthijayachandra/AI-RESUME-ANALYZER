"""Contract for the future structured resume parser."""

from app.models.schemas import ResumeProfile


def parse_resume(_text: str) -> ResumeProfile:
    """Parse resume content in Phase 4."""
    raise NotImplementedError("Resume parsing is planned for Phase 4.")
