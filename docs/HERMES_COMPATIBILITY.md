# Hermes compatibility

## Verified specification

Release 1.0.0 is built against Hermes Agent v0.18.2 and its current Skills System/CLI documentation. The repository uses the default custom-tap path `skills/`, valid `SKILL.md` frontmatter, and only the supported `references/`, `templates/`, `scripts/`, `examples/`, and `assets/` support directories.

The main `SKILL.md` explicitly links every runtime file because direct URL/GitHub installation copies exact referenced support files rather than enumerating unrelated repository content. The automated simulated install confirms that the referenced set equals the runtime set.

## Security and lifecycle

Community tap and direct GitHub installs are expected to undergo Hermes security scanning. Users should inspect before install and should not override a dangerous verdict. Update provenance is retained by Hermes for `skills check` and `skills update`; uninstall uses `skills uninstall`. See `INSTALL.md` for commands.

## Supported range

`>=0.18.2,<0.19.0` for this release. This is a conservative compatibility declaration, not a claim that 0.19 will be incompatible. Re-test when Hermes changes frontmatter, tap indexing, allowlisted support directories, security policy, or install/update behavior.

## Publication verification still required

After a GitHub owner is selected and the repository is published:

1. Add the tap and inspect/search the skill.
2. Install by tap identifier.
3. Uninstall, then install by direct GitHub path.
4. Confirm all runtime files and slash-command discovery.
5. Run `hermes skills audit`, `check`, `update`, and `uninstall`.
6. Record Hermes version, platform, scan verdict, and file listing in release notes.
