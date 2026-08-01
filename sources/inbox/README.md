---
type: Meta
title: Inbox — transient capture queue
description: Pre-pipeline drop zone; anything here is freely editable until ingest files it.
status: draft
---

# What this folder is

The single entry point for new knowledge: clipper drops, session captures, corrections, anything the user or another surface wants remembered. Any agent on any surface may **add** files here.

# Rules

- Items here are **pre-pipeline**: freely editable and deletable. The freeze happens at filing — when `ingest` moves an item to its permanent stream folder (articles/, sessions/, meetings/, life/), path and content become immutable.
- A correction from the user is a file here too, with provenance `"the user, <date>"` — the user's statement is itself a source.
- `quarantine/` holds captures that failed ingest validation (empty, truncated, junk). They await the user; the pipeline never reads that folder.
- Empty inbox = fully ingested. Nothing should live here long-term.
