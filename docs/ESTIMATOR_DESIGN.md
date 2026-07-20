# Estimator design

## Architecture

The estimator has three independent layers.

### 1. Per-condition candidate comparison

`estimate_condition.py` accepts YAML or JSON containing a confirmed-diagnosis object, candidate codes, and facts with source provenance. It compares only explicit facts against a manually reviewed partial snapshot. Every criterion returns supported, conflicting, and missing facts plus medical/adjudicative flags. It never creates a diagnosis, nexus, service connection, or grant probability.

Qualitative criteria are displayed but not scored deterministically. A candidate range is descriptive of criteria still in play, not a predicted award. Unsupported codes return `Outside the current rating snapshot`; absent diagnosis returns `Not estimable`.

### 2. Combined-rating engine

`combine_ratings.py` implements table-equivalent remaining-efficiency calculations, half-up whole-number conversion after each combination, descending order, final nearest-ten rounding, explicit zero/100 handling, and the bilateral factor. It compares valid bilateral subsets to apply the current § 4.26(d) most-favorable exception.

The engine is deterministic, standard-library-only, offline, type-annotated, and emits a full trace. It assumes every input evaluation is valid and separately payable.

### 3. Separate flags

TDIU, SMC, hospitalization/convalescence/prestabilization, protections/reductions, paired-organ rules, amputation rule, extraschedular consideration, staged periods, and pyramiding remain flags. They are never folded automatically into the basic combined percentage.

## Snapshot maintenance

The active JSON snapshot records ID/version, source URL/IDs, retrieval and effective-through dates, stale-after date, normalization rules, coverage statement, criteria, manual-review flags, and code-level sources. The user-initiated updater fetches official eCFR XML and stages it for manual review; it never silently overwrites the snapshot.

A release update requires: inspect legal amendment/effective date; normalize criteria; two-person review where practical; add tests; update source registry and change log; run deterministic regression tests; regenerate checksums.

## Provenance model

Each fact supports source type, document name/date, page/section, exact extracted fact, fact character, confidence, and dispute status. Output repeats inputs and assumptions so a reviewer can audit the result.

## Non-goals

No diagnosis; treatment advice; claims filing; legal representation; probability of grant; target-rating coaching; automation of credibility, competency, nexus, code selection, extraschedular judgment, or qualitative severity.
