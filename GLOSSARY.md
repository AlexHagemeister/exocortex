---
updated: 2026-08-04 Tue, Aug 4 — 3:30 PM
---
# GLOSSARY — system vocabulary

This file owns **term meaning**. Procedures live in skills; invariants in CLAUDE.md; folder law in READMEs; principles in CONSTITUTION.md. When a definition and a rule disagree, fix the glossary or amend the rule — do not paper over with a second definition elsewhere.

Runtime surfaces say **you** and **the user**. Role nouns (Curator, Maintainer) appear only in CONSTITUTION.md and design docs.

## Zones and sharing

**program** — shippable system files per MANIFEST: rules, skills, substrate scripts, glossary, and supporting conventions; no personal data.
_Avoid:_ the vault, the wiki, the repo (ambiguous — name which surface)
_Home:_ CONSTITUTION.md § Sharing and boundaries; public repo MANIFEST

**bundle** — a contained folder of related knowledge; bundles nest freely (e.g. a project's bundle inside projects/). Unqualified, "the bundle" still means the outermost one: wiki/ alone, the OKF-conformant export surface — not the vault and not the program. (Sense widened per the user, 2026-07-20.)
_Avoid:_ the vault, the program, "my exocortex" (ambiguous)
_Home:_ CONSTITUTION.md § Sharing and boundaries (export sense); GLOSSARY only for the nested sense

**hub** — a project's central page: goals, current state, key decisions, links to satellites. In a bundle, the hub is the folder's authored `index.md` — a page, not a derived listing.
_Avoid:_ index (indexes are derived and regenerated; hubs are authored)
_Home:_ wiki/projects/README.md

**satellite** — a page holding one substantial sub-topic of a project, linked from its hub.
_Avoid:_ section (a satellite is a page, not a heading), sub-page
_Home:_ wiki/projects/README.md

**vault** — the whole personal knowledge installation: sources, notes, wiki, attachments, and pipeline bookkeeping.
_Avoid:_ the wiki, the program, the bundle
_Home:_ CLAUDE.md § Zones

**wiki** — agent-maintained compiled knowledge layer in wiki/; claims carry status and provenance.
_Avoid:_ the vault, notes, sources
_Home:_ wiki/README.md

**source** — frozen record of what was said, filed under sources/ after ingest moves it from inbox/.
_Avoid:_ truth claim, "the wiki says"
_Home:_ CLAUDE.md § Zones; sources/inbox/README.md (freeze-at-filing)

**attachment set** — several inbox items that are one source: a primary item plus the attachments it explicitly cites at capture. Each member files separately; one summary page cites them all.
_Avoid:_ bundle (a folder of wiki knowledge), "related captures" (topical similarity is not membership)
_Home:_ `.claude/skills/ingest/` step 4

**note** — the user's own writing in notes/; the maintainer never edits note bodies.
_Avoid:_ source, wiki page
_Home:_ CLAUDE.md § Zones

**inbox** — pre-pipeline capture queue at sources/inbox/; freely editable until ingest files an item.
_Avoid:_ the wiki, "pending pages"
_Home:_ sources/inbox/README.md

**staging** — import holding area at staging/; invisible to the pipeline until items move into notes/ or sources/inbox/.
_Avoid:_ inbox (that's sources/inbox/, the capture queue)
_Home:_ staging/README.md

**drawings** — shared sketch space at drawings/; the user's canvases and sketches plus agent-drawn diagrams, never swept or ingested by the pipeline. Location is the rule, not file type.
_Avoid:_ attachments (media embedded in pages), staging (import holding area)
_Home:_ drawings/README.md

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
_Avoid:_ spellcheck, cleanup, audit (that's the review-loop skill)
_Home:_ `.claude/skills/lint/`

**digest** — skill that compiles the user-facing review surface from pipeline output.
_Avoid:_ summary email, newsletter
_Home:_ `.claude/skills/digest/`

**audit-exocortex** — skill that runs the user's page review as an interactive loop: one page per turn, a reading brief with addressed items, explicit verdicts (correct / add / promote / skip). Suffixed to avoid collision with non-vault audit skills; "audit" unqualified in vault surfaces means this one.
_Avoid:_ lint (health checks), digest (compiles the review surface; audit is the loop that walks it)
_Home:_ `.claude/skills/audit-exocortex/`

**review-system** — creator-side skill (source vault only; not yet shipped) that reviews the system itself (rules vs disk, skill-layer drift, automation, human-loop health) on a fixed rubric; reports to .state/reviews/.
_Avoid:_ lint (page health), audit (content review loop)
_Home:_ `.claude/skills/review-system/`

**amend** — skill that changes rules, skills, or wiki folder structure with user approval.
_Avoid:_ fix the rules, edit CLAUDE.md (name the skill)
_Home:_ `.claude/skills/amend/`

**publish-program** — creator-side skill (source vault only; not shipped) that syncs vault program files to the public repo after user-reviewed diff.
_Avoid:_ push, backup, mirror
_Home:_ `.claude/skills/publish-program/`

**vault-snapshot** — skill that commits and pushes the vault git history for recovery and remote capture.
_Avoid:_ backup (ambiguous), publish (that's publish-program)
_Home:_ `.claude/skills/vault-snapshot/`

**update-exocortex** — skill that pulls the latest program release into this vault, reconciling local amendments.
_Avoid:_ upgrade, pull updates (name the skill)
_Home:_ `.claude/skills/update-exocortex/`

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

**modality** — how much evidential weight a stream grants its contents (declared in that stream's README); a filed item may carry its own `modality:` frontmatter line when the stream default would mislabel it, and the item's line wins.
_Avoid:_ tone, format
_Home:_ stream README (e.g. sources/meetings/README.md); `.claude/skills/ingest/` step 2 (per-item override)

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

**claim-neutral edit** — a user-directed wiki edit that changes no claim (style, structure, formatting, link fixes); applied directly on in-chat approval and day-logged — no knowledge enters, so no pipeline is bypassed.
_Avoid:_ correction (that flow is for wrong claims), override (this is rule-following, not an exception)
_Home:_ CLAUDE.md, single-pipeline rule

**self-interview** — the digest's 1–3 question-shaped items about the user per cycle: blind-spot (receipted hypothesis awaiting verdict), disclosure (the system doesn't know, asks), negative-space (neither knows); the user's verdict completes all bookkeeping.
_Avoid:_ survey, personality quiz, blind-spot report
_Home:_ `.claude/skills/digest/` compile 4b + Review interview-verdicts

**self-model page** — the joint self-knowledge ledger at wiki/life/self-model.md: trait- and pattern-level claims about the user, each claim's provenance naming whose knowledge it is (self-report / confirmed agent inference / a named person's feedback); only explicit user verdicts admit content.
_Avoid:_ user-model, profile (the self modeled is the user; the modelers are both parties)
_Home:_ wiki/life/README.md (page law)

**deployment profile** — environment bindings in meta/DEPLOYMENT.md; skills reference it, never hardcode paths.
_Avoid:_ config, settings (too generic)
_Home:_ meta/DEPLOYMENT.md

**MANIFEST** — allowlist in the public program repo naming vault paths that ship; adding a line is a publishing decision.
_Avoid:_ package.json, file list
_Home:_ public repo MANIFEST; `.claude/skills/publish-program/`

## Flagged ambiguities

- **repo** — three distinct repos in play: the vault (private), the public program, and optionally remote capture branches. Name which one.
- **maintainer** — design-time role noun only; runtime surfaces say "you" (the agent) and "the user."
