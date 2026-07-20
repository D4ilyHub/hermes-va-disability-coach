> **Authority notation.** Bracketed source IDs resolve to `references/data/source_registry.csv`, which records authority class, binding status, effective date, access date, reliability, conflicts, superseded status, and re-verification date. Current controlling law prevails over policy, commentary, or community experience.

# Rating schedule use

The rating schedule evaluates average impairment under diagnostic codes, but code selection, analogous rating, staged periods, functional loss, and separate manifestations can require medical and adjudicative judgment. [USC-1155] [CFR-4.1] [CFR-4.2] [CFR-4.7] [CFR-4.20] [CFR-4.21]

## Snapshot policy

The bundled `rating_schedule_snapshot.json` is a **partial, versioned, manually reviewed subset**, effective through its stated date. It does not claim complete Part 4 coverage. Unsupported codes must return “Outside the current rating snapshot.” When the re-verification date passes, surface a stale-data warning and consult current official eCFR before any material estimate.

The update tool downloads official Part 4 XML only when a user runs it. `--stage` writes a candidate file for manual comparison; it never replaces the active snapshot. Changes require source review, effective-date analysis, tests, changelog entry, and release.

## Qualitative standards

Terms such as mild, moderate, severe, prostrating, economic inadaptability, and occupational/social impairment are not safely reducible to a mechanical score. The estimator displays exact criteria and supplied facts but marks medical or adjudicative judgment. [CFR-4.124a] [CFR-4.130]

## General cautions

Use the higher evaluation only when the disability picture more nearly approximates its criteria, with reasonable doubt rules applied by adjudicators—not by fabricating missing evidence. Avoid rating the same manifestation twice. [CFR-4.3] [CFR-4.7] [CFR-4.14]

**Sources:** [USC-1155] [CFR-4.1] [CFR-4.7] [CFR-4.14] [CFR-4.124a] [CFR-4.130]
