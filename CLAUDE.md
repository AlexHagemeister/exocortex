---
updated: 2026-07-20 Mon, Jul 20 — 9:30 PM
---
# CLAUDE.md — Vault Operating Rules

This vault is the user's knowledge system: an agent-maintained wiki compiled from their sources and notes. You are reading its core rules. Everything here binds you on every turn. Folder-specific rules live in each folder's README.md — read the README of any folder before writing to it. Skill procedures live in .claude/skills/. Principles live in CONSTITUTION.md — read it at session start, before other vault work; when no rule anticipates a case, reason from the principles. When a system term is ambiguous, or when amending vocabulary, read GLOSSARY.md — do not paste definitions here. When using a term the user may not know, give the one-liner once or point at the entry. If meta/DEPLOYMENT.md has a `## Voice` section, adopt it — it governs tone only, never the epistemic rules: status labels, provenance, disputes, and corrections stay plain.

## Zones — who writes where

| Zone | You may | You may not |
|---|---|---|
| sources/ | add files to sources/inbox/; file inbox items to stream folders during ingest | edit or delete anything already filed — sources are frozen records of what was said, not truth claims |
| wiki/ | create and edit pages, **only via the skills** | write directly outside a skill procedure |
| notes/ | read, link to, ingest from; sweep write-back of frontmatter metadata — additive only, pointers to existing wiki pages (rules in process-inbox) | touch note bodies, or edit/delete anything the user wrote — the words are the user's alone |
| attachments/ | read, embed-link; move/rename/delete when the user explicitly and specifically approves | touch files otherwise — the user's media; Obsidian files new attachments here |
| templates/ | read; edit when the user explicitly and specifically approves | touch otherwise — the user's Obsidian note templates |
| CLAUDE.md, .claude/skills/ | propose changes via the `amend` skill | edit directly |
| .state/ | pipeline bookkeeping via skills | anything else |

**The single-pipeline rule:** knowledge enters the wiki only through sources/inbox/, the notes/ sweep, or a skill. If you're about to write a wiki page and you're not inside a skill procedure, stop — route it through inbox/ or invoke the skill.

## Reading wiki pages — status weighting

Every wiki page's frontmatter carries `status`. Weight what you read accordingly:

- `verified` — treat as ground truth.
- `draft` — treat as hypothesis. Usable, but say so when it materially affects an answer.
- `stale` — re-verify before relying on it.
- `disputed` — do not build on it; mention the dispute if relevant.
- A page flagged `pending_review: true`: its core is verified, but content under "Unreviewed additions" headings is draft-grade — weight those sections as `draft`.

Most pages are drafts. That is normal and by design, not a defect to fix.

## When the user's request conflicts with these rules

The user is not expected to know these rules; you are. In order:

1. **Translate.** Most conflicts are phrasing. "Fix that wiki page" → the correction flow below. "Remember this" → write it to sources/inbox/. "Link my note to X" → `related:` write-back on the note (per process-inbox) or the wiki-side link. Do what they meant via the conforming path, and say in one line which mechanism you used.
2. **Surface true conflicts.** If the intent itself breaks a rule, name the rule and its reason in one sentence, then offer the conforming alternative and the override.
3. **Overrides are the user's right.** If they confirm, comply — and record the exception in the day log, wiki/log/<YYYY-MM-DD>.md (what, why). Never silently comply, never silently reinterpret, never refuse.

## Corrections

When the user says something in the vault is wrong — a wiki claim, a session summary, anything — do not hand-edit the page. Write their correction as a new file in sources/inbox/ with provenance `"the user, <date>"`. Ingestion reconciles the affected pages. The user's statement is itself a source.

## This system is young — you are also its tester

These rules are under active development and not yet stress-tested. If a rule is ambiguous, fights the task at hand, or a situation arises that nothing here anticipates: handle the immediate task conservatively (when in doubt, ask the user), then file an issue (one file in .state/issues/, per the convention in ISSUES.md at the vault root) — what happened, which rule, what you did. No format ceremony; a flag that takes effort won't get filed. The digest surfaces open issues to the user and they drive rule changes.

## Skills (in .claude/skills/ — invoke, don't improvise)

`ingest` (source → wiki pages) · `process-inbox` (drain inbox + sweep notes) · `session-capture` (preserve a session's knowledge) · `query` (answer from the vault, with citations) · `lint` (health checks) · `digest` (review surface for the user) · `vault-snapshot` (backup) · `amend` (change the rules/skills, with the user's approval) · `publish-program` (sync system files to the public repo, user-reviewed)

If a task matches a skill, use the skill. If no skill fits and the task touches wiki/ or sources/, ask the user rather than improvising a write path.
