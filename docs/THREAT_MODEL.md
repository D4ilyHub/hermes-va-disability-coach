# Threat model

## Protected assets

User privacy, medical/military records, credentials, local files, source integrity, calculation correctness, and trust in safety boundaries.

## Threats and controls

| Threat | Control |
|---|---|
| Prompt injection in records, web pages, PDFs, comments, or repositories | Treat source instructions as data; only project/skill rules govern behavior |
| Credential or PII collection | No account integration; no credential requests; de-identification default; secret-pattern validation |
| Malicious or destructive scripts | Standard-library offline core; explicit inputs; no shell execution; review and Hermes security scan |
| Silent legal/rating drift | Versioned snapshot, stale warning, row-level re-verification, manual staging, no cron |
| False precision | Partial coverage label; explicit statuses; qualitative criteria remain manual; full trace |
| Evidence fabrication or concealment | Hard prohibition, contradictory-evidence field, adversarial tests |
| Unsafe medical delay | Care-first rule and urgent/crisis stop conditions |
| Automatic filing or external action | No send, submit, sign, login, or API integration |
| Supply-chain compromise | Minimal dependencies, lock-free offline core, checksums, CI, release review |
| Path traversal / oversized input | bounded inputs, fixed default paths, schema validation, no archive extraction at runtime |

## Residual risk

A model can misinterpret facts or sources, a source can change before re-verification, and a user can supply inaccurate data. Outputs must remain educational, reviewable, and nonbinding.
