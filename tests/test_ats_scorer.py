"""Tests for deterministic, explainable Phase 5 ATS-style scoring."""

from app.models.schemas import ResumeProfile
from app.services.ats_scorer import calculate_score


def test_empty_profile_scores_zero_with_all_categories_explained() -> None:
    """No extracted evidence receives no points and clear improvement tips."""
    result = calculate_score(ResumeProfile())

    assert result.total_score == 0
    assert [(category.name, category.points) for category in result.categories] == [
        ("Skills", 0),
        ("Certifications", 0),
        ("Projects", 0),
        ("Education", 0),
    ]
    assert all(category.improvement_tip for category in result.categories)


def test_complete_profile_reaches_the_score_cap() -> None:
    """Each category cap produces a 100-point score when all evidence exists."""
    profile = ResumeProfile(
        skills=[f"Skill {number}" for number in range(8)],
        education=["B.Tech, Example University"],
        projects=["Project one", "Project two"],
        experience=["Internship", "Responsibilities"],
        certifications=["AWS Cloud Practitioner", "Google Data Analytics"],
    )

    result = calculate_score(profile)

    assert result.total_score == 100
    assert [category.points for category in result.categories] == [40, 20, 25, 15]


def test_score_is_deterministic_and_shows_category_contributions() -> None:
    """The rubric's fixed rules give an explainable partial score."""
    profile = ResumeProfile(
        skills=["Python", "SQL"],
        education=["B.Sc. Computer Science"],
        projects=["Portfolio"],
        experience=["Software Intern"],
        certifications=["Python Institute Certificate"],
    )

    result = calculate_score(profile)

    assert result.total_score == 48
    assert [category.points for category in result.categories] == [10, 10, 13, 15]
    assert result.categories[0].rationale == "2 detected skill(s) at 5 points each, capped at 40."
    assert result.categories[1].rationale == "1 detected certification(s) at 10 points each, capped at 20."
    assert result.categories[3].rationale == "An education section with resume details was detected."


def test_category_scores_are_capped_and_experience_does_not_change_score() -> None:
    """Extra evidence is capped and experience remains outside Phase 5 scoring."""
    baseline = ResumeProfile(
        skills=[f"Skill {number}" for number in range(20)],
        education=["B.Tech", "Example University"],
        projects=["One", "Two", "Three"],
        certifications=["AWS", "Google", "Microsoft"],
    )
    with_experience = ResumeProfile(
        skills=baseline.skills,
        education=baseline.education,
        projects=baseline.projects,
        experience=["Internship", "Responsibilities", "Volunteer role"],
        certifications=baseline.certifications,
    )

    assert calculate_score(baseline).total_score == 100
    assert calculate_score(with_experience).total_score == 100
