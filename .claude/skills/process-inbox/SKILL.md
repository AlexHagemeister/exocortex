---
name: process-inbox
description: Drain sources/inbox/ and sweep notes/ for new or changed content. Run on schedule (daily-ish) or when the user asks to process captures, catch up the pipeline, or sweep notes.
---

# Process inbox — drain the queue, sweep the notes

Two passes: ingest everything waiting in the inbox, then diff `notes/` against the last sweep and ingest what changed. Read the README of any folder you write to. Success criterion: empty inbox, current cursor.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Acquire and release `.state/maintainer.lock` per the protocol in `.state/README.md` — first action and last action of the run. Cap the notes sweep at ~20 notes per run (prefer recent and substantive; the cursor carries the rest forward); decide conservatively, never wait for input, flag judgment calls in the log.

## Pass 1 — inbox

List `sources/inbox/`, excluding:

- `quarantine/` — rejected items awaiting the user; the pipeline never reads it.
- **Sync-conflict files** — filenames containing "conflicted copy", "Conflicted Copy", or a duplicate-suffix pattern (`name 2.md` alongside `name.md`). Sync layers spawn these silently; ingesting them makes the sync layer an unaudited source of divergent claims. Flag them in your report for the user instead.
- READMEs.

Run the `ingest` skill on each remaining item, oldest first. If a session is interactive and items need judgment calls (which stream, junk-or-not), ask; scheduled runs decide conservatively and log.

## Pass 2 — notes sweep

The cursor lives at `.state/notes-cursor.txt`: one line per known note — `<sha256>  <read-timestamp ISO 8601>  <path relative to notes/>`. Create it on first run.

1. Walk `notes/` recursively. OS artifacts (`.DS_Store`, `Thumbs.db`, `desktop.ini`) are invisible to the sweep — never walked, ingested, or carried in the cursor.
2. **Sync eviction is not deletion.** A sync-layer placeholder (e.g. `.<name>.icloud`) means the file is evicted but present — record it as "evicted, unchanged" and skip; never treat it as new, changed, or deleted. (None should appear on the current deployment — if one does, flag it to the user.)
3. Skip sync-conflict filenames (same patterns as above) — flag, don't ingest.
4. **Respect the opt-out:** any note carrying the `#no-ingest` tag (inline or in frontmatter `tags:` — check both) is skipped entirely. That tag is the user's only curation gate on this stream, in both directions: honor it absolutely, and never impose your own — untagged notes ingest regardless of subject matter.
5. For each new or changed file (hash differs from cursor): run `ingest` on the delta — cite `notes/<path>` plus the read timestamp. Then write back frontmatter metadata: `related:` wikilinks (tags where apt) to the wiki pages the note fed or clearly relates to; fill `description:` if blank and obvious. Additive only — never remove or reword user-authored values, point only at existing wiki pages, never touch the body. Notes are never moved or filed; the note stays live, the citation is pinned.
6. For each cursor entry whose file is gone (no file AND no sync placeholder): record the path in `.state/deleted-notes.txt`. Deletion is withdrawal — a speech act the wiki must hear; `lint` walks the consequences (claims resting solely on a deleted note demote to disputed). A sweep that finds a large share of the cursor deleted at once is almost certainly bugged, not right — stop and report instead of recording.
7. Rewrite the cursor with current hashes and read timestamps.

## Close out

Log one summary line in the day log (`wiki/log/<YYYY-MM-DD>.md`; items ingested, quarantined, notes swept, deletions recorded, conflicts flagged). Zero-friction is this stream's point — never ask the user to pre-sort notes or the inbox.
