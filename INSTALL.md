# Installation

Verified against Hermes Agent **v0.18.2**. The supported range for this release is `>=0.18.2,<0.19.0`; later Hermes versions require compatibility re-verification.

Repository: `D4ilyHub/hermes-va-disability-coach`.

## Custom tap

```bash
hermes skills tap add D4ilyHub/hermes-va-disability-coach
hermes skills search va-disability-coach
hermes skills install D4ilyHub/hermes-va-disability-coach/va-disability-coach
```

## Direct GitHub install

```bash
hermes skills install D4ilyHub/hermes-va-disability-coach/skills/va-disability-coach
```

Hermes treats a new tap as community trust, stages the bundle for a security scan, and installs the exact support files referenced by `SKILL.md`. Review the scan report; do not override a dangerous verdict.

## Verify

```bash
hermes skills list
hermes skills audit
/va-disability-coach explain the skill boundaries
```

For repository validation:

```bash
python skills/va-disability-coach/scripts/validate_skill_bundle.py --repo-root .
pytest -q
```

## Upgrade

```bash
hermes skills check
hermes skills update va-disability-coach
```

Review `CHANGELOG.md`, source freshness, and local modifications before updating.

## Uninstall

```bash
hermes skills uninstall va-disability-coach
hermes skills tap remove D4ilyHub/hermes-va-disability-coach
```

Uninstalling the skill does not delete user-created documents elsewhere. This repository never installs or overwrites `SOUL.md`, `USER.md`, `MEMORY.md`, `config.yaml`, credentials, or user data.
