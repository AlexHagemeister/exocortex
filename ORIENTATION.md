---
updated: 2026-08-06 Thu, Aug 6 — 11:54 PM
---
# ORIENTATION — what you can ask for

This page is the tour of your maintainer's capability surface. Keep it; nothing here needs memorizing. Every skill answers to plain words or to its slash command (`/digest` and "what needs my review" reach the same procedure), and asking "what can you do?" in any vault session re-opens this tour.

## The daily loop

- **Capture.** Drop any markdown file into `sources/inbox/`, clip from your browser, or say "remember this: …" mid-conversation. Provenance is recorded at capture time.
- **Compile.** "Process my inbox" (`process-inbox`) files captures, sweeps your notes for changes, and compiles draft wiki pages. Works run by hand or on a schedule.
- **Ask.** "What do you know about X?" (`query`) answers from your vault, citing pages and sources, weighted by how verified each claim is.

## The habit that matters: review

"What needs my review" (`digest`) compiles your review surface: new connections, disputes the maintainer found, drafts ready to promote. Skim it, correct what's wrong (a correction is one sentence to the maintainer), promote what's solid. Promoting a page to `verified` is deliberately yours alone.

Run it as often as you feel like. Daily is normal when a lot is flowing in (an early migration, a busy stretch); weekly suits a settled vault. The cadence is yours. The experience is the core of the system: this is where the wiki becomes something you trust. Run it by hand at first; once you know your rhythm, ask to schedule it.

## When something is off

- **Corrections.** Say "that's wrong, actually …". Your statement enters as a new source and the affected pages reconcile. Nothing is hand-edited.
- **Health checks.** `lint` finds contradictions, staleness, and broken structure. Usually scheduled; on demand anytime.
- **Rule changes.** If anything chafes, say so. The `amend` skill proposes a concrete change, you approve it, and it's logged. The rules are yours to renegotiate.

## Keeping and growing

- **"Capture this session"** (`session-capture`) preserves a conversation's decisions and reasoning before it evaporates.
- **"Let's audit"** (`audit-exocortex`) reviews recent wiki pages with you, one page at a time.
- **`vault-snapshot`** commits vault history to your private remote. Usually scheduled; run it before anything risky.
- **"Update my exocortex"** (`update-exocortex`) checks for program releases, shows what changed, asks before applying, and then introduces what the update lets you do.

## What's possible later: the cookbook

`meta/cookbook/` is a library of opt-in recipes: connectors (calendar, email), capture tools, a phone-reachable vault server, and workflows that earned their place in real use. Nothing in it runs until you opt in. Browse the folder, or ask "what else can this do?" anytime.
