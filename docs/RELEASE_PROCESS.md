# Release process

1. Freeze research cutoff and verify current controlling authorities.
2. Run source freshness and resolve stale controlling sources.
3. Review snapshot changes and effective dates; keep unsupported coverage explicit.
4. Run `python skills/va-disability-coach/scripts/validate_skill_bundle.py --repo-root .`.
5. Run `pytest -q`, Python compilation, JSON/YAML/CSV/schema checks, and local-link validation.
6. Confirm no scheduled workflows, credentials, PII, profile files, destructive actions, or unreferenced runtime support files.
7. Update VERSION, CHANGELOG, CITATION.cff, README counts, TEST_RESULTS, MANIFEST, tree, and checksums.
8. Build ZIP and uncompressed TAR, verify archive contents and SHA-256.
9. Tag `vX.Y.Z` under Semantic Versioning and publish release notes including estimator limits and source gaps.
10. Test custom-tap and direct GitHub installation against the declared Hermes range.
