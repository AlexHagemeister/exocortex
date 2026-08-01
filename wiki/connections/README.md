---
type: Meta
title: Connections — first-class relationship claims
description: Pages asserting that two things relate; the insight surface between notes, sources, and wiki.
status: draft
---

# What this folder is

A connection is a **claim that two things relate** — a note and a concept, two concepts, a source and a project. It gets a page, never a link appended to a note: page-hood gives the claim the full status lifecycle (promote, dispute, expire), and notes/ is never written to — backlinks make wiki-side links visible on the note for free.

Routine associations (a note merely mentions a known entity) do **not** belong here — ingest handles those as ordinary links on the relevant concept pages. This folder is for substantive insights: the relationship itself carries new information.

# Page template

```yaml
---
type: Connection
title: <endpoint A> ↔ <endpoint B>
description: <the relationship, in one sentence>
tags: []
timestamp: <ISO 8601>
status: draft
verified_at:
depends_on: []
sources: [<what surfaced this connection>]
---
```

Body: state the relationship and why it might matter, linking both endpoints with standard markdown links. Separate what was observed from what is inferred.

# Lifecycle

- Born `draft`, like every agent write. Promotion happens only via digest triage or explicit flow-of-use confirmation — the same bar as any claim.
- **Expiry:** `type: Connection` drafts expire if unpromoted; the policy and its clock live in the `lint` skill (check 7), keyed on the `type` field, not on this folder. Pages of other types are never expired — if one is found here, that's a filing error for the user to review, not a page to delete.
- The weekly digest lists new connection pages — discovery is push, so insights reach the user unprompted.
