---
type: Meta
title: Vault wiki — start here
description: One-screen orientation to what this vault is, how it's organized, and how to read it. For a fast lay-of-the-land, especially on mobile/lightweight clients.
status: draft
updated: 2026-08-26
---

# What this is

An **agent-maintained knowledge wiki** compiled from the user's sources and notes. Agents (Claude) do the writing; the user's raw material stays frozen as evidence. The wiki is the distilled, navigable layer on top.

# How it's organized

- **[Concepts](concepts/)**: ideas, methods, technical and world knowledge (the research brain).
- **[Projects](projects/)**: ongoing work, one hub page per project plus satellites. Start point: the project hubs in the [[wiki/projects/index|index]].
- **[People](people/)**: collaborators and contacts.
- **[Entities](entities/)**: organizations, places, events, artworks: named things in the world that aren't people.
- **[Life](life/)**: personal facts and infrastructure agents need to act on the user's behalf.
- **[Craft](craft/)**: craft knowledge: how the user works right now (workflows, principles, stack defaults). Fast-evolving by design; the efforts themselves live in Projects, and project pages link here, not the reverse. For prose and writing rules, start at [[writing-style-system]]: it is the router, not the rule text (the rules live in machine files under `~/.claude`, and that page says which file owns which kind of rule).
- **[Agent](agent/)**: agent capability self-knowledge and operating instructions: what Claude's surfaces and tools can do on this deployment, and how agents should perform recurring tasks. The instantiation layer of Craft's principles: craft/ holds the why, agent/ holds the current mechanics.
- **[Connections](connections/)**: first-class claims that two things relate; the insight surface between notes and wiki.
- **[Log](log/)**: dated history of what the pipeline did (`log/<date>.md`). Skim, don't read whole.
- **[Chronicle](chronicle/)**: agent-written record of the *user's* days, one page per day plus weekly roll-ups. Opt-in via the cookbook's chronicle recipe. Sibling of Log: Chronicle records the user's days, Log records the pipeline's acts.

The link directory is [[wiki/index|index.md]]; this page is the prose orientation.

# How to read it (status weighting)

Every page's frontmatter carries a `status`. Weight what you read by it:

- **verified**: ground truth.
- **draft**: hypothesis; usable, but say so when it matters. **Most pages are drafts; that's by design, not a defect.**
- **stale**: re-verify before relying on it.
- **disputed**: don't build on it.
- A page flagged `pending_review: true` has a verified core plus draft-grade "Unreviewed additions".

(Reader's mirror of the ladder in `CLAUDE.md`, which is the authority: if they ever differ, CLAUDE.md wins.)

# How knowledge enters

One pipeline only: sources land in `sources/inbox/`, get filed (frozen) and distilled into wiki pages by the skills; the user's `notes/` are swept in the same way. Sources record *what was said*; the wiki decides *what's true* at the page layer. Full rules live in `CLAUDE.md` at the vault root. Term meanings (program, bundle, vault, hub, satellite, scope) live in `GLOSSARY.md` beside it.
