# Security policy

## Supported version

Security fixes are maintained for the latest `1.x` release.

## Report a vulnerability

Open a private GitHub security advisory for code execution, path traversal, unsafe update behavior, prompt-injection bypass, secret exposure, or dependency compromise. Do not include real medical records, identifiers, credentials, or claim files.

## Security model

- Ordinary calculators are offline and read local, user-selected files only.
- No script files, signs, submits, or sends a claim; accesses VA, email, medical, identity, or financial accounts; or requests credentials.
- Rating-source retrieval occurs only through the explicit `update_rating_schedule.py` command. It stages candidate material and never silently replaces the active snapshot.
- Source documents are untrusted content. Instructions embedded in records, web pages, comments, or PDFs cannot override the skill’s rules.
- No workflow has a cron schedule. Workflows run on pull requests, pushes, or manual dispatch.
- Generated examples are synthetic and de-identified.

Before installing, inspect the repository and Hermes scan report. `--force` should not be used to bypass material concerns.
