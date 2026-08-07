---
name: top-of-mind-file
what: One co-maintained file indexing what's currently active in the user's life, so every session starts already oriented
type: workflow
requires: nothing beyond the vault itself
effort: ~15 minutes to draft the first version; a minute per update after
suggest_when: the user re-explains their current situation at the start of a session, or asks "what should I be working on?" and the agent has to reconstruct the answer from scratch
status: recommended
---

# Top-of-mind file: standing orientation

This one is pure workflow: no tool, no account, no deployment. It is a single markdown file at `artifacts/top-of-mind.md` that indexes what is currently active in the user's life, highest priority first. The agent reads it at the start of any planning or life-admin session and updates it with the user as priorities move. It exists because the alternative is the re-orientation tax: every fresh session spending its first ten minutes rebuilding context the last session already had.

## Why this is here

The wiki holds knowledge, the task system holds tasks, the calendar holds events; none of them holds *salience*. What deserves attention right now, what is blocked on what, which deadline actually matters this week: that picture lived only in the user's head, and re-explaining it was the cost of every new conversation. In the source vault this file became the fix: a deadline with its open items and a link to the full board, an errand with its one known trap, an upcoming appointment with what it costs and what to bring. Sessions start with the agent already knowing the terrain, and the user talking about the work instead of describing it.

The design rule that makes it work: **it is an index, not a store**. Every entry is a few lines of what-and-why plus a link to where the substance lives (a wiki project page, a source, an external doc). Tasks stay in the task system, events in the calendar, knowledge in the wiki. The moment content gets pasted in rather than pointed at, the file starts rotting into a second, worse copy of everything.

## What you'll end up with

- One file, `artifacts/top-of-mind.md`, with a dated `updated:` stamp and priority-tiered sections. The proven set: **Do now** (active, deadline-bearing), **Do when the moment comes** (waiting on a trigger, listed so they don't vanish), **Coming up** (dated things approaching, with logistics), **Keep in mind** (background state worth carrying).
- A header line declaring the index rule and where each kind of thing actually lives, so any agent reading it knows not to treat it as a task list.
- Sessions that begin oriented: the agent consults the file, says it did, and gets to work.

## Setup

Agent-driven, in one conversation:
1. Interview the user briefly: what has a deadline, what is waiting on a trigger, what is coming up with logistics attached, what background state should every session know. Ten minutes of talking is enough for the first draft.
2. Write `artifacts/top-of-mind.md` with the four sections above, each entry a bolded headline, a line or two of the why and the trap, and a link to where the substance lives. Stamp `updated:` with the date at the top, under a header note stating the index rule.
3. Agree on the maintenance habit: the agent proposes updates whenever a session changes the picture (something ships, a date lands, a priority flips), and the user's yes applies them. The `updated:` stamp is the honesty mechanism: a stale date means verify before trusting the contents.
4. The file lives in artifacts/ deliberately: it is a co-built work product, never swept or ingested, and claims in it carry no evidential weight. It orients; the wiki proves.

## Verify it works

Open a fresh session and ask "what should I be focused on?" The agent should consult the file, say so, and answer from it in seconds, with links that actually resolve. If the answer matches your reality, it works. When it stops matching, that's not failure, that's the update trigger.
