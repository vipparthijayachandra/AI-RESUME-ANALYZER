# ResumeIQ Project Plan

## 1. Project Architecture

ResumeIQ will be a local, modular Python application with a Streamlit user interface. A student uploads a PDF resume, the application extracts and normalizes its text, analyzes the candidate profile, compares it with role requirements, and presents clear recommendations in a dashboard.

```text
Student PDF Resume
        |
        v
PDF Extraction & Text Cleaning
        |
        v
Resume Information Extraction
(skills, education, projects, experience)
        |
        +---------------------> SQLite role and skill data
        |
        v
ATS-Style Scoring & Role Matching
        |
        v
Skill-Gap Recommendations
        |
        v
Streamlit Results Dashboard
```

The design separates presentation, analysis, data access, and shared utilities. This keeps scoring logic explainable, enables independent testing of components, and makes future additions such as new roles or scoring criteria straightforward.

## 2. Modules and Responsibilities

| Module | Responsibility |
|---|---|
| Streamlit dashboard | Provides resume upload, controls, score summaries, role recommendations, and visual result views. |
| PDF processing | Reads PDF resumes with PyMuPDF and converts document pages into usable text. |
| Text preprocessing | Cleans extracted text, standardizes case and spacing, and prepares content for NLP analysis. |
| Resume parser | Identifies and structures skills, education, projects, and work experience from the resume text. |
| NLP and skill extraction | Uses keyword matching and NLP techniques to detect skills and related terms accurately. |
| ATS scoring engine | Produces an explainable score out of 100 using transparent weighted criteria such as skills, education, projects, and experience. |
| Role recommendation engine | Compares the student profile with defined job-role requirements and ranks suitable roles. |
| Skill-gap analysis | Lists matching skills, missing skills, and prioritized skills to develop for every recommended role. |
| Data repository | Stores role definitions, required skills, optional skills, score weights, and analysis history in SQLite. |
| Data models and utilities | Defines shared data structures, constants, validation, logging, and reusable helper functions. |

## 3. Planned Folder Structure

```text
ResumeIQ/
├── PROJECT_PLAN.md
├── README.md
├── requirements.txt
├── .gitignore
├── app/
│   ├── main.py
│   ├── dashboard/
│   │   ├── upload_view.py
│   │   ├── results_view.py
│   │   └── components.py
│   ├── services/
│   │   ├── pdf_processor.py
│   │   ├── text_preprocessor.py
│   │   ├── resume_parser.py
│   │   ├── ats_scorer.py
│   │   ├── role_matcher.py
│   │   └── skill_recommender.py
│   ├── data/
│   │   ├── database.py
│   │   ├── repositories.py
│   │   └── seed_data.py
│   ├── models/
│   │   └── schemas.py
│   └── utils/
│       ├── constants.py
│       └── validators.py
├── data/
│   ├── resumeiq.db
│   └── role_skill_catalog.csv
├── tests/
│   ├── test_pdf_processor.py
│   ├── test_resume_parser.py
│   ├── test_ats_scorer.py
│   └── test_role_matcher.py
└── docs/
    └── scoring_methodology.md
```

This is a target structure for later phases; it is not being created as part of this task.

## 4. Technologies and Their Purpose

| Technology | Purpose |
|---|---|
| Python | Core application language and integration layer. |
| Streamlit | Interactive dashboard for upload, analysis, and result visualization. |
| Pandas | Organizes role data, skill catalogs, score breakdowns, and tabular output. |
| NumPy | Supports numerical calculations and score normalization. |
| Scikit-learn | Enables text similarity, vectorization, and possible role-matching models. |
| PyMuPDF | Extracts text from uploaded PDF resumes. |
| SQLite | Provides lightweight local storage for roles, skills, scoring configuration, and optional analysis history. |
| NLP | Supports resume section detection, entity/keyword extraction, normalization, and semantic matching. |
| Git and GitHub | Version control, collaboration, issue tracking, and project documentation. |

## 5. Development Phases

1. **Planning and data design**
   - Define target job roles, the skill catalog, role requirements, resume fields, and transparent scoring criteria.

2. **Foundation setup**
   - Establish the project structure, dependency specification, database schema, configuration, and Git workflow.

3. **Resume ingestion**
   - Implement PDF upload, text extraction, validation, and text-cleaning workflows.

4. **Profile extraction**
   - Build extraction for skills, education, projects, and experience; validate output against sample student resumes.

5. **Explainable ATS scoring**
   - Implement the 100-point scoring rubric and show each category's contribution and improvement rationale.

6. **Role matching and recommendations**
   - Compare extracted profiles to role requirements, rank suitable roles, and compute matching and missing skills.

7. **Dashboard experience**
   - Build clear Streamlit views for the profile summary, ATS score, role cards, skill gaps, and development recommendations.

8. **Testing, refinement, and documentation**
   - Add automated tests, review edge cases, calibrate scores, document methodology, and prepare the repository for GitHub.

## 6. Data Flow

1. The student uploads a PDF resume through the Streamlit dashboard.
2. The PDF processing module extracts raw text using PyMuPDF.
3. The preprocessing module cleans and normalizes the text for consistent analysis.
4. The resume parser and NLP layer extract structured information: skills, education, projects, and experience.
5. The application reads job-role requirements and skill relationships from SQLite (and curated seed data).
6. The ATS scoring engine evaluates the structured profile using published weighted rules and returns a score out of 100 with a category-level explanation.
7. The role recommendation engine compares the student profile against each role and ranks the most suitable roles.
8. The skill-gap analysis produces matching skills, missing skills, and recommended skills to develop for each suggested role.
9. The Streamlit dashboard presents the extracted profile, score breakdown, recommendations, and actionable next steps.
10. If analysis history is enabled in a later phase, a privacy-aware summary of the result is saved to SQLite for retrieval and comparison.
