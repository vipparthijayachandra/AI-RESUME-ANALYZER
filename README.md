# ResumeIQ

ResumeIQ is a Streamlit-based tool that will help students understand how their resumes align with entry-level job roles.

## Current status

Phase 2 foundation setup is complete. The project includes a modular application layout, dependency and Streamlit configuration, a local SQLite schema, PDF utilities, and a minimal Streamlit landing page. Resume ingestion, parsing, scoring, and role matching are intentionally deferred to later phases.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py
```

The application creates `data/resumeiq.db` on first run. This local database is intentionally excluded from version control.

## Git workflow

Keep source code, documentation, and the role-skill catalog under version control. Do not commit local virtual environments, Streamlit secrets, Python caches, or the generated SQLite database; the project `.gitignore` excludes them.

Before starting a focused change, check the working tree with `git status`. Review staged changes with `git diff --staged` before committing a coherent unit of work.

## Project documentation

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the agreed project architecture and development phases. See [docs/scoring_methodology.md](docs/scoring_methodology.md) for the future ATS-score design principles.
