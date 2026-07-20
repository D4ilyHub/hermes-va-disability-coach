# Contributing

Contributions are welcome for source corrections, clinical communication improvements, rating-rule changes, tests, and accessibility.

## Requirements

1. Use generic, de-identified examples. Never commit personal records, identifiers, credentials, or claim files.
2. Cite substantive legal, procedural, clinical, and rating assertions with a source ID present in `SOURCE_REGISTRY.csv`.
3. Prefer current controlling authority. Label M21-1, proposed rules, Board decisions, practitioner views, and community experience accurately.
4. Do not add behavior that diagnoses, prescribes, directs medication changes or testing, acts as legal representation, exaggerates, minimizes, manipulates facts or care to reach a target percentage, conceals facts, pressures a clinician, or files automatically. Transparent rating-aware comparison, evidence prioritization, and neutral questions about evaluation and treatment are allowed and encouraged within those boundaries.
5. Update the snapshot only after manual review, effective-date analysis, tests, changelog entry, and source metadata refresh.
6. Run `pytest -q` and `validate_skill_bundle.py`.
7. Add or update a de-identified coaching scenario when changing boundary calibration, recommendation style, treatment conversations, occupational-context reasoning, or correction behavior.

Use the issue templates for source corrections and rating-rule updates. A pull request must describe authority, effective date, affected files, tests, and any unresolved uncertainty.
