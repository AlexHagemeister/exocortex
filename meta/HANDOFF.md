# HANDOFF — Vault System Build Plan

Instructions for the implementation session (Claude Code, working in the vault). This document compiles the design session's decisions. Read it fully before writing anything. Normative order: this handoff > VAULT-DOCTRINE v0.3 (construction artifact, high-resolution reference) > OKF SPEC.md (external conformance target). Where this handoff is silent, consult the doctrine; where both are silent, ask the Curator.

## 1. What you are building

A personal AI knowledge system: an OKF-conformant, agent-maintained wiki compiled from the Curator's sources and live notes, with epistemic guardrails (status lifecycle, provenance, modality) built into every write path. The doctrine describes the whole design. Your job is to **distribute its operational rules into the surfaces where they bind** (CLAUDE.md, skills, READMEs) and scaffold the vault. The doctrine itself is a construction artifact — after the build, the operational parts of it are superseded by the surfaces; only CONSTITUTION.md remains authoritative for principles.

Delivered alongside this handoff: CLAUDE.md v1 (the one-page invariant core — place at vault root, do not expand past one page) and CONSTITUTION.md (principles, rationale, residence map — place at vault root).

## 2. End-state allocation (where every rule lives)

| Rule / element | Home |
|---|---|
| Ownership matrix + zone topology | CLAUDE.md (verbatim) |
| Single-pipeline rule | CLAUDE.md |
| Status semantics for readers (draft/verified/stale/disputed weighting) | CLAUDE.md |
| Instruction-conflict behavior: translate → disclose mechanism in one line → surface true conflicts → loud, logged overrides | CLAUDE.md |
| Corrections-as-statements — trigger/recognition | CLAUDE.md; reconciliation mechanics → `ingest` |
| Skill roster map | CLAUDE.md (pointers only) |
| Filing move (inbox → stream folder before citing), freeze-at-filing, validation gate (reject empty/truncated/junk → inbox/quarantine/), content-hash dedup | `ingest` |
| Frontmatter template, standard-markdown-link rule, observation/inference section split, provenance-required, index.md format | `ingest` — embed as **templates the agent fills**, not prose rules; conformance *checking* → `lint` |
| Draft-by-default; sole exception: verbatim Curator quotes born `verified` (paraphrases are NOT) | `ingest` |
| Modality meta-rule ("honor the stream README's declared evidential semantics") | `ingest`; each stream's actual modality → that stream's README |
| Notes sweep (diff vs. cursor in .state/), sync-conflict filename exclusion, quarantine routing | `process-inbox` |
| Verbatim quoting of pivotal exchanges; summary → inbox with provenance | `session-capture` |
| Index-first navigation, status-weighted synthesis with citations, write-back-as-draft, flow-of-use promotion on **explicit** confirmation only (politeness ≠ assent; when unsure, ask) | `query` |
| Staleness decay (per-type half-lives — start with placeholders, tune per §6), contradiction sweep (→ both pages `disputed`, queue), deleted-note withdrawal (claims resting solely on deleted note → `disputed`), stale note-citations (note changed after read-timestamp → re-ingest delta), retraction walk (inbound links + depends_on), connection expiry (~3 *reviewed* digests), orphans/red-link triage, frontmatter conformance, surface-vs-surface consistency sweep | `lint` |
| Digest triage (leverage-ranked: centrality, query traffic, dispute adjacency; hard cap 5–10), new-ISSUES.md-entries surfacing, Curator review marker (write to .state/ — this is the event expiry clocks count), 15-min tripwire (over budget → tighten cap/scoring, never the Curator's schedule) | `digest` |
| Mirror mechanics (vault → external non-iCloud git repo; observational, never a gate; recovery source for expired pages) | `mirror-snapshot` + deployment profile |
| Folder-refactor-as-migration (propose → Curator approves → execute with link-rewrite → log); rule-overridden-~3× → propose amendment | `amend` |
| Connection page semantics, promotion bar, expiry policy | wiki/connections/README.md; creation procedure → `ingest`; digest listing → `digest` |
| Stream modalities: calendar = intention never occurrence ("did X" needs second-stream corroboration); sessions = agent paraphrase of what was said; measurements carry error | sources/life/README.md, sources/sessions/README.md, sources/articles/README.md |
| Bundle boundary + sharing semantics (bundle = wiki/ alone; notes/ and .state/ never ship; public bundle sharing = redaction pass) | CONSTITUTION.md |
| Anti-pattern catalog with reasons | CONSTITUTION.md; each one also lands as a stated "don't" inside its owning skill (laundered inference → ingest; politeness-as-promotion → query; silent exception → CLAUDE.md; hand-healing → CONSTITUTION only, it binds the Curator; folder churn → amend; promiscuous capture → ingest, scoped to external content) |
| Purpose, roles, principles, rationale, residence map | CONSTITUTION.md |

**Residence rule for anything unlisted: who reads this rule, and when?** Every agent every turn → CLAUDE.md. During a procedure → that skill. When touching a folder → that folder's README. Only at design time / for adopters → CONSTITUTION.md. Curator-only norms → CONSTITUTION.md (agents don't need rules that bind the human).

