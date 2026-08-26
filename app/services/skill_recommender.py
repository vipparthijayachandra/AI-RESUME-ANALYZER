"""Deterministic skill-development recommendations from catalog skill gaps."""

from pathlib import Path

from app.models.schemas import ResumeProfile, RoleMatchResult, SkillRecommendation
from app.services.resume_parser import normalize_skill_name
from app.services.role_matcher import CATALOG_PATH, load_role_catalog


def _canonical_skill(skill_name: str) -> str:
    """Reuse the existing Phase 4 canonical skill vocabulary."""
    return normalize_skill_name(skill_name) or skill_name.strip()


def recommend_skills(
    profile: ResumeProfile,
    role_matches: list[RoleMatchResult],
    catalog_path: Path = CATALOG_PATH,
) -> list[SkillRecommendation]:
    """Recommend missing required catalog skills across the supplied role matches.

    Priority equals the number of supplied supported roles requiring a missing
    skill. Recommendations are sorted by descending priority and then skill
    name, so their order is stable and explainable.
    """
    catalog = load_role_catalog(catalog_path)
    present_skills = {_canonical_skill(skill) for skill in profile.skills if skill.strip()}
    supporting_roles: dict[str, set[str]] = {}

    for role_match in role_matches:
        required_skills = set(catalog.get(role_match.role_name, ()))
        for missing_skill in role_match.missing_skills:
            canonical_skill = _canonical_skill(missing_skill)
            if canonical_skill in required_skills and canonical_skill not in present_skills:
                supporting_roles.setdefault(canonical_skill, set()).add(role_match.role_name)

    recommendations = [
        SkillRecommendation(
            skill_name=skill_name,
            priority=len(roles),
            roles=tuple(sorted(roles, key=str.casefold)),
        )
        for skill_name, roles in supporting_roles.items()
    ]
    return sorted(recommendations, key=lambda recommendation: (-recommendation.priority, recommendation.skill_name.casefold()))
