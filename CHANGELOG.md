# Changelog

Notable changes to the exocortex program, per release. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) — pre-1.0, a minor bump means new capability or a rule change, a patch means fixes and wording.

To update an installed vault, see [SETUP.md § Updating](SETUP.md#updating-an-existing-deployment) — or paste the update prompt from there into your agent. Watch this repo (Watch → Custom → Releases) to be notified of new versions.

## [Unreleased]

## [0.1.0] — 2026-07-19

First versioned release: the system as it stands after the vault-as-repo migration.

### Architecture
- The vault is itself a git repo with a private remote. The `vault-snapshot` skill (replacing `mirror-snapshot`) commits, pull-rebases, and pushes on schedule — history, rollback, and recovery live in the vault's own git history.
- Device sync, if wanted, is a dotfolder-ignoring layer (Obsidian Sync). iCloud and Dropbox must not hold the vault — they corrupt the repo.

### Added
- `INSTALL.md` — agent-guided install: one pasted prompt; the agent interviews, sets up, verifies, and hands off.
- SETUP.md § 8 — corpus-migration workflow for notes arriving from another app: batched, topic-coherent, review-paced.
- Ingest topic-tether rule: on a page the user's material justifies, cited external reference content is welcome; lookups never open new topics and lookup-derived content doesn't cascade.
- README rewritten as TL;DR → quick start → capabilities → workflow → rationale.
