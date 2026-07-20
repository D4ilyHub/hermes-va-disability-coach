> **Authority notation.** Bracketed source IDs resolve to `references/data/source_registry.csv`, which records authority class, binding status, effective date, access date, reliability, conflicts, superseded status, and re-verification date. Current controlling law prevails over policy, commentary, or community experience.

# Combined ratings

VA combines evaluations using the Combined Ratings Table concept: start with the highest evaluation, apply the next evaluation to the remaining efficiency, convert each pair to the nearest whole number, continue in order, then convert the final value to the nearest multiple of ten with values ending in five rounded upward. Ratings are not added arithmetically. [CFR-4.25]

## Local engine

```bash
python scripts/combine_ratings.py --input examples/deidentified_rating_scenario.json
python scripts/combine_ratings.py --input examples/deidentified_rating_scenario.json --json
```

The output includes inputs, bilateral groups, bilateral base and addition, combination order, intermediate values, raw final value, final rounded evaluation, warnings, source IDs, version, and snapshot date.

Examples: 50 and 30 combine to 65, which rounds to 70; 60, 40, and 20 combine through 76 and 81, which rounds to 80. [CFR-4.25]

Zero-percent evaluations are retained but do not change the math. An existing schedular 100 produces a basic combined result of 100, while SMC or other ancillary analysis may remain relevant.

## What the engine does not decide

It assumes the input evaluations are valid and independently payable. It does not select codes, test pyramiding, apply the amputation rule, calculate paired-organ provisions, determine staged periods, or decide TDIU/SMC/temporary/protected evaluations.

**Sources:** [CFR-4.25] [CFR-4.14] [CFR-4.68]
