---
name: message-timestamps
what: Every message the user sends arrives with the current date and time attached, so the agent always knows when "now" is
type: automation
requires: Claude Code (any surface that honors hooks in settings.json)
effort: one minute, one settings edit
suggest_when: the agent misdates a day log or chronicle entry, reasons from a stale "today", or asks the user what time it is
status: recommended
---

# Message timestamps: the agent always knows when now is

A Claude Code `UserPromptSubmit` hook that runs `date` on every message the user sends, injecting the current date and time into the context alongside it. It closes a quiet failure mode: an agent's sense of "now" is set once at session start, so in a long-running or resumed session it drifts — day logs get yesterday's date, "today" means the wrong day, dated records misfile. With the hook, every user message re-anchors the clock.

## Why this is here

Earned in the source vault, where dated surfaces are everywhere (day logs, chronicle entries, issue files, `updated:` stamps) and a session open across an afternoon was silently misdating them. The hook fixed the whole class at once. The property that makes it worth shipping: it is completely transparent — the user never sees it, never maintains it, and never needs to know it is working for it to work. There is nothing to remember and nothing to keep fresh.

## What you'll end up with

Every user message arrives with a line like `Wed 2026-08-26 4:05PM` attached. Dated writes (logs, entries, stamps, filenames) use the message's clock, not the session's stale one. No visible change anywhere else.

## Setup

Agent-driven, one edit. Add to the user's `~/.claude/settings.json` (machine-wide, recommended — the benefit is not vault-specific), merging with any existing `hooks` block rather than replacing it:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "date '+%a %Y-%m-%d %-I:%M%p'"
          }
        ]
      }
    ]
  }
}
```

If the user prefers it scoped to the vault alone, the same block goes in the vault's `.claude/settings.json` instead. Never overwrite an existing settings file; merge the hook into what is there.

## Verify it works

Send any message in a fresh session and ask the agent what time you sent it. It should answer to the minute without calling any tool. Then check the next dated write (a day-log line, an entry filename) carries the right date.
