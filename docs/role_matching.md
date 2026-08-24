# Role Matching Methodology

ResumeIQ uses `data/role_skill_catalog.csv` as the complete source of supported roles and their requirements. The catalog has exactly three columns: `role_name`, `skill_name`, and `is_required`.

Only rows marked `is_required=true` participate in matching.

```text
Match percentage = round((matching required skills / total required skills) * 100)
```

Matching and missing skills are calculated only from the required catalog skills. Phase 4's canonical vocabulary is reused for known aliases: for example, `python3` matches `Python` and `sklearn` matches `Scikit-learn`.

Results are ranked by highest match percentage first, with role name as the alphabetical tie-breaker. Matching is deterministic and measures skill overlap only; it does not assess proficiency, project quality, or experience relevance. This phase identifies missing skills but does not provide skill-development recommendations.
