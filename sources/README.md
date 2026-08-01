---
updated: 2026-07-30 Thu, Jul 30 — 10:15 PM
---
# sources/ — frozen records of what was said

The vault's evidence layer. Everything here is a record of speech — what someone said, wrote, published, or exported — never a truth claim. Truth-status lives one layer up, in the wiki, where claims carry status and can be disputed without falsifying the record. <!-- constitution: principle 2, freeze speech -->

How this folder works:

- **[inbox/](inbox/README.md)** is the single entry point. Items there are pre-pipeline and freely editable; the freeze happens when `ingest` files them into a stream.
- **Streams** are the permanent subfolders — [articles/](articles/README.md), [sessions/](sessions/README.md), [meetings/](meetings/README.md), [life/](life/README.md) — each with a README declaring its evidential modality: what kind of claim its contents can support. Read the stream README before filing into it; a filed item may carry its own `modality:` frontmatter when the stream default would mislabel it (rule: `.claude/skills/ingest/` step 2).
- **Filed means frozen.** Never edit or delete a filed source. Corrections arrive as new speech: a new file through inbox/, reconciled by ingest.
- Each stream's `index.md` is derived; the pipeline regenerates it.

New top-level streams are the user's call — a stream carries evidential semantics, not just taxonomy.

Zone row authority: CLAUDE.md. This README is the folder law that row points agents to read.
