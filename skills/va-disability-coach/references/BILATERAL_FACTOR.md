> **Authority notation.** Bracketed source IDs resolve to `references/data/source_registry.csv`, which records authority class, binding status, effective date, access date, reliability, conflicts, superseded status, and re-verification date. Current controlling law prevails over policy, commentary, or community experience.

# Bilateral factor

When compensable disabilities affect both arms, both legs, or paired skeletal muscles, the qualifying evaluations are combined first; ten percent of that combined value is added (not combined), the adjusted bilateral value is converted to a whole number, and that value is combined with other evaluations in severity order. When qualifying disabilities affect all four extremities, one bilateral calculation can include them. [CFR-4.26]

The calculator requires explicit `side` and `paired_group`; it will not infer pairing from a condition name. Zero-percent items do not establish a compensable pair.

## Most-favorable exception

Current § 4.26(d) requires removing one or more otherwise bilateral disabilities from the bilateral calculation when doing so creates a higher combined evaluation. The engine compares qualifying subsets deterministically and reports when the exception changes the result. [CFR-4.26] [FR-BILATERAL-2023]

## Example

Two 10-percent paired evaluations combine to 19; ten percent is 1.9; 20.9 converts to 21. In the regulatory-style sequence with 60 and 20 percent nonbilateral evaluations, 60 and 21 combine to 68, then 20 to 74, yielding 70 after final rounding. [CFR-4.26]

Complex anatomical pairing, paired muscle groups, amputations, and overlapping code questions require manual review.

**Sources:** [CFR-4.26] [FR-BILATERAL-2023] [CFR-4.25]
