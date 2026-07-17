---
name: ingest
description: Turn a source into wiki pages — validate, file, summarize, update related concepts. Use when processing an item from sources/inbox/, a notes/ delta handed over by process-inbox, or when the user says "ingest this", "add this to the wiki", or asks you to remember content they provide.
---

# Ingest — source → wiki

You are turning one source item into durable wiki knowledge. Input is one of: a file in `sources/inbox/`, a new-or-changed note delta from the notes sweep, or a correction statement from the user (which becomes an inbox file first). Read the README of every folder you write to before writing — folder-local rules live there.

## Procedure

### 1. Validate (gate before anything else)

Reject items that are empty, truncated mid-content, or junk (boilerplate-only clips, error pages, binary noise). Rejected inbox items → move to `sources/inbox/quarantine/` and log one line in the day log (`wiki/log/<YYYY-MM-DD>.md`) with the reason. The gate applies no matter which tool captured the item — the inbox is multi-tenant.

Then dedup: compute the content hash (`shasum -a 256`) and check it against the ledger `.state/ingest-hashes.txt` (one `<hash>  <filed path>` per line; create if missing). Already ingested → delete the duplicate inbox item, log it, stop.

Note deltas skip quarantine (notes/ is the user's zone — never move a note or touch its body); if a note delta is unusable, skip it and log why.

### 2. File (freeze happens here)

Move the inbox item to its permanent stream folder — `sources/articles/` (external material), `sources/sessions/` (session captures), `sources/life/` (personal exports) — choosing by the stream READMEs. Use a stable, descriptive, date-prefixed filename (`2026-07-16-title-slug.md`); this path is cited forever.

**File before you cite.** Provenance always references the final path. Before filing, inbox items are freely editable; after filing, the source is frozen — never edit or delete it, because a source records what was said, not what's true. Append the new hash to the ledger.

Notes are never filed — they stay in `notes/`, and you cite `notes/<path>` **plus the timestamp you read it** (mutability for the user, pinned provenance for the wiki).

### 3. Read under the stream's modality

Read the source in full. Honor the stream README's declared evidential semantics — they bound what kind of claim the source can support (e.g., a calendar entry evidences intention, never occurrence; a session summary is paraphrase of what was said, not what's true).

If this is an interactive session, briefly discuss takeaways with the user before writing — what seems important, what connects to existing pages.

### 4. Write the source-summary page

One wiki page distilling the source, in the appropriate `wiki/` topic folder (check `wiki/index.md`; if no folder fits, ask the user — new top-level folders are the user's call, because a path is an identity and renames break links). Fill this template:

```yaml
---
type: Source summary
title: <source title>
description: <one sentence>
tags: []
timestamp: <now, ISO 8601>
status: draft
verified_at:
depends_on: []
sources: ["<final filed path, or notes/<path> + read timestamp, or URL>"]
---
```

**YAML discipline**: double-quote any frontmatter value containing `": "` (colon-space) or starting with a special character — an unquoted colon silently breaks the mapping and the page stops rendering in Obsidian.

Body sections — keep observation and inference under separate headings, always: <!-- constitution: laundered inference -->

```markdown
# What the source says

<claims, attributed per the stream's modality>

# What we conclude

<your inferences, explicitly marked as inference>
```

### 5. Update related concept pages (5–15)

Find existing wiki pages the source bears on (start from `wiki/index.md`, drill via links) and update them; create new concept pages where a red link or a clear gap exists. Every page write follows the same rules:

- Same frontmatter template as above, with `type: Concept` (or another descriptive type).
- **`status: draft`, always.** Sole exception: a claim quoting the user **verbatim** is born `verified` (set `verified_at`). Paraphrases are NOT — paraphrase is where misstatement lives.
- **No claim without provenance.** Every substantive claim traces to a `sources:` entry or is explicitly marked as your inference. Never write a guess with the typography of a fact.
- **Standard markdown links only, file-relative paths** (same folder: `[orders](orders.md)`; other folder: `[orders](../concepts/orders.md)`) — never wikilinks, and never leading-slash paths: Obsidian resolves `/...` from the vault root, not the bundle root, so those links are dead in the viewer and clicking them spawns phantom files. File-relative is OKF-legal (spec §5.2). Dangling links are legal and useful: red links are the backlog of known-missing knowledge.
- `depends_on:` lists the concept paths this page's claims rest on.

**Adding to an existing `status: verified` page** (staged-sections convention): never edit the verified core prose — new material appends under a dated heading `## Unreviewed additions (YYYY-MM-DD)` (multiple dated sections may accumulate), each claim with provenance, and you set `pending_review: true` in the frontmatter. The page-level `verified` then means "the reviewed core is verified"; annex content is draft-grade until the user confirms it (digest merges it into the core and clears the flag). If annex material *contradicts* the verified core, flag the contradiction inside the annex and let it queue for the digest — never auto-dispute the page. Sole exception to core immutability: the correction flow — a correction from the user (provenance "the user, <date>") authorizes rewriting the core directly. Draft pages need none of this; edit them freely.

### 6. Connections

If the source reveals a substantive insight that two things relate (beyond a note merely mentioning a known entity — those are ordinary links), create a page in `wiki/connections/` per that folder's README. Never write links into note bodies — navigational `related:`/tag pointers in note frontmatter are the sweep's write-back (per process-inbox), not ingest's; backlinks surface wiki-side links on the note automatically.

### 7. Close out

- Regenerate `index.md` in every folder you touched — source-stream folders you filed into count as touched (derived files: sections of `* [Title](path) - description` lines pulled from frontmatter; regenerate freely, never hand-maintain).
- Append one entry per action to today's day log, `wiki/log/<YYYY-MM-DD>.md` (create it if missing; newest-first `* **Update**: …` lines; log.md indexes the day files).

## Corrections (when the source is the user's statement)

A correction file (provenance `"the user, <date>"`) reconciles rather than adds: locate every wiki page citing the corrected claim (grep `sources:` and body), rewrite the affected claims citing the correction, and leave the superseded source in place — it stays as historical record; the wiki layer outweighs it. A verbatim correction from the user is born `verified`. If a claim is withdrawn entirely, re-examine pages listing it in `depends_on` or linking to it — never retract silently.

## Don'ts

- **Laundered inference** — a guess written as a fact. Status fields and the observation/inference split exist to prevent it.
- **Promiscuous capture** — never pull in external content the user didn't deliberately capture. (notes/ and life exports are exempt: the user's own speech and scheduled personal exports are pre-curated by definition.)
- **Never edit a filed source, ever** — corrections arrive as new sources.
