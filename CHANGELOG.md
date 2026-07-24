# Changelog

Notable changes to the exocortex program, per release. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) — pre-1.0, a minor bump means new capability or a rule change, a patch means fixes and wording.

To update an installed vault, tell your maintainer "update my exocortex" (the `update-exocortex` skill) — or see [SETUP.md § Updating](SETUP.md#updating-an-existing-deployment) for the by-hand path. Watch this repo (Watch → Custom → Releases) to be notified of new versions.

## [Unreleased]

### Added
- **The digest surfaces new program releases** — each digest run fetches the program clone and, when a newer release exists, adds one line pointing at "update my exocortex." Notification now rides the surface users already review; applying still gates on their approval. INSTALL's handoff mentions this plus the GitHub Watch → Releases option.
- Onboarding handoff now suggests the Obsidian Web Clipper by name — articles and YouTube pages clip straight to the inbox; most new users don't know it exists.
- README shows the product instead of describing it: a worked capture-to-cited-answer example (transcript + the actual before/after files), a "your first five minutes" section, a Mermaid pipeline diagram, license badge, collapsible reference sections.
- **Upstream bug reports are now the documented norm** (ISSUES.md): when friction is in the shipped program rather than local amendments or data, maintainers file it on this repo's issue tracker in receiving-end detail — file, line, expected vs. observed, environment. Public-post rules apply: no vault content, no personal data, and the user approves before anything goes up (unattended runs draft locally for the digest). Formalizes the flow that produced issue #1.

## [0.3.0] — 2026-07-23

### Added
- Ko-fi support link: button in the README (§ Support) and a one-time mention at install handoff (INSTALL.md § 4, item 7).
- **`staging/` import folder** ships in the vault skeleton, with a README (zone: user-owned, invisible to the pipeline). Migrating users drop their exported corpus there and move batches into `notes/` or `sources/inbox/` deliberately — the move is the activation. SETUP § 9 rewritten around it; any other import route still works.
- **Obsidian setup section** (SETUP § 5, INSTALL interview + execute steps): open-as-vault, default attachment location → `attachments/`, default new-note location → `notes/`, Templater configured to auto-apply the shipped note template on file creation in `notes/` (the core Templates plugin can't fire on creation), and a field-tested caution scoping frontmatter-rewriting plugins away from wiki/.
- **Prerequisites now name the full dependency surface**: git (required), a GitHub account + `gh` CLI (optional, recommended for the private backup remote and bug reports). Onboarding walks users through account signup and `gh auth login` when wanted — always the user's own acts; the agent guides and never touches credentials.
- GLOSSARY entries: `update-exocortex` (was the one skill without a term home) and `staging`.

### Changed
- CLAUDE.md `.state/` zone row: "issue files any time" carve-out, resolving the self-contradiction with the file-an-issue instruction.
- Lint check 1's quote-provenance trigger narrowed to speech-attributed blockquotes — editorial callout boxes that merely mention the user no longer flag (was ~10 false positives per run on deliverables pages).
- The digest review-time tripwire number is stated only in the digest skill; the amend skill now points instead of restating it.
- meta/README's index-frontmatter policy line reconciled with practice (pre-2026-07-20 `updated:` stamps are grandfathered).
- vault-snapshot notes the optional hourly mechanical subset (snapshot-lite) and sweeps up anything it left behind — unpushed work, scan hits, conflicts (rode along from a 2026-07-22 vault amendment).

### Fixed
- `bootstrap.sh --update` now refreshes `GLOSSARY.md` (it was missing from the program-file copy list, so updated vaults silently kept a stale glossary) and never overwrites a live vault's `ISSUES.md` — the issue index is vault-owned and is now seeded only on fresh install (issue #1, reported by @amattinger).

## [0.2.0] — 2026-07-22

### Added
- **`update-exocortex` skill — updating is now a first-class, in-vault act.** Say "update my exocortex" in a vault session: the skill fetches the latest release, summarizes the changelog, waits for your go-ahead, commits a rollback point, reconciles your local amendments (keep yours / take upstream / merge — never silently overwritten) and sets aside skills you added locally before `bootstrap.sh --update` would delete them, applies, and stamps the new version. `meta/DEPLOYMENT.md` gains a `Program version` row (template updated; stamped at install). INSTALL.md and SETUP.md § Updating now delegate to the skill instead of duplicating the procedure.
- **`audit-exocortex` skill** — the interactive page-review loop: one page per turn, a reading brief with precisely addressed items, explicit verdicts (correct / add / promote / skip). The digest's review step now runs through it; promotion stays an explicit human act. GLOSSARY entry added.
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
- Ingest: inline quote-link form specified — in-prose quotes make the quoted words the link anchor; blockquotes end with a `— [the user, <date>](<path>)` citation line. Frontmatter `sources:` pinned as built-from provenance; lint check 1 syncs it additively (append missing body-link targets, never remove).
- Lint check 1: the YAML-parseability test now also covers `.state/issues/*.md` (the issue index is derived from them and cannot regenerate over a broken file).
- GLOSSARY: "bundle" sense widened — bundles are contained folders of related knowledge and nest freely; unqualified "the bundle" still means the wiki/ export surface. README Key terms and skill roster refreshed to match.

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
