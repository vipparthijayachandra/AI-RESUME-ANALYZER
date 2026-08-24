"""Deterministic role matching using the local role-skill catalog."""

import csv
from pathlib import Path

from app.models.schemas import ResumeProfile, RoleMatchResult
from app.services.resume_parser import normalize_skill_name


CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "role_skill_catalog.csv"
REQUIRED_SKILL_VALUES = {"1", "true", "yes"}


def _canonical_skill(skill_name: str) -> str:
    """Use the existing Phase 4 skill vocabulary whenever an alias is known."""
    return normalize_skill_name(skill_name) or skill_name.strip()


def load_role_catalog(catalog_path: Path = CATALOG_PATH) -> dict[str, tuple[str, ...]]:
    """Load only required skills for each role from the local CSV catalog."""
    with catalog_path.open(newline="", encoding="utf-8") as catalog_file:
        reader = csv.DictReader(catalog_file)
        required_columns = {"role_name", "skill_name", "is_required"}
        if reader.fieldnames is None or not required_columns <= set(reader.fieldnames):
            raise ValueError("The role skill catalog must include role_name, skill_name, and is_required columns.")

        catalog: dict[str, list[str]] = {}
        for row in reader:
            role_name = (row["role_name"] or "").strip()
            skill_name = (row["skill_name"] or "").strip()
            is_required = (row["is_required"] or "").strip().casefold()
            if not role_name or not skill_name or is_required not in REQUIRED_SKILL_VALUES:
                continue

            canonical_skill = _canonical_skill(skill_name)
            role_skills = catalog.setdefault(role_name, [])
            if canonical_skill not in role_skills:
                role_skills.append(canonical_skill)

    return {role_name: tuple(skills) for role_name, skills in catalog.items()}


def _normalized_profile_skills(profile: ResumeProfile) -> set[str]:
    """Normalize parsed skills while retaining unfamiliar values as written."""
    return {_canonical_skill(skill) for skill in profile.skills if skill.strip()}


def match_role(profile: ResumeProfile, role_name: str, required_skills: tuple[str, ...]) -> RoleMatchResult:
    """Calculate matching and missing required skills for one role.

    Match percentage = round((matching required skills / total required skills) * 100).
    """
    profile_skills = _normalized_profile_skills(profile)
    matching_skills = tuple(skill for skill in required_skills if skill in profile_skills)
    missing_skills = tuple(skill for skill in required_skills if skill not in profile_skills)
    percentage = round((len(matching_skills) / len(required_skills)) * 100) if required_skills else 0
    return RoleMatchResult(role_name, percentage, matching_skills, missing_skills)


def recommend_roles(profile: ResumeProfile, catalog_path: Path = CATALOG_PATH) -> list[RoleMatchResult]:
    """Return supported roles ranked by descending match and then role name."""
    catalog = load_role_catalog(catalog_path)
    results = [
        match_role(profile, role_name, required_skills)
        for role_name, required_skills in catalog.items()
    ]
    return sorted(results, key=lambda result: (-result.match_percentage, result.role_name.casefold()))
