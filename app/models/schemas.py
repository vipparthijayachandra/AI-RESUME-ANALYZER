"""Shared domain data structures."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JobRole:
    """A role stored in the local role catalog."""

    name: str
    description: str


@dataclass
class ResumeProfile:
    """Structured information extracted from a student's resume."""

    skills: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ScoreCategory:
    """One transparent contribution to an ATS-style score."""

    name: str
    points: int
    maximum_points: int
    rationale: str
    improvement_tip: str


@dataclass(frozen=True)
class ATSScoreResult:
    """An explainable resume score and its category-level breakdown."""

    total_score: int
    categories: tuple[ScoreCategory, ...]


@dataclass(frozen=True)
class RoleMatchResult:
    """An explainable comparison between a resume and one role's requirements."""

    role_name: str
    match_percentage: int
    matching_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
