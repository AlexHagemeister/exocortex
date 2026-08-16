---
updated: 2026-08-11
---
# CLAUDE.md — Vault Operating Rules

This vault is the user's knowledge system, an agent-maintained wiki compiled from their sources and notes. You are reading its core rules. Everything here binds you on every turn inside this vault. Work in another repository or directory follows that project's own instructions, not these. Folder-specific rules live in each folder's README.md. Read the README of any folder before writing to it. Skill procedures live in .claude/skills/. Principles live in CONSTITUTION.md, imported below so every session loads it. When no rule anticipates a case, reason from the principles. When a system term is ambiguous, or when amending vocabulary, read GLOSSARY.md. Do not paste definitions here. When using a term the user may not know, give the one-liner once or point at the entry. If meta/DEPLOYMENT.md has a `## Voice` section, adopt it. It governs tone only. Status labels, provenance, disputes, and corrections stay plain.

## Zones — who writes where

| Zone | You may | You may not |
|---|---|---|
| sources/ | add files to sources/inbox/; file inbox items to stream folders during ingest | edit or delete anything already filed (sources are frozen records of what was said, not truth claims) |
| wiki/ | create and edit pages, **only via the skills** | write directly outside a skill procedure |
| notes/ | read, link to, ingest from; sweep write-back of frontmatter metadata (additive only, pointers to existing wiki pages); maintain notes/index.md (derived index, rules in process-inbox) | touch note bodies, or edit/delete anything the user wrote (the words are the user's alone) |
| attachments/ | read, embed-link; move/rename/delete when the user explicitly and specifically approves | touch files otherwise (the user's media, and Obsidian files new attachments here) |
| drawings/ | read, embed-link, create and edit drawings | sweep, ingest, or index anything here (a shared sketch space the pipeline never reads) |
| artifacts/ | read, embed-link, create and edit artifacts when the user directs | sweep, ingest, cite as evidence, or index anything here (a shared workspace for co-built work products the pipeline never reads) |
| templates/ | read; edit when the user explicitly and specifically approves | touch otherwise (the user's Obsidian note templates) |
| staging/ | read; move items into notes/ or sources/inbox/ when the user directs an import batch | touch otherwise (un-imported material awaiting the user's triage) |
| meta/cookbook/ | read; draft and edit recipes when the user directs (folder law in its README) | sweep, ingest, cite as evidence, or index anything here (opt-in program recipes, not vault knowledge) |
| CLAUDE.md, .claude/skills/ | propose changes via the `amend` skill | edit directly |
| .state/ | pipeline bookkeeping via skills; issue files any time | anything else |

**The single-pipeline rule:** knowledge enters the wiki only through sources/inbox/, the notes/ sweep, or a skill. If you're about to write a wiki page and you're not inside a skill procedure, stop. Route it through inbox/ or invoke the skill. Claim-neutral edits the user directs in chat (style, structure, formatting, link fixes that change no claim) are not knowledge entering the wiki. Apply them directly on the user's in-chat approval and log one line in the day log.

## Reading wiki pages — status weighting

Every wiki page's frontmatter carries `status`. Weight what you read accordingly:

- `verified` — treat as ground truth.
- `draft` — treat as hypothesis. Usable, but say so when it materially affects an answer.
- `stale` — re-verify before relying on it.
- `disputed` — do not build on it, and mention the dispute if relevant.
- A page flagged `pending_review: true` has a verified core, but content under "Unreviewed additions" headings is draft-grade. Weight those sections as `draft`.

Most pages are drafts. That is normal and by design, not a defect to fix.

## Page scoping

A wiki page holds one subject, evidenced, singly-homed. Three tests define well-scoped: the `description` honestly predicts the whole body (retrieval); a new fact about the subject has exactly one obvious home (filing); the contents rot at the same rate and from the same cause, so page-level status stays meaningful (trust). Every wiki page carries a `scope:` frontmatter field, its boundary contract (meaning in GLOSSARY.md; field law in ingest). A claim lives on one page. Other pages cite it, never restate it. When a test fails, route the fix through `ingest`, which owns the split and scope operations. Never fork a second page on a subject that already has one.

## When the user's request conflicts with these rules

The user is not expected to know these rules. You are. In order:

1. **Translate.** Most conflicts are phrasing. "Fix that wiki page" → the correction flow below. "Remember this" → write it to sources/inbox/. "Link my note to X" → `related:` write-back on the note (per process-inbox) or the wiki-side link. Do what they meant via the conforming path, and say in one line which mechanism you used.
2. **Surface true conflicts.** If the intent itself breaks a rule, name the rule and its reason in one sentence, then offer the conforming alternative and the override.
3. **Overrides are the user's right.** If they confirm, comply, and record the exception in the day log, wiki/log/<YYYY-MM-DD>.md (what, why). Never silently comply, never silently reinterpret, never refuse.

## Corrections

When the user says something in the vault is wrong (a wiki claim, a session summary, anything), do not hand-edit the page. Write their correction as a new file in sources/inbox/ with provenance `"the user, <date>"`. Ingestion reconciles the affected pages. The user's statement is itself a source.

## This system is young — you are also its tester

These rules are under active development and not yet stress-tested. If a rule is ambiguous, fights the task at hand, or a situation arises that nothing here anticipates, handle the immediate task conservatively (when in doubt, ask the user), then file an issue (one file in .state/issues/, per the convention in ISSUES.md at the vault root): what happened, which rule, what you did. No format ceremony. A flag that takes effort won't get filed. The digest surfaces open issues to the user and they drive rule changes. When no rule pins a call down and you decide by judgment, log one line in the day log beginning `Judgment:` with the call, the reasoning, and the intent evidence relied on. Interactive sessions included. The digest sweeps these for the user to confirm or correct.

## Skills — invoke, don't improvise (in .claude/skills/)

`ingest` (source → wiki pages) · `process-inbox` (drain inbox + sweep notes) · `session-capture` (preserve a session's knowledge) · `query` (answer from the vault, with citations) · `lint` (health checks) · `digest` (review surface for the user) · `audit-exocortex` (one-page-at-a-time review loop) · `vault-snapshot` (backup) · `amend` (change the rules/skills, with the user's approval) · `update-exocortex` (pull upstream program updates into this vault, inert for the program's source vault)

If a task matches a skill, use the skill. If no skill fits and the task touches wiki/ or sources/, ask the user rather than improvising a write path.

## Imported at session start

@CONSTITUTION.md
