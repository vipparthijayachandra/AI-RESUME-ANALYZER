"""Tests for deterministic Phase 8 skill-development recommendations."""

from pathlib import Path

from app.models.schemas import ResumeProfile, RoleMatchResult
from app.services.skill_recommender import recommend_skills


def _write_catalog(path: Path) -> Path:
    """Create a compact required-skill catalog for recommendation tests."""
    path.write_text(
        "role_name,skill_name,is_required\n"
        "Data Analyst,Excel,true\n"
        "Data Analyst,SQL,true\n"
        "Python Developer,Git,true\n"
        "Python Developer,Excel,true\n"
        "Frontend Developer,React,true\n"
        "Frontend Developer,Docker,false\n",
        encoding="utf-8",
    )
    return path


def test_no_missing_skills_produces_no_recommendations(tmp_path: Path) -> None:
    """Complete role matches do not produce skills to develop."""
    profile = ResumeProfile(skills=["Excel", "SQL"])
    matches = [RoleMatchResult("Data Analyst", 100, ("Excel", "SQL"), ())]

    assert recommend_skills(profile, matches, _write_catalog(tmp_path / "catalog.csv")) == []


def test_one_missing_skill_produces_one_recommendation(tmp_path: Path) -> None:
    """A catalog-backed missing skill is returned with priority one."""
    matches = [RoleMatchResult("Data Analyst", 50, ("SQL",), ("Excel",))]

    recommendations = recommend_skills(
        ResumeProfile(skills=["SQL"]), matches, _write_catalog(tmp_path / "catalog.csv")
    )

    assert len(recommendations) == 1
    assert recommendations[0].skill_name == "Excel"
    assert recommendations[0].priority == 1
    assert recommendations[0].roles == ("Data Analyst",)


def test_shared_missing_skill_has_higher_priority_and_preserves_roles(tmp_path: Path) -> None:
    """One shared gap receives priority from each supported role requiring it."""
    matches = [
        RoleMatchResult("Python Developer", 0, (), ("Git", "Excel")),
        RoleMatchResult("Data Analyst", 0, (), ("Excel", "SQL")),
    ]

    recommendations = recommend_skills(
        ResumeProfile(), matches, _write_catalog(tmp_path / "catalog.csv")
    )

    assert recommendations[0].skill_name == "Excel"
    assert recommendations[0].priority == 2
    assert recommendations[0].roles == ("Data Analyst", "Python Developer")


def test_present_resume_skills_are_not_recommended(tmp_path: Path) -> None:
    """A present skill is filtered even when supplied as a stale missing entry."""
    matches = [RoleMatchResult("Data Analyst", 0, (), ("Excel", "SQL"))]

    recommendations = recommend_skills(
        ResumeProfile(skills=["excel"]), matches, _write_catalog(tmp_path / "catalog.csv")
    )

    assert [recommendation.skill_name for recommendation in recommendations] == ["SQL"]


def test_equal_priorities_use_alphabetical_skill_tie_breaking(tmp_path: Path) -> None:
    """Skills with equal catalog frequency are ordered alphabetically."""
    matches = [RoleMatchResult("Data Analyst", 0, (), ("SQL", "Excel"))]

    recommendations = recommend_skills(
        ResumeProfile(), matches, _write_catalog(tmp_path / "catalog.csv")
    )

    assert [recommendation.skill_name for recommendation in recommendations] == ["Excel", "SQL"]


def test_empty_unknown_and_optional_skills_do_not_invent_recommendations(tmp_path: Path) -> None:
    """Only required catalog skills can become recommendations."""
    catalog_path = _write_catalog(tmp_path / "catalog.csv")
    unknown_match = RoleMatchResult("Data Analyst", 0, (), ("Rust",))
    optional_match = RoleMatchResult("Frontend Developer", 0, (), ("Docker",))

    assert recommend_skills(ResumeProfile(), [], catalog_path) == []
    assert recommend_skills(ResumeProfile(), [unknown_match], catalog_path) == []
    assert recommend_skills(ResumeProfile(), [optional_match], catalog_path) == []


def test_phase_four_aliases_are_treated_as_present_skills(tmp_path: Path) -> None:
    """Known aliases do not become recommendations when the skill is present."""
    catalog_path = tmp_path / "catalog.csv"
    catalog_path.write_text(
        "role_name,skill_name,is_required\n"
        "Machine Learning Intern,Scikit-learn,true\n",
        encoding="utf-8",
    )
    match = RoleMatchResult("Machine Learning Intern", 0, (), ("Scikit-learn",))

    assert recommend_skills(ResumeProfile(skills=["sklearn"]), [match], catalog_path) == []
