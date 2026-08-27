---
name: chronicle
what: An agent-compiled daily record of your days in wiki/chronicle/ — evidence first, inference marked, the agent's read last — with weekly roll-ups
type: workflow
requires: the vault itself; a scheduled maintenance chain to run it in (SETUP.md § 6); optional external connectors (calendar, email, messages) widen the evidence
effort: 20 minutes — create the folder from the shipped law, author your surface registry, add one step to your maintenance chain
suggest_when: the user asks "what did I do last Tuesday?" and the vault has no answer, or wants a durable record of their days that no single tool holds
status: experimental
---

# Chronicle: the record of your days

The chronicle is a page per day in `wiki/chronicle/`, compiled retrospectively each morning by the `chronicle` skill (`.claude/skills/chronicle/SKILL.md`), with a weekly roll-up after each Sunday. It is the account of what **you** did, distinct from the day log (`wiki/log/`), which records what the pipeline did. Same dates, different books. Each entry has five fixed sections: what you reported, what the witnesses observed, the inferred shape of the day with every line citing its evidence, an honest coverage map of what the witnesses could not see, and the agent's own read of the day, plainly marked as its judgment.

## Why this is here

Grown in the source vault from 2026-08-08. What earned it: "what did I do last Tuesday?" became answerable in one page read instead of an archaeology dig across sessions, calendar, and git. The five-section structure keeps the record honest — evidence and inference never blend, and the coverage section says out loud what the day's record is blind to. Entries are living pages: late-arriving evidence lands as dated additions, so the compile-time record and later enrichment stay distinguishable. The larger unlock is a memory brain with provenance: a diary the agent writes from receipts, that neither flatters nor invents.

The boundary that makes it safe: chronicle entries are **never a citation target**. Wiki claims cite the underlying sources the entries themselves cite. The record orients; it does not testify.

## What you'll end up with

- `wiki/chronicle/` with one page per day (04:00-to-04:00 boundary), named `YYYY-MM-DD-<weekday>.md`, plus `YYYY-MM-DD-week.md` roll-ups dated by the closing Sunday, and a derived index. Folder law ships in `wiki/chronicle/README.md`.
- A morning step in your maintenance chain that compiles yesterday before you ask, gated so it never runs against an undrained inbox.
- Answers to "what was I doing on <date>?" grounded in cited evidence, with the agent's inference marked as inference.

## Setup

1. **Create the folder.** Make `wiki/chronicle/` — the shipped `wiki/chronicle/README.md` is its law (sections, naming, day boundary, frontmatter template, the never-cite rule). The skill regenerates `index.md` itself.
2. **Author your surface registry** at `meta/chronicle-surfaces.md`. Like DEPLOYMENT.md, every deployment writes its own: one row per witness surface (calendar, reminders, email, messages, meeting notes, desktop sessions — whatever connectors this deployment actually has), each with a capture brief and any boundary ("report-only" for surfaces that must never be quoted verbatim). The skill spawns one collector per `active` surface and treats the registry as law. Vault-internal witnesses (sessions, git, notes) need no registration. Activating a surface is the user's explicit yes, per surface.
3. **Add the step to your maintenance chain** (SETUP.md § 6), after the inbox drain: a delegated subagent executing the DAILY procedure of `.claude/skills/chronicle/SKILL.md`, and on Mondays the WEEKLY procedure after it. The skill's own intake gate re-checks the inbox state, so ordering mistakes fail safe.
4. **Agree on enrichment**: later evidence (a source that arrives at noon, your own correction) goes in as a dated addition via the skill, never a silent rewrite.

## Verify it works

The morning after setup, yesterday's page exists in `wiki/chronicle/`, all five sections present, the Coverage section names every registered surface (consulted or unreachable), and asking "what did I do yesterday?" gets answered from the entry with citations that resolve. If an entry ever appears as evidence in a wiki page citation, that is a defect — file it.
