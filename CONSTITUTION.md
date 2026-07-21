---
updated: 2026-07-20 Mon, Jul 20 — 1:18 PM
---
# CONSTITUTION — Principles of the Vault System

This is the design-time document: the purpose, roles, and principles from which every operational rule in this system derives. Every agent session reads it at start (per CLAUDE.md) — the working rules still live in CLAUDE.md, the skills, and folder READMEs. Return to it when changing the rules (the `amend` skill consults it), when a situation arises that no rule anticipated, or when deciding whether to adopt this system. Lineage: Karpathy's LLM-wiki pattern (Apr 2026) → Google's Open Knowledge Format v0.1 (Jun 2026) → this system.

## Purpose

One vault, three roles at once: a **research brain** (compiled knowledge of the world), a **memory brain** (compiled knowledge of the Curator's work and life), and an **agent substrate** (the context that lets any agent act as a colleague rather than a smart stranger). The wiki is optimized for agent consumption first, human browsing second — the files are the interface; any vault app is only a viewer.

## Roles

**The Curator** is the human: curates inputs, promotes drafts, adjudicates disputes, owns notes/, holds final say over the rules. Curation is the one job that cannot be delegated — the system's epistemic quality is bounded by what the Curator lets in and confirms. **The Maintainer** is the agent role: the skill set, wearable by any capable agent instance. Roles are hats, not identities. These names appear only here and in design documents; runtime surfaces say "you" and "the user," because a rule an agent follows mid-task must be legible with zero glossary.

## Principles

Everything operational instantiates one of these. When rules conflict or a novel case arises, reason from here.

1. **Provenance before claims.** No claim enters the wiki without a traceable origin — a source path, a URL, or the Curator's own words with a date. A knowledge base whose claims cannot be checked is not knowledge; it is confident text. This is verifiability as a design constraint, not truth: the system records what can be traced, and lets status carry how much to trust it.

2. **Freeze speech, never truth.** Sources are immutable records of what was said — never edited to "fix" them, because a source is evidence, not a claim. Truth-status lives one layer up, in the wiki, where claims can be disputed, outweighed, and retracted without falsifying the record of what anyone said. Corrections therefore arrive as *new speech* (the Curator's statement is itself a source), never as edits to old speech.

3. **Gate on status, not on merge.** Writes are never blocked; trust is graduated. Agents write freely as `draft`; promotion to `verified` is a human act; readers weight by status. This resolves the throughput asymmetry at the system's heart — machines write faster than humans can review — without either bottlenecking the machine or trusting it. Verified is scarce by design; a mostly-draft wiki is healthy.

4. **Rules live where they bind.** Every operational rule resides in the surface whose reader it governs: invariants in CLAUDE.md, procedures in skills, folder law in READMEs, Curator norms here. No rule lives twice. Attention is the scarce resource — adherence degrades with rule-set size, so every context an agent wakes up in contains only the rules binding now, in vocabulary that resolves without a glossary.

5. **Pay at write time so read time stays cheap.** Synthesis at ingest, not per query; templates over prose rules; indexes maintained, not derived on demand. Rules are read thousands of times and amended rarely; knowledge likewise. Spend machine labor and write-side complexity to keep the read side — where attention lives and errors compound — lean and reliable.

6. **Human-gated clocks count human acts.** Any lifecycle awaiting the Curator (draft expiry, review-based decay) ticks on review events, never wall-clock time. A vacation must not expire good work. Time is not attention; only attention gates.

7. **Curator–system friction is data.** A rule repeatedly overridden indicts the rule, not the Curator. Overrides are always permitted, always explicit, always logged; roughly three of the same means the Maintainer proposes an amendment. The rules are a Ulysses pact the Curator authored and may renegotiate — never a cage, and never silently bent.

8. **Curation cannot be delegated.** The agent absorbs every maintenance task except one: deciding what deserves to enter and what deserves trust. Bad sources poison the wiki; unreviewed promotion launders inference into fact. Every automation decision in this system preserves this one human bottleneck on purpose.

## Sharing and boundaries

The **program** is this document, CLAUDE.md, and .claude/skills/ — pure markdown, no personal data, shippable. The **bundle** is wiki/ alone (OKF-conformant). sources/ and notes/ are external referenced resources; an exported bundle carries dangling references to them by design (OKF consumers must tolerate broken links). notes/ and .state/ never ship. The boundary is file-level, not knowledge-level: wiki pages distill note content, so sharing a bundle publicly is a redaction pass, not a folder exclusion.

## Anti-patterns (named failure modes, with reasons)

- **Laundered inference** — a guess written with the typography of a fact. The deadliest failure: it propagates silently and poisons everything built on it. Status fields and observation/inference separation exist to prevent it.
- **Hand-healing** — the Curator editing wiki/ directly. It fixes the symptom, forks the agent's model of its own work, and leaves the upstream cause to reoffend. Root-cause instead; corrections flow through sources.
- **Promiscuous capture** — auto-ingesting external content without a curation gate. (The notes and life-data streams are exempt: the Curator's own speech and scheduled personal exports are pre-curated by definition.)
- **Silent exception** — an agent quietly complying with a rule-breaking instruction, or quietly reinterpreting it. Either way the Curator's mental model diverges from the system's reality. Translation must be spoken; overrides must be logged.
- **Politeness-as-promotion** — inferring verification from friendly acknowledgment. The trust ledger records explicit assent only.
- **Folder churn** — casual reorganization of wiki/. Identity is path; a rename breaks every inbound link. Refactors are migrations: proposed, approved, executed with a link rewrite, logged.
- **Silent retraction** — correcting a claim without re-examining what was built on it. Local healing, global poisoning; the retraction walk exists for this.

## Residence map (where everything lives)

| Concern | Surface |
|---|---|
| Invariants: zones, single pipeline, status weighting, conflict protocol, corrections trigger | CLAUDE.md (one page, hard budget) |
| Procedures and their rules | the owning skill in .claude/skills/ |
| Folder-local law (stream modality, connection policy) | that folder's README.md |
| Principles, rationale, roles, sharing semantics, this map | here |
| File-format conformance target | meta/OKF-SPEC.md (pinned copy of an external spec; never loaded at runtime — compiled into templates) |
| Environment bindings (machines, paths, sync, surfaces) | deployment profile — meta/DEPLOYMENT.md (skills reference it, never hardcode; deployment config may point at the program but never contain it) |

Changing a rule = editing its one home, via `amend`, with the Curator's approval. Changing a principle = editing this document, which should be rare and deliberate — principles are what the rules are *for*.
