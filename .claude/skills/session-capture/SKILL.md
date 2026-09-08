---
name: session-capture
scope: "Writing one session's durable knowledge as a single inbox source, verbatim quotes preserved. Wiki pages come later through ingest, and corrections to a filed capture arrive as new inbox sources, never edits."
description: Preserve the current session's durable knowledge as an inbox source. Use when the user says "capture this session", "save this conversation", or wants the decisions, facts, or reasoning from this chat kept in the vault.
---

# Session capture — preserve what this session produced

You are writing a source, not wiki pages. The capture goes to `sources/inbox/` and ingestion turns it into knowledge later (or immediately, if the user asks). The user triggers this deliberately, and you may also trigger it yourself when the session produced a decision, a ruling, or a durable fact that would otherwise be lost (the user's ruling, 2026-08-30, scoped 2026-08-31). An unprompted capture must be announced in the session before it ends ("captured this to the inbox"), so the user can veto on the spot. Most sessions are still not worth capturing. Read the README of any folder you write to.

## Procedure

1. **Select the durable knowledge**: decisions made, facts established, reasoning worth keeping, open questions. Leave out the mechanics (tool calls, dead ends) unless the path itself was the insight.

2. **Quote pivotal exchanges verbatim.** Where the user stated something important, quote their exact words, marked as a quote with speaker and rough position ("early in session"). One-line why: a verbatim user verdict, ruling, or correction can be born `verified` downstream (other verbatim speech is born draft, but only verbatim carries the user's authority at all). Your paraphrase cannot, because paraphrase is where misstatement lives. Summarize the rest as reported speech ("we discussed…", "the user asked…"), never as flat fact. A capture records what was said, not what's true. A commitment voiced in the record ("I'll send that now") is written as committed, never as done, because the record ends before the action would occur.

3. **Write one file** to `sources/inbox/<YYYY-MM-DD>-session-<topic-slug>.md`:

```yaml
---
type: Session capture
title: <session topic>
description: <one sentence>
timestamp: <now, ISO 8601>
provenance: "session with the user, <date>, <surface if known>"
session_id: <the harness session id, or omit the field if none is exposed>
---
```

`session_id` is the pointer back to the full transcript, for a later agent that needs more than the capture kept. Record it when the harness exposes it (on this deployment the register hook prints it every turn). The surface named in `provenance` says where that id resolves: a Claude Code id is a transcript file under `~/.claude/projects/`, and a chat-app id is not. Never guess an id. Omit the field rather than fabricate one. (Amendment 2026-09-03.)

Body: summary first, then a `# Verbatim quotes` section, then `# Open questions` if any. Name a sibling capture written in the same session by its basename wikilink (`[[2026-08-28-spaced-repetition-decks-trial]]`), never by its `sources/inbox/` path. Filing changes a capture's path and not its name, and a filed source is frozen, so an inbox path written now is a dead pointer the moment either file is filed.

4. **Add an ingest brief when the session had wiki pages in play.** End the capture with an `# Ingest brief` section, written while you still hold the routing knowledge: which wiki pages were read or discussed this session, which claims on which page this capture supersedes or extends (one line per page), and whether anything warrants a new page (proposed name, home folder, one-line scope). Head it `*Agent routing notes, <date>: a recommendation to ingest, not a claim about the world.*` Never name a page you didn't actually have in context; a guessed route is worse than none. Skip the section entirely when the session touched no existing pages.

5. Tell the user it's in the inbox and will enter the wiki on the next ingest, or run `ingest` now if they want it immediately (a capture with an ingest brief is cheap to ingest on the spot or delegate to a subagent, since the routing is already written).

Inbox items are pre-pipeline, so the user may edit the capture freely until it's filed. If the user later says a filed capture misstated something, their correction enters the inbox as a new source. The filed capture is never edited.
