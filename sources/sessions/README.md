---
type: Meta
title: Sessions stream — captured conversations
description: Session captures filed here permanently by ingest; agent paraphrase of what was said.
status: draft
---

# What this folder is

The permanent home for session captures — summaries of conversations the user chose to preserve (via the `session-capture` skill), moved here from inbox/ by `ingest`. Captures the user typed or dictated themselves (statements, phone notes, corrections) belong here too: a conversation of one, read under the verbatim tier below (the user's ruling, 2026-09-06; the sole fresh-install repro of the stream taxonomy, closed by this line rather than a new stream).

# Rules

- **Frozen once filed.** Never edit a filed capture. If the user says a capture misstated something, their correction enters inbox/ as a new source and ingestion reconciles the dependent pages — the superseded original remains as historical record.
- [index.md](index.md) is derived; the pipeline regenerates it.

# Evidential modality

A session capture is **agent paraphrase of what was said** — not what is true, and (outside marked verbatim quotes) not exactly what was said. Two tiers:

- **Verbatim quotes**, marked as quotes with a speaker: the user's actual words. Claims quoting the user verbatim may be born `verified` (trust inheritance).
- **Everything else**: paraphrase. Paraphrase is where misstatement lives — claims built on it land as `draft`, attributed as reported speech ("the user said…", "we discussed…").
