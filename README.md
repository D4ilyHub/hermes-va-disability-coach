# hermes-va-disability-coach

![A transitioning service member beside organized disability-claim records and a stethoscope, with the title VA Disability Coach](docs/hermes-va-disability-coach-banner.png)

An independent, care-first Hermes skill for VA disability education and active-duty transition planning—covering truthful clinician communication, evidence organization, C&P preparation, decision review, and transparent rating estimates.

> **Independent educational project; not affiliated with or endorsed by the U.S. Department of Veterans Affairs or Department of Defense. Not medical care, legal representation, a VA decision, or an emergency service.** The skill does not diagnose, prescribe, change medication, invent or conceal evidence, manipulate facts or care to reach a target percentage, pressure clinicians, file claims, access accounts, or request credentials.

## Design commitments

- **Care first. Accurate communication second. Claim documentation is a result of accurate care, not a substitute for care.**
- Uses a direct, calm, user-led coaching style that still makes concrete recommendations; distinguishes narrow hard boundaries from recommendations and user decisions.
- Uses occupational, duty, environmental, and cultural context to find blind spots and ask better questions—never to infer a diagnosis, exposure, nexus, or severity.
- Helps users prepare to discuss reasonable evaluation and treatment options without prescribing, directing medication changes, or pressuring clinicians.
- Is rating-aware without target-rating manipulation: it may compare criteria and evidence priorities for true reported issues, but never manufactures facts or steers care to reach a number.
- Replaces rejected assumptions and re-runs affected reasoning when the user corrects the coach; it does not preserve a rigid rule under softer wording.
- Supports all body systems without making PTSD the default lens.
- Separates symptoms, diagnoses, claimed conditions, service-connection theories, nexus evidence, diagnostic codes, and evaluations.
- Uses current controlling authority first and labels policy, clinical guidance, practitioner interpretation, and community experience.
- Uses only generic, de-identified examples; installs no profile or private case files.
- Makes uncertainty visible. Unsupported codes and stale data stop safely.

## Capabilities

The main skill routes automatically among 19 modes: pre-separation planning; issue inventory; record review; appointment preparation; sensitive communication; clinician role-play; claims explanation; service-connection mapping; exposure research; C&P preparation; evidence gaps; lay statements; decision review; appeal education; per-condition comparison; combined ratings; accredited-representative referral; urgent/crisis escalation; and source freshness.

## Install

See [INSTALL.md](INSTALL.md). Tap installation:

```bash
hermes skills tap add D4ilyHub/hermes-va-disability-coach
hermes skills install D4ilyHub/hermes-va-disability-coach/va-disability-coach
```

Direct installation:

```bash
hermes skills install D4ilyHub/hermes-va-disability-coach/skills/va-disability-coach
```

Verified Hermes version: **0.18.2**. Supported range for release 1.0.0: `>=0.18.2,<0.19.0`.

## Local tools

```bash
# Combined ratings and bilateral factor
python skills/va-disability-coach/scripts/combine_ratings.py   --input skills/va-disability-coach/examples/deidentified_rating_scenario.json

# Candidate condition comparison
python skills/va-disability-coach/scripts/estimate_condition.py   --input skills/va-disability-coach/templates/rating_estimate_input.yaml

# Date-relative separation plan
python skills/va-disability-coach/scripts/generate_transition_plan.py   --separation-date 2027-06-30 --as-of 2026-07-16

# Validation
python skills/va-disability-coach/scripts/validate_skill_bundle.py --repo-root .
pytest -q
```

## Estimator limits

The per-condition layer uses a manually reviewed **partial** snapshot containing 27 diagnostic-code entries. It never infers a diagnosis or service connection. Qualitative criteria remain medical or adjudicative judgments. The combined engine assumes supplied evaluations are valid and separately payable; it does not decide pyramiding, TDIU, SMC, temporary totals, protection rules, the amputation rule, paired-organ provisions, staged ratings, or extraschedular questions.

## Research

Research cutoff: **2026-07-16**. The registry contains **339** curated sources across **68** normalized domains, including **291** official/primary entries and **55** clinical entries. Registry inclusion means authority/relevance and metadata screening; critical controlling sources received content-level review. It is not a claim that every source was read exhaustively. See [research method](docs/RESEARCH_METHOD.md), [source registry](docs/SOURCE_REGISTRY.md), [contradictions](docs/CONTRADICTIONS.md), and [gaps](docs/RESEARCH_GAPS.md).

## Privacy

The skill does not need personal records to function. Users should work with de-identified summaries and retain private documents outside the repository. No telemetry or account integration is included.

## License

MIT covers original code and documentation. U.S. government materials, cited authorities, third-party works, trademarks, and linked content remain subject to their own status and terms. The repository summarizes rather than copying substantial secondary material.
