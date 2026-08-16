"""Shared domain data structures."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JobRole:
    """A role stored in the local role catalog."""

    name: str
    description: str


@dataclass
class ResumeProfile:
    """Structured resume data to be populated by the parser in Phase 4."""

    skills: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    experience: list[str] = field(default_factory=list)
