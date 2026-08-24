"""Tests for deterministic Phase 6 role matching and skill-gap analysis."""

from pathlib import Path

from app.models.schemas import ResumeProfile
from app.services.role_matcher import load_role_catalog, recommend_roles


def _write_catalog(path: Path) -> Path:
    """Create a small local catalog for focused role-matcher tests."""
    path.write_text(
        "role_name,skill_name,is_required\n"
        "Python Developer,Python,true\n"
        "Python Developer,SQL,true\n"
        "Python Developer,Git,true\n"
        "Data Analyst,Python,true\n"
        "Data Analyst,SQL,true\n"
        "Data Analyst,Pandas,true\n"
        "Frontend Developer,HTML,true\n"
        "Frontend Developer,CSS,true\n"
        "Frontend Developer,JavaScript,true\n"
        "Frontend Developer,Docker,false\n",
        encoding="utf-8",
    )
    return path


def test_load_role_catalog_includes_required_skills_only(tmp_path: Path) -> None:
    """Optional skill rows are excluded from the required-skill catalog."""
    catalog = load_role_catalog(_write_catalog(tmp_path / "catalog.csv"))

    assert catalog["Python Developer"] == ("Python", "SQL", "Git")
    assert catalog["Frontend Developer"] == ("HTML", "CSS", "JavaScript")


def test_exact_match_has_no_missing_skills(tmp_path: Path) -> None:
    """All required skills yield a 100 percent match."""
    profile = ResumeProfile(skills=["Python", "SQL", "Git"])

    result = recommend_roles(profile, _write_catalog(tmp_path / "catalog.csv"))[0]

    assert result.role_name == "Python Developer"
    assert result.match_percentage == 100
    assert result.matching_skills == ("Python", "SQL", "Git")
    assert result.missing_skills == ()


def test_partial_match_reports_missing_skills_and_rounds_percentage(tmp_path: Path) -> None:
    """Two of three required skills yields a 67 percent match."""
    profile = ResumeProfile(skills=["Python", "SQL"])
    results = recommend_roles(profile, _write_catalog(tmp_path / "catalog.csv"))
    data_analyst = next(result for result in results if result.role_name == "Data Analyst")

    assert data_analyst.match_percentage == 67
    assert data_analyst.matching_skills == ("Python", "SQL")
    assert data_analyst.missing_skills == ("Pandas",)


def test_multiple_roles_are_ranked_deterministically(tmp_path: Path) -> None:
    """Equal percentages are ranked alphabetically after percentage sorting."""
    results = recommend_roles(ResumeProfile(skills=["Python"]), _write_catalog(tmp_path / "catalog.csv"))

    assert [result.role_name for result in results] == [
        "Data Analyst",
        "Python Developer",
        "Frontend Developer",
    ]
    assert [result.match_percentage for result in results] == [33, 33, 0]


def test_empty_and_unknown_skills_match_nothing(tmp_path: Path) -> None:
    """Missing or unknown resume skills do not create catalog matches."""
    catalog_path = _write_catalog(tmp_path / "catalog.csv")

    assert all(result.match_percentage == 0 for result in recommend_roles(ResumeProfile(), catalog_path))
    assert all(
        result.match_percentage == 0
        for result in recommend_roles(ResumeProfile(skills=["Rust"]), catalog_path)
    )


def test_role_matching_reuses_phase_four_alias_normalization(tmp_path: Path) -> None:
    """Known aliases match the same canonical skills used by the parser."""
    catalog_path = tmp_path / "catalog.csv"
    catalog_path.write_text(
        "role_name,skill_name,is_required\n"
        "Machine Learning Intern,Python,true\n"
        "Machine Learning Intern,Scikit-learn,true\n",
        encoding="utf-8",
    )

    result = recommend_roles(ResumeProfile(skills=["python3", "sklearn"]), catalog_path)[0]

    assert result.match_percentage == 100
    assert result.matching_skills == ("Python", "Scikit-learn")
