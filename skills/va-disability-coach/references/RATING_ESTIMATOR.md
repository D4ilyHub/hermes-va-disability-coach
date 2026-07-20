> **Authority notation.** Bracketed source IDs resolve to `references/data/source_registry.csv`, which records authority class, binding status, effective date, access date, reliability, conflicts, superseded status, and re-verification date. Current controlling law prevails over policy, commentary, or community experience.

# Per-condition candidate estimator

## Preconditions

The estimator requires an explicitly supplied diagnosis object, candidate code or safe alias match, and provenance-bearing facts. It does not diagnose, decide service connection, predict grant probability, or select the legally correct diagnostic code.

## Output

For each candidate code it displays current bundled criterion text; supporting facts; conflicting facts; missing facts; medical/adjudicative judgment flags; laterality; notes; source IDs; and a cautiously labeled candidate range. Status values are:

- Supported by supplied documentation
- Potentially supported
- Insufficient documentation
- Conflicting documentation
- Requires medical determination
- Requires adjudicative judgment
- Not estimable
- Outside the current rating snapshot

A mechanical match means only that supplied facts meet the encoded comparison. It is not a rating decision. Multiple plausible codes and overlapping manifestations are flagged for manual review. [CFR-4.14] [CFR-4.20] [CFR-4.27]

## Command

```bash
python scripts/estimate_condition.py --input templates/rating_estimate_input.yaml
```

Inspect `input_facts`, provenance, assumptions, source IDs, snapshot date, and warnings. Never report only the highest number.

## Separate flags

TDIU, SMC, temporary totals, convalescence, hospitalization, prestabilization, protections, paired-organ provisions, amputation rule, extraschedular consideration, staged ratings, and pyramiding remain separate flags. [CFR-4.16] [CFR-3.350] [CFR-4.29] [CFR-4.30] [CFR-4.68]

**Sources:** [CFR-4.1] [CFR-4.7] [CFR-4.14] [CFR-4.20] [CFR-4.27]
