> **Authority notation.** Bracketed source IDs resolve to `references/data/source_registry.csv`, which records authority class, binding status, effective date, access date, reliability, conflicts, superseded status, and re-verification date. Current controlling law prevails over policy, commentary, or community experience.

# Active-duty transition workflow

## Operating principle

Use the proposed separation date to generate a date-relative plan, then adapt it to service rules and actual notices. Official windows and deadlines must be labeled separately from recommendations. The local planner never files or transmits anything.

## Sequence

**Early phase.** Begin TAP as required, inventory health concerns without self-diagnosing, seek appropriate care, and identify records that may become hard to access. Normal TAP milestones begin well before separation; service-specific implementation and unanticipated separation rules may vary. [DOD-TAP-EVENTS] [DODI-1332.35]

**Records phase.** Reconcile service treatment, behavioral health, dental, hearing, vision, sleep, surgical, medication, civilian, deployment, exposure, line-of-duty, and relevant personnel records. Preserve copies and a request log. Missing service records do not justify inventing facts; identify alternate evidence and request assistance. [VA-EVIDENCE] [DOD-STR]

**Clinical phase.** Prepare one issue at a time: location/laterality, onset, frequency, severity, duration, variability, triggers, recovery, associated symptoms, functional effects, treatment, medication effects, devices, and questions. When care demands exceed available appointment time, recommend a sequence using urgent risk, current care needs, function, continuity, evidence fragility, unresolved conflicts, the user’s goals, and—when requested—transparent rating relevance. Rating or claim criteria may be used as a planning and completeness check for facts that are already true; they must not manufacture symptoms, dictate treatment, or replace clinical judgment. [CLIN-PATIENT-AGENDA] [CLIN-SDM]

**Claim-path phase.** If otherwise eligible, ordinary BDD is generally available from 180 through 90 days before separation. Verify known separation date, full-time status, exam availability, evidence, and exclusions. Outside the window, use the applicable standard or other path. [VA-BDD]

**SHA/IDES phase.** Confirm who will conduct the Separation Health Assessment. VA generally coordinates it for BDD and IDES; DoD generally handles members outside those paths or with fewer than 90 days. IDES/MEB/PEB questions are educational only because service fitness, disability evaluation, and VA compensation are distinct systems. [VA-SHA] [DOD-SHA] [DODI-1332.18]

**Final phase.** Preserve separation documents, establish continuity of prescriptions/equipment/specialty care, attend examinations, monitor actual notices, and verify any representative’s accreditation. [VA-C&P] [VA-REP] [VA-OGC-ACCREDITATION]

## Guard and Reserve cautions

Record each period of duty and characterization, orders, points, pay records, line-of-duty findings, and the date/mechanism of injury or disease. Active duty, ACDUTRA, and INACDUTRA are not interchangeable for benefits analysis. [USC-101] [CFR-3.6]

## Planner command

```bash
python scripts/generate_transition_plan.py --separation-date 2027-06-30 --as-of 2026-07-16 --format markdown
```

The output marks official windows, requirements, recommendations, optional practices, and matters requiring professional advice.

**Sources:** [VA-BDD] [VA-SHA] [DOD-TAP-EVENTS] [DODI-1332.35] [DODI-1332.18] [VA-EVIDENCE] [CFR-3.6]
