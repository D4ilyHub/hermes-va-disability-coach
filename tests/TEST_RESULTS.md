# Test results

**Final run date:** 2026-07-19  
**Repository version:** 1.0.0  
**Python:** 3.11.3 in the final local verification environment; project minimum 3.11  
**Hermes specification:** verified against Hermes Agent v0.18.2 documentation and repository layout

## Final results

| Check | Result |
|---|---:|
| Pytest | **399 passed** |
| Scenario contracts executed | **346 passed** |
| Bundle validator | **PASS — 719 checks, 0 errors** |
| Python compilation | **PASS** |
| Source freshness at 2026-07-16 | **CURRENT — 0 stale sources, snapshot current** |
| Simulated exact-reference Hermes install | **PASS — installed set equals all runtime files referenced by SKILL.md** |

## Scenario coverage

| File | Count |
|---|---:|
| `communication_scenarios.jsonl` | 50 |
| `coaching_scenarios.jsonl` | 6 |
| `transition_scenarios.jsonl` | 40 |
| `functional_scenarios.jsonl` | 50 |
| `estimator_scenarios.jsonl` | 50 |
| `combined_scenarios.jsonl` | 40 |
| `overlap_scenarios.jsonl` | 30 |
| `adversarial_scenarios.jsonl` | 30 |
| `safety_scenarios.jsonl` | 20 |
| `citation_scenarios.jsonl` | 30 |
| **Total** | **346** |

Each scenario records the input, expected behavior, prohibited behavior, required source class, required skill reference, pass criteria, actual result, and remediation.

## Calculator vectors and properties

Executed vectors include 50+30→65→70; 40+20→52→50; 60+40+20→81→80; zero evaluations; existing 100; bilateral 10/10; bilateral 20/20; four-extremity bilateral calculation; and the § 4.26(d) most-favorable exception. Property tests cover input-order invariance, monotonicity, bounds, and invalid input.

## Estimator tests

Tests cover supplied-diagnosis gating, unsupported codes, stale data, provenance preservation, qualitative mental-health criteria, overlap flags, no grant-probability field, mechanical tinnitus criteria, and scenario-level status outputs.

## Safety and security tests

Tests verify no profile files or OS metadata, no obvious contact information or absolute user-home paths, no scheduled workflows, no external-action code in core tools, user-initiated-only source staging, de-identified examples, source-registry thresholds and metadata, exact runtime references, local links, JSON/YAML/CSV parsing, Python syntax, and no obvious embedded secret assignments.

## Failure-driven remediation

The initial collection run exposed two generated test-file escaping errors; both test files were rewritten. Pre-suite manual checks also exposed YAML date normalization issues in the estimator and schema validator; date values are normalized to ISO strings. The 2026-07-19 verification exposed and fixed an f-string escaping error in the transition planner, then added coaching and repository-wide privacy regressions. No known test failures remain.

## Commands

```bash
pytest -q
python -m compileall -q skills tests
python skills/va-disability-coach/scripts/validate_skill_bundle.py --repo-root . --json
python skills/va-disability-coach/scripts/check_source_freshness.py --as-of 2026-07-16 --json
```

The Hermes CLI was not installed in the isolated build container. Installation behavior was therefore tested with an exact-reference copy simulation and validated against the current v0.18.2 official specification; a release maintainer should perform one live tap install and one direct GitHub install after publishing under the final GitHub owner.