## 3. Vault scaffold

Create ISSUES.md at vault root (agent-appendable friction log — operational bookkeeping like log.md, exempt from the pipeline; digest surfaces new entries). Create per doctrine §2 topology: .claude/skills/ (flat — one folder per skill, no grouping subfolders; nested .claude/skills/ discovery is documented but unreliable in the field, do not depend on it), sources/{inbox/{quarantine/},articles/,sessions/,life/}, wiki/{connections/}, notes/, .state/. Skills live at vault root so Claude Code sessions in the vault auto-register them, and outside wiki/ so OKF consumers never parse SKILL.md as concept documents. Each sources stream and each wiki folder gets index.md (derived; pipeline-regenerated; no frontmatter; OKF format) + README.md (authored semantics; frontmatter type: Meta). notes/ gets neither. wiki/ root gets index.md + log.md. **Staged bootstrap (the Curator has two existing vaults: a personal-notes vault and a prior LLM wiki):**
- *Stage 0 — empty system.* The Curator creates the vault themselves via Obsidian's "create vault → store in iCloud" flow (iCloud vaults must be born through the app or mobile Obsidian won't discover them) and places this handoff plus CLAUDE.md, CONSTITUTION.md, and VAULT-DOCTRINE.md inside it. You wake up in that vault: scaffold everything within it, and never create, rename, or relocate the vault folder itself. Exit criterion: one article runs clip → ingest → query end-to-end to the Curator's satisfaction.
- *Stage 1 — notes in.* Bulk-copy the personal-notes vault into notes/ (Curator zone, no invariants, no ceremony). Sweep + digest cycles begin. Exit: two Curator-reviewed digests with tolerable connection quality.
- *Stage 2 — legacy wiki retired.* The prior LLM wiki is small and its pages lack provenance/status (unaudited past-AI synthesis), so it does not enter the system at all. The Curator skims it once, re-clips the underlying sources still worth having into the new inbox (fresh, firsthand, full provenance), then archives or deletes the old vault. NEVER copy legacy wiki pages into wiki/ — the system's epistemic floor starts clean.

## 4. Skill-authoring conventions

- **Universal vocabulary only.** Runtime surfaces address the reading agent as "you" and the human as "the user." No role nouns (Curator/Maintainer stay in CONSTITUTION.md); "consumer" only in its OKF sense (external bundle-reading tooling). Every rule must be legible with zero glossary.
- **Rules as templates where possible.** A frontmatter block the skill fills beats a prose rule about frontmatter. Conformance should be the path of least resistance.
- **One-line whys.** Each embedded rule gets at most one clause of rationale ("sources are never edited — they record what was said, not what's true"). Full rationale lives in CONSTITUTION.md; don't duplicate it.
- **Portability.** No Curator-personal facts in skills. Deployment specifics (paths, machines, surface names) go in a DEPLOYMENT.md profile the skills reference, so the program ships clean.
- **Each skill is self-sufficient at L1.** An agent with CLAUDE.md + one skill + the READMEs of folders it touches must be able to execute correctly without the doctrine or other skills in context.
- **Skills read the README of any folder they write to.** State this in each skill.
- **Write to a branch of trust:** all wiki writes are `status: draft` unless the trust-inheritance exception applies. No skill ever promotes except `query` (flow-of-use) and `digest` (triage), and only on explicit Curator action.

