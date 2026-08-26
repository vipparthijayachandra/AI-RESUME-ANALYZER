# Skill Development Recommendations

## Purpose

Phase 8 turns Phase 6 missing required skills into a deterministic list of skills to develop. It does not assess proficiency, hiring probability, or the quality of a candidate's projects.

## Inputs and catalog dependency

The recommender receives a parsed `ResumeProfile` and Phase 6 `RoleMatchResult` values. The local `data/role_skill_catalog.csv` remains the source of truth: only missing skills that are required by the matching role's catalog rows can be returned.

## Priority formula

```text
priority = number of supplied supported roles that require the missing skill
```

Skills already present in the resume are excluded. Known Phase 4 aliases use the same canonical names, such as `python3` to `Python` and `sklearn` to `Scikit-learn`.

Recommendations sort by descending priority, then skill name alphabetically. Each recommendation lists the supported roles that contribute to its priority. The system does not add optional or unknown skills and does not use external services.
