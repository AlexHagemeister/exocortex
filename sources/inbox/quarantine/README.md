---
type: Meta
title: Quarantine — rejected captures
description: Captures that failed ingest validation, awaiting the user.
status: draft
updated: 2026-07-20 Mon, Jul 20 — 1:18 PM
---

Items land here when ingest's validation gate rejects them (empty, truncated, or junk content), with the reason logged in the day log (`wiki/log/<YYYY-MM-DD>.md`). They await the user's decision: re-clip, fix and move back to inbox/, or delete. The pipeline never ingests from this folder.
