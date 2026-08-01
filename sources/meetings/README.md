---
type: Meta
title: Meetings stream — recorded conversation transcripts
description: Meeting transcripts filed here permanently by ingest; machine-transcribed speech, weighted by speaker.
status: draft
---

# What this folder is

The permanent home for meeting transcripts — recordings of real-world conversations (work syncs, vendor calls, conference debriefs), captured by a transcription tool (currently Granola) and moved here from inbox/ by `ingest`.

# Rules

- **Frozen once filed.** Never edit a filed transcript. Corrections enter inbox/ as new sources; the superseded record remains as history.
- Filename carries date + counterpart (`2026-06-30-client-sync.md`, `2026-07-14-vendor-call.md`); each file opens with a provenance block (date, participants, capture tool) so the record is self-describing.
- [index.md](index.md) is derived; the pipeline regenerates it.

# Evidential modality

A transcript is a **machine-transcribed record of what was spoken** — closer to verbatim than a session capture, but transcription errs on wording, names, and speaker attribution, so no claim is born `verified` from a transcript alone. Weight claims by **speaker**, not by file:

- **The user's own recorded speech**: his statement, near-verbatim — but transcription noise means claims built on it land `draft` until he confirms the wording.
- **Principals** (e.g. the project counterpart he reports to): evidence of direction, decisions, and commitments — as reported speech.
- **Interested parties** (vendors, salespeople, anyone pitching): evidence only that the party said it. Self-descriptions are sales claims; corroboration comes from outside evidence, never from the pitch itself.
- A transcript evidences what was said in the meeting — never that the content is true.
