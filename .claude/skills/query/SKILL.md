---
name: query
scope: "Answering questions from the vault: status-weighted retrieval, cited synthesis with draft write-back, query-traffic recording, and flow-of-use promotion on explicit confirmation. Corrections route through sources/inbox/ for ingest, and ranked promotion triage lives in digest."
description: Answer a question from the vault with status-weighted citations. Use when the user asks what the vault knows, asks a question the wiki might answer, or wants a synthesis across notes, sources, and wiki pages.
---

# Query — answer from the vault

You are answering from the vault's compiled knowledge, weighting every page by its trust status. Read the README of any folder you write to.

## Procedure

### 1. Navigate index-first

Start at `wiki/index.md`, drill down via links (folder indexes → pages). Indexes exist so you can see what's available before opening files. Prefer them over blind directory searches, and fall back to grep only when the indexes come up empty. `sources/` and `notes/` are readable too, but the wiki is the synthesis layer. Cite wiki pages first, raw sources for detail.

If the vault comes up empty and the question concerns past work with the agent, check the session's tool roster for a transcript-search surface (Claude Code desktop, for example, exposes session-management tools that full-text search past session transcripts) and search it before asking the user or reporting the matter unrecorded. A transcript is a raw record of what was said. Cite it like a source, but never ingest from it directly. If what it yields is durable knowledge, route it through session-capture or sources/inbox/ so it enters the wiki through the pipeline.

### 2. Weight by status

Weight and disclose every page per the status ladder in CLAUDE.md ("Reading wiki pages — status weighting"), the rule's one home, always in context. It covers `pending_review` annexes too. When a non-`verified` page materially shapes the answer, the disclosure goes in the answer itself ("per a draft page, …").

### 3. Synthesize with citations

Answer, citing the pages (and where useful, the underlying sources) each claim rests on. Distinguish what pages state from what you are inferring across them. Never blend a guess into cited fact. <!-- constitution: laundered inference -->

When an answer or recommendation turns on a recently filed source (this session, or the last few days), **re-read the filed file** before relying on your working memory of it. Extraction is not weighting, and the failure mode is recommending against a fact you personally wrote down. If that source holds a negative record about the entity you're recommending on (a withdrawal, a dropped commitment, a stated constraint), surface it explicitly, even to say it was considered and judged non-blocking. Silence is indistinguishable from having missed it.

On long multi-page syntheses, place the fetched content above the question in any context you assemble, and quote the passages the answer rests on before reasoning over them. Both measurably improve long-context accuracy.

### 4. Write good answers back

If the answer required real synthesis (connected pages, resolved something, filled a gap), file it into the wiki as a new page so explorations compound, with `status: draft`, standard markdown links, and provenance listing every page and source used:

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

Place it in a topic folder (usually `wiki/concepts/`), per `wiki/index.md`, and **never in `wiki/connections/`**. That folder is for `type: Connection` pages only (atomic relationship claims between two endpoints, which carry an expiry lifecycle), and a Synthesis answering the user's question is neither an atomic relationship claim nor expirable. Regenerate the touched folder's index, and log one line in the day log (`wiki/log/<YYYY-MM-DD>.md`). Skip write-back for lookups that added nothing beyond what one page already says.

### 5. Record draft citations

Append the paths of draft pages your answer materially relied on to `.state/query-traffic.txt` (one `<date>  <path>` per line). The digest ranks promotion candidates partly by query traffic. This is how used knowledge gets verified fastest.

## Flow-of-use promotion (the one promotion path in this skill)

If the user **explicitly confirms** a specific cited claim ("yes, that's right", "confirmed"), that is a review event:

1. Set that page's `status: verified` and `verified_at: <now>`.
2. Add to its `sources:`: `"user confirmed in session, <date>"`.
3. Log the promotion in the day log (`wiki/log/<YYYY-MM-DD>.md`).

**Politeness is not assent.** "Thanks!", "great answer", or moving on confirms nothing. The trust ledger records explicit assent only. When unsure whether a reply was confirmation, ask. If the user *corrects* a claim instead, route it as a correction: write their statement to `sources/inbox/` with provenance `"the user, <date>"` and say you've done so. Ingestion reconciles the pages.
