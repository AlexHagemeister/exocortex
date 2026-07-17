---
name: session-capture
description: Preserve the current session's durable knowledge as an inbox source. Use when the user says "capture this session", "save this conversation", or wants the decisions, facts, or reasoning from this chat kept in the vault.
---

# Session capture — preserve what this session produced

You are writing a source, not wiki pages — the capture goes to `sources/inbox/` and ingestion turns it into knowledge later (or immediately, if the user asks). The user triggers this deliberately; most sessions are not worth capturing, so never capture unprompted. Read the README of any folder you write to.

## Procedure

1. **Select the durable knowledge**: decisions made, facts established, reasoning worth keeping, open questions. Leave out the mechanics (tool calls, dead ends) unless the path itself was the insight.

2. **Quote pivotal exchanges verbatim.** Where the user stated something important, quote their exact words, marked as a quote with speaker and rough position ("early in session"). One-line why: verbatim user speech can be born `verified` downstream; your paraphrase cannot — paraphrase is where misstatement lives. Summarize the rest as reported speech ("we discussed…", "the user asked…"), never as flat fact — a capture records what was said, not what's true.

3. **Write one file** to `sources/inbox/<YYYY-MM-DD>-session-<topic-slug>.md`:

```yaml
---
type: Session capture
title: <session topic>
description: <one sentence>
timestamp: <now, ISO 8601>
provenance: "session with the user, <date>, <surface if known>"
---
```

Body: summary first, then a `# Verbatim quotes` section, then `# Open questions` if any.

4. Tell the user it's in the inbox and will enter the wiki on the next ingest — or run `ingest` now if they want it immediately.

Inbox items are pre-pipeline: the user may edit the capture freely until it's filed. If the user later says a filed capture misstated something, their correction enters the inbox as a new source — the filed capture is never edited.
