# Changelog

Notable changes to the exocortex program, per release. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) — pre-1.0, a minor bump means new capability or a rule change, a patch means fixes and wording.

To update an installed vault, see [SETUP.md § Updating](SETUP.md#updating-an-existing-deployment) — or paste the update prompt from there into your agent. Watch this repo (Watch → Custom → Releases) to be notified of new versions.

## [Unreleased]

### Added
- **GLOSSARY.md** — canonical system vocabulary (term meanings with Avoid/Home pointers). Ships with the program; CLAUDE.md points agents at it when jargon is ambiguous. Public README gains a Key terms skim subset; `tools/sync.sh` fails the publish if those one-liners drift from GLOSSARY.md.
- Folder law READMEs for `attachments/` and `templates/` (zone rows already existed; agents can now satisfy "read the README before writing").
- **Onboarding posture** (INSTALL §4 Hand off + SETUP §7): minimum viable use first; invite "explain it simply"; rules change via `amend` with approval — not freestyle; principle tension → plain-language tradeoff brief, then the user decides.
- **Voice — your maintainer's communication style is now yours to choose.** The setup interview asks how your maintainer should talk to you; INSTALL.md § 1a elicits it by example (the same digest message in three voices — pick, blend, or write your own) and saves a confirmed spec, never just a label. The spec lives in your `meta/DEPLOYMENT.md` `## Voice` section (user-owned, survives updates); CLAUDE.md binds sessions to adopt it — tone only, never the epistemic rules: status labels, provenance, disputes, and corrections stay plain in every voice.
- Zone rows for `attachments/` and `templates/` in CLAUDE.md — both user-owned; the agent reads freely, writes only with explicit approval.
- Digest skill: retroactive review markers — when act-evidence shows a review that never got its marker, reconstruct it (dated to the acts, noted as reconstructed); unattended runs surface the evidence instead.
- Ingest: verbatim user quotes carry an inline source link at the quote; lint check 1 enforces it.
- Lint check 5: consuming a deleted note re-reads every citing page — standing flags sourced to withdrawn evidence are queued, never silently kept; annotated tombstones recognized as already reconciled.

### Changed
- CONSTITUTION § Sharing: program definition matches MANIFEST (shippable system markdown; `.state/` contents never ship, its README may).
- Amend skill: when a proposal tensions with a principle, push back with tradeoffs before asking for approval; jargon changes update GLOSSARY.md in the same pass.
- Issue-workflow residence: `~3` cluster threshold lives in amend; close procedure lives in ISSUES.md; digest points.
- Digest last-call for connection expiry points at lint check 7 instead of deriving a duplicate number.
- Lint check 1: folder `README.md` files exempt from the `sources:` requirement (Meta documentation, not claim pages).
- Status-weighting ladder now lives only in CLAUDE.md; the query skill points to it instead of restating it.
- `publish-program` skill now carries the release protocol: changelog maintenance, version tagging, and GitHub releases are part of the publish procedure.
- Note template timestamps use a human-readable date format.
- Ingest: page `description` fields are written as retrieval hooks — third person, what the page holds + when to fetch it — since that line is often all an agent sees when deciding whether to load the page (per Anthropic's context-engineering guidance).
- Query: long multi-page syntheses place fetched content above the question and quote load-bearing passages before reasoning — both measurably improve long-context accuracy.
- Lint and process-inbox eviction guards generalized to sync-layer-neutral wording (iCloud kept as a filename example, dropped as an environment assumption).
- Two stale path references corrected: CONSTITUTION's residence map now names `meta/OKF-SPEC.md`; meta/README's move-instructions name the real dependents instead of a deleted skill.

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
