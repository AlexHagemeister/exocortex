---
updated: 2026-07-20 Mon, Jul 20 — 9:25 PM
---
# GLOSSARY — system vocabulary

This file owns **term meaning**. Procedures live in skills; invariants in CLAUDE.md; folder law in READMEs; principles in CONSTITUTION.md. When a definition and a rule disagree, fix the glossary or amend the rule — do not paper over with a second definition elsewhere.

Runtime surfaces say **you** and **the user**. Role nouns (Curator, Maintainer) appear only in CONSTITUTION.md and design docs.

## Zones and sharing

**program** — shippable system markdown per MANIFEST: rules, skills, glossary, and supporting conventions; no personal data.
_Avoid:_ the vault, the wiki, the repo (ambiguous — name which surface)
_Home:_ CONSTITUTION.md § Sharing and boundaries; public repo MANIFEST

**bundle** — wiki/ alone, OKF-conformant export surface; not the vault and not the program.
_Avoid:_ the vault, the program, "my exocortex" (ambiguous)
_Home:_ CONSTITUTION.md § Sharing and boundaries

**vault** — the whole personal knowledge installation: sources, notes, wiki, attachments, and pipeline bookkeeping.
_Avoid:_ the wiki, the program, the bundle
_Home:_ CLAUDE.md § Zones

**wiki** — agent-maintained compiled knowledge layer in wiki/; claims carry status and provenance.
_Avoid:_ the vault, notes, sources
_Home:_ wiki/README.md

**source** — frozen record of what was said, filed under sources/ after ingest moves it from inbox/.
_Avoid:_ truth claim, "the wiki says"
_Home:_ CLAUDE.md § Zones; sources/inbox/README.md (freeze-at-filing)

**note** — the user's own writing in notes/; the maintainer never edits note bodies.
_Avoid:_ source, wiki page
_Home:_ CLAUDE.md § Zones

**inbox** — pre-pipeline capture queue at sources/inbox/; freely editable until ingest files an item.
_Avoid:_ the wiki, "pending pages"
_Home:_ sources/inbox/README.md

## Pipeline skills

**ingest** — skill that files a source and compiles it into wiki pages.
_Avoid:_ import, add to the wiki, sync in
_Home:_ `.claude/skills/ingest/`

**process-inbox** — skill that drains sources/inbox/ and sweeps notes/ for deltas.
_Avoid:_ ingest (ingest handles one item; process-inbox orchestrates the queue and sweep)
_Home:_ `.claude/skills/process-inbox/`

**session-capture** — skill that preserves a conversation's durable knowledge as an inbox source.
_Avoid:_ ingest, remember this (name the skill)
_Home:_ `.claude/skills/session-capture/`

**query** — skill that answers from the vault with status-weighted citations.
_Avoid:_ search, chat about the vault
_Home:_ `.claude/skills/query/`

**lint** — skill that runs vault health checks and queues fixes.
_Avoid:_ spellcheck, cleanup, audit (too vague)
_Home:_ `.claude/skills/lint/`

**digest** — skill that compiles the user-facing review surface from pipeline output.
_Avoid:_ summary email, newsletter
_Home:_ `.claude/skills/digest/`

**amend** — skill that changes rules, skills, or wiki folder structure with user approval.
_Avoid:_ fix the rules, edit CLAUDE.md (name the skill)
_Home:_ `.claude/skills/amend/`

**publish-program** — skill that syncs vault program files to the public repo after user-reviewed diff.
_Avoid:_ push, backup, mirror
_Home:_ `.claude/skills/publish-program/`

**vault-snapshot** — skill that commits and pushes the vault git history for recovery and remote capture.
_Avoid:_ backup (ambiguous), publish (that's publish-program)
_Home:_ `.claude/skills/vault-snapshot/`

## Epistemics

**draft** — wiki status: hypothesis-grade; usable but say so when it matters.
_Avoid:_ unverified (use status labels), guess (use observation/inference sections)
_Home:_ CLAUDE.md § Reading wiki pages — status weighting

**verified** — wiki status: human-promoted ground truth; scarce by design.
_Avoid:_ true, confirmed (unless quoting a source), approved (politeness ≠ assent)
_Home:_ CLAUDE.md § Reading wiki pages — status weighting

**stale** — wiki status: past its review half-life; re-verify before relying on it.
_Avoid:_ old, outdated (use status)
_Home:_ CLAUDE.md § Reading wiki pages — status weighting; `.claude/skills/lint/` check 2

**disputed** — wiki status: contradictory evidence; do not build on it.
_Avoid:_ wrong, deprecated
_Home:_ CLAUDE.md § Reading wiki pages — status weighting

**pending_review** — frontmatter flag: verified core plus draft-grade "Unreviewed additions" sections.
_Avoid:_ draft (the core may still be verified)
_Home:_ CLAUDE.md § Reading wiki pages — status weighting

**provenance** — traceable origin of a claim (source path, URL, or the user's dated words).
_Avoid:_ citation (provenance is origin; citation is how you point at it)
_Home:_ CONSTITUTION.md principle 1

**modality** — how much evidential weight a stream grants its contents (declared in that stream's README).
_Avoid:_ tone, format
_Home:_ stream README (e.g. sources/meetings/README.md); `.claude/skills/ingest/`

**freeze** — the moment ingest files a source: path and content become immutable records of what was said.
_Avoid:_ lock, archive
_Home:_ sources/inbox/README.md; `.claude/skills/ingest/`

## Operations

**stream** — a permanent sources/ subfolder with its own modality README (articles/, sessions/, meetings/, life/, …).
_Avoid:_ folder, category (streams carry evidential semantics, not just taxonomy)
_Home:_ sources/inbox/README.md; `.claude/skills/ingest/` step 2

**issue** — friction-log entry in .state/issues/; ISSUES.md lists open issues only.
_Avoid:_ ticket, bug (unless quoting an external tracker)
_Home:_ ISSUES.md; `.state/README.md`

**day log** — dated pipeline history at wiki/log/<YYYY-MM-DD>.md.
_Avoid:_ journal, changelog (program changes use public CHANGELOG.md)
_Home:_ wiki/log/

**deployment profile** — environment bindings in meta/DEPLOYMENT.md; skills reference it, never hardcode paths.
_Avoid:_ config, settings (too generic)
_Home:_ meta/DEPLOYMENT.md

**MANIFEST** — allowlist in the public program repo naming vault paths that ship; adding a line is a publishing decision.
_Avoid:_ package.json, file list
_Home:_ public repo MANIFEST; `.claude/skills/publish-program/`

## Flagged ambiguities

- **repo** — three distinct repos in play: the vault (private), the public program, and optionally remote capture branches. Name which one.
- **maintainer** — design-time role noun only; runtime surfaces say "you" (the agent) and "the user."
