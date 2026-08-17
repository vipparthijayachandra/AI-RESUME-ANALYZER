"""Tests for deterministic Phase 4 resume-profile extraction."""

from app.models.schemas import ResumeProfile
from app.services.resume_parser import extract_sections, parse_resume
from app.services.text_preprocessor import normalize_text


def test_parser_extracts_profile_from_common_student_resume_sections() -> None:
    """Skills and explicit profile sections are structured without inference."""
    text = normalize_text(
        """
        TECHNICAL SKILLS
        Python, SQL, pandas, scikit learn, GitHub
        EDUCATION
        B.Tech in Computer Science, ABC University, 2026
        CGPA: 8.7
        ACADEMIC PROJECTS
        ResumeIQ | Python, Streamlit
        Library Management System | Java, MySQL
        INTERNSHIP EXPERIENCE
        Data Intern, Acme Labs | June 2025 - August 2025
        Built data reports with Excel.
        CERTIFICATIONS
        Google Data Analytics Certificate
        """
    )

    profile = parse_resume(text)

    assert profile.skills == [
        "Python",
        "SQL",
        "Pandas",
        "Scikit-learn",
        "GitHub",
        "Streamlit",
        "Java",
        "MySQL",
        "Excel",
    ]
    assert profile.education == ["B.Tech in Computer Science, ABC University, 2026", "CGPA: 8.7"]
    assert profile.projects == [
        "ResumeIQ | Python, Streamlit",
        "Library Management System | Java, MySQL",
    ]
    assert profile.experience == [
        "Data Intern, Acme Labs | June 2025 - August 2025",
        "Built data reports with Excel.",
    ]
    assert profile.certifications == ["Google Data Analytics Certificate"]


def test_section_detection_supports_inline_and_format_variations() -> None:
    """Common heading variations and same-line values are detected."""
    sections = extract_sections(
        """Skills: Python | nodejs | POWER BI
Academic Background:
- Bachelor of Engineering, Example College
Personal Projects:
• Portfolio Website
Professional Experience:
Software Intern, Example Co.
Certificates: AWS Cloud Practitioner
"""
    )

    assert sections["skills"] == ["Python | nodejs | POWER BI"]
    assert sections["education"] == ["Bachelor of Engineering, Example College"]
    assert sections["projects"] == ["Portfolio Website"]
    assert sections["experience"] == ["Software Intern, Example Co."]
    assert sections["certifications"] == ["AWS Cloud Practitioner"]


def test_parser_normalizes_common_skill_variations() -> None:
    """Known spelling variations map to one canonical displayed skill."""
    profile = parse_resume("Skills: python3, JS, react.js, NodeJS, sklearn, PostgreSQL")

    assert profile.skills == [
        "Python",
        "JavaScript",
        "React",
        "Node.js",
        "Scikit-learn",
        "PostgreSQL",
    ]


def test_parser_returns_empty_fields_for_missing_sections_without_inventing_data() -> None:
    """Unheaded statements do not become education, projects, or experience."""
    profile = parse_resume("Motivated student seeking an opportunity. Familiar with Python.")

    assert profile.skills == ["Python"]
    assert profile.education == []
    assert profile.projects == []
    assert profile.experience == []
    assert profile.certifications == []


def test_parser_returns_empty_profile_for_empty_text() -> None:
    """Empty normalized input yields an empty, valid schema object."""
    assert parse_resume("   ") == ResumeProfile()
