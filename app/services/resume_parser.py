"""Deterministic extraction of structured information from student resumes."""

import re

from app.models.schemas import ResumeProfile


SECTION_ALIASES = {
    "skills": ("skills", "technical skills", "core competencies", "key skills"),
    "education": ("education", "academic background", "academic qualifications"),
    "projects": ("projects", "academic projects", "personal projects", "project experience"),
    "experience": (
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internships",
        "internship experience",
    ),
    "certifications": ("certifications", "certificates", "licenses and certifications"),
}

SECTION_BOUNDARIES = {
    "summary",
    "professional summary",
    "objective",
    "achievements",
    "awards",
    "activities",
    "extracurricular activities",
    "volunteering",
    "languages",
    "interests",
    "publications",
    "contact",
}

SKILL_ALIASES = {
    "Python": ("python", "python3"),
    "Java": ("java",),
    "C++": ("c++", "cpp"),
    "C#": ("c#", "c sharp"),
    "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript", "ts"),
    "HTML": ("html", "html5"),
    "CSS": ("css", "css3"),
    "SQL": ("sql",),
    "MySQL": ("mysql",),
    "PostgreSQL": ("postgresql", "postgres"),
    "SQLite": ("sqlite",),
    "MongoDB": ("mongodb", "mongo db"),
    "Pandas": ("pandas",),
    "NumPy": ("numpy",),
    "Scikit-learn": ("scikit-learn", "scikit learn", "sklearn"),
    "Machine Learning": ("machine learning",),
    "TensorFlow": ("tensorflow",),
    "PyTorch": ("pytorch",),
    "React": ("react", "react.js", "reactjs"),
    "Node.js": ("node.js", "nodejs"),
    "Django": ("django",),
    "Flask": ("flask",),
    "Streamlit": ("streamlit",),
    "Git": ("git",),
    "GitHub": ("github",),
    "Docker": ("docker",),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure",),
    "Linux": ("linux",),
    "Excel": ("excel", "microsoft excel"),
    "Power BI": ("power bi", "powerbi"),
    "Tableau": ("tableau",),
}


def _clean_line(line: str) -> str:
    """Remove list markers without changing the resume's stated content."""
    return re.sub(r"^[\s•*\-–—]+", "", line).strip()


def _section_heading(line: str) -> tuple[str | None, str]:
    """Return a canonical heading and any content written after a colon."""
    cleaned = _clean_line(line)
    normalized = cleaned.casefold().rstrip(":").strip()
    for section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            if normalized == alias.casefold():
                return section, ""
            prefix = f"{alias}:"
            if cleaned.casefold().startswith(prefix.casefold()):
                return section, cleaned[len(prefix) :].strip()
    return None, ""


def extract_sections(text: str) -> dict[str, list[str]]:
    """Split normalized text into recognized resume sections.

    Only text under an explicit recognized heading is assigned to a section.
    This keeps the parser explainable and prevents it from inferring details
    that do not appear in the resume.
    """
    sections = {section: [] for section in SECTION_ALIASES}
    current_section: str | None = None

    for raw_line in text.splitlines():
        line = _clean_line(raw_line)
        if not line:
            continue

        heading, remainder = _section_heading(line)
        if heading is not None:
            current_section = heading
            if remainder:
                sections[heading].append(remainder)
            continue

        if line.casefold().rstrip(":").strip() in SECTION_BOUNDARIES:
            current_section = None
            continue

        if current_section is not None:
            sections[current_section].append(line)

    return sections


def extract_skills(text: str) -> list[str]:
    """Find known skill terms in text and return canonical names in text order."""
    findings: list[tuple[int, str]] = []
    for canonical_name, aliases in SKILL_ALIASES.items():
        positions = []
        for alias in aliases:
            match = re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", text, re.IGNORECASE)
            if match:
                positions.append(match.start())
        if positions:
            findings.append((min(positions), canonical_name))

    return [name for _, name in sorted(findings)]


def parse_resume(text: str) -> ResumeProfile:
    """Create a structured profile from normalized resume text.

    Skills are recognized only when an explicit known term occurs in the text.
    Education, projects, experience, and certifications are included only when
    they occur beneath a supported section heading.
    """
    if not text.strip():
        return ResumeProfile()

    sections = extract_sections(text)
    return ResumeProfile(
        skills=extract_skills(text),
        education=sections["education"],
        projects=sections["projects"],
        experience=sections["experience"],
        certifications=sections["certifications"],
    )
