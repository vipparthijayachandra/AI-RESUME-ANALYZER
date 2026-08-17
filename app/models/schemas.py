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
