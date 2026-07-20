---
name: query
description: Answer a question from the vault with status-weighted citations. Use when the user asks what the vault knows, asks a question the wiki might answer, or wants a synthesis across notes, sources, and wiki pages.
---

# Query — answer from the vault

You are answering from the vault's compiled knowledge, weighting every page by its trust status. Read the README of any folder you write to.

## Procedure

### 1. Navigate index-first

Start at `wiki/index.md`, drill down via links (folder indexes → pages). Indexes exist so you can see what's available before opening files — prefer them over blind directory searches; fall back to grep only when the indexes come up empty. `sources/` and `notes/` are readable too, but the wiki is the synthesis layer — cite wiki pages first, raw sources for detail.

### 2. Weight by status

Weight and disclose every page per the status ladder in CLAUDE.md ("Reading wiki pages — status weighting") — the rule's one home, always in context; it covers `pending_review` annexes too. When a non-`verified` page materially shapes the answer, the disclosure goes in the answer itself ("per a draft page, …").

### 3. Synthesize with citations

Answer, citing the pages (and where useful, the underlying sources) each claim rests on. Distinguish what pages state from what you are inferring across them — never blend a guess into cited fact. <!-- constitution: laundered inference -->

### 4. Write good answers back

If the answer required real synthesis (connected pages, resolved something, filled a gap), file it into the wiki as a new page so explorations compound — `status: draft`, standard markdown links, provenance listing every page and source used:

```yaml
---
type: Synthesis
title: <question, as a topic>
description: <one sentence>
tags: []
timestamp: <now, ISO 8601>
status: draft
verified_at:
depends_on: [<concept paths the answer rests on>]
sources: [<pages and sources cited>]
---
```

Place it in a topic folder (usually `wiki/concepts/`), per `wiki/index.md` — **never in `wiki/connections/`**: that folder is for `type: Connection` pages only (atomic relationship claims between two endpoints, which carry an expiry lifecycle), and a Synthesis answering the user's question is neither noise nor expirable. Regenerate the touched folder's index; log one line in the day log (`wiki/log/<YYYY-MM-DD>.md`). Skip write-back for lookups that added nothing beyond what one page already says.

### 5. Record draft citations

Append the paths of draft pages your answer materially relied on to `.state/query-traffic.txt` (one `<date>  <path>` per line). The weekly digest ranks promotion candidates partly by query traffic — this is how used knowledge gets verified fastest.

## Flow-of-use promotion (the one promotion path in this skill)

If the user **explicitly confirms** a specific cited claim ("yes, that's right", "confirmed") — that is a review event:

1. Set that page's `status: verified` and `verified_at: <now>`.
2. Add to its `sources:`: `"user confirmed in session, <date>"`.
3. Log the promotion in the day log (`wiki/log/<YYYY-MM-DD>.md`).

**Politeness is not assent.** "Thanks!", "great answer", or moving on confirms nothing — the trust ledger records explicit assent only. When unsure whether a reply was confirmation, ask. If the user *corrects* a claim instead, route it as a correction: write their statement to `sources/inbox/` with provenance `"the user, <date>"` and say you've done so — ingestion reconciles the pages.