## 5. Build order

1. Scaffold (§3) + place CLAUDE.md and CONSTITUTION.md at vault root. Fetch OKF SPEC.md from the GoogleCloudPlatform/knowledge-catalog repo (okf/SPEC.md) and pin the copy in the vault, noting the version/commit fetched — §4 templates are compiled against it, and the spec is an evolving draft. Keep it and VAULT-DOCTRINE.md as reference (suggest a meta/ or docs/ location outside the bundle — Curator's call).
2. `ingest` — the core loop; everything else depends on its conventions.
3. `query` — so the system pays rent immediately.
4. `process-inbox`, `session-capture`.
5. `lint`, `digest` (they need content to operate on; fine to author now, schedule after first ingests).
6. `mirror-snapshot` — requires the deployment decision (which machine hosts the non-iCloud repo). Ask the Curator; do not guess. **Git must not live inside the iCloud vault.**
7. `amend` — last; there must be a program before it can be amended.
8. First live test (Stage 0 exit): ingest one clipped article end-to-end, show the Curator the resulting pages, iterate. Then run `session-capture` retroactively on the design session (the Curator has it; this handoff summarizes decisions but the session contains reasoning worth keeping).

## 6. Open decisions (ask, don't assume)

- Physical home for the git mirror + scheduled agents (machine/runner).
- Per-type staleness half-lives (ship placeholders: life/infrastructure facts ~30d, conceptual pages ~180d; tune from lint output).
- wiki/ top-level topic folders — Curator chooses; propose 3–5 candidates from his existing material, keep few and stable (identity-is-path: renames are breaking migrations).
- Whether sources/ ships alongside the bundle when sharing (default: no).
- Mobile query via remote Claude Code session — test, don't architect around.
- Distribution end-state (deferred, do not design yet): a program-only git repo — skills, CLAUDE.md template, constitution, agent-followable SETUP.md — extractable from the live vault as a release artifact, such that "clone this repo and set up this system" works agent-to-agent. The authoring conventions (no personal facts, bindings referenced not hardcoded) exist to keep this extraction possible; honor them, build nothing else for it.

## 7. Fidelity notes (decisions easy to lose, with their reasons)

- **Freeze happens at filing, not capture** — inbox items are freely editable; the pipeline freezes only what it has cited.
- **Deletion of a note is withdrawal** — a speech act the wiki must hear, not a broken link to tolerate silently.
- **Expiry and staleness clocks tick on Curator review events, never wall-clock** — human-gated lifecycles count human acts (vacation must not expire good drafts).
- **Verified is scarce by design** — most of the wiki stays draft forever and reading agents are built for that; do not build anything that treats a large draft fraction as a problem to fix.
- **The notes stream has no curation gate on purpose** — zero friction is the point; the draft status and #no-ingest opt-out (respect this tag in the sweep) are the safety, not an inbox.
- **Session capture is a skill, not hooks** — the Curator triggers it; most sessions are not worth capturing.
- **The clipper already does an LLM tidy pass** — the ingest validation gate stays anyway (inbox is multi-tenant; the program must not assume any particular capture tool).
- **Skills live in vault/.claude/skills/, flat** — inside the portable unit, outside the bundle. Project-skill discovery only applies to Claude Code sessions opened in the vault (the maintainer surface, per topology); other surfaces remain read-only toward wiki/.
- **iCloud eviction is not deletion.** macOS "Optimize Mac Storage" can offload vault files, leaving `.name.icloud` placeholder stubs that CLI tools see instead of content. The notes sweep and lint MUST treat a placeholder as "evicted, present" — the deletion-is-withdrawal rule fires only when neither file nor placeholder exists. mirror-snapshot MUST refuse to snapshot (or force-download first) if placeholders are present, or backups silently omit content. The Curator should pin the vault ("Keep Downloaded" in Finder) on every Mac that touches it; the defensive checks exist because that setting is one toggle from undone.
- **Connection pages, never links appended to notes** — a connection is a claim needing the status lifecycle; notes/ is agent-inviolate and backlinks make wiki-side links visible on the note for free.
