# Freshness log

| Item | Effective through / revision | Retrieved or reviewed | Re-verify by | Status |
|---|---|---|---|---|
| Rating snapshot 1.0.0 | 2026-07-13 | 2026-07-16 | 2026-10-14 | Current at release |
| Source registry | Mixed; row-level metadata | 2026-07-16 | Row-level, generally 2026-10-14 | Current at release |
| Hermes packaging specification | v0.18.2 / main docs | 2026-07-16 | Before next release or Hermes 0.19 | Verified |
| BDD/SHA pages | Current pages | 2026-07-16 | 2026-10-14 | Verified |
| Crisis resources | Current pages | 2026-07-16 | 2026-10-14 | Verified |

Run:

```bash
python skills/va-disability-coach/scripts/check_source_freshness.py --as-of YYYY-MM-DD --json
```

The command is offline and does not update anything. The source-staging command is separate and user initiated.
