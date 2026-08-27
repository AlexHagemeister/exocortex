---
name: digest-nudge
what: A session-start reminder that fires only when the digest review is overdue, so a manually-run digest never silently lapses
type: automation
requires: Claude Code (SessionStart hooks); the shipped digest skill's review markers
effort: one minute, one settings edit (the script ships with the program)
suggest_when: the user runs the digest by hand and reviews have quietly stopped happening, or asks how to keep a manual cadence honest without scheduling it
status: recommended
---

# Digest nudge: overdue-only, zero noise otherwise

The digest is deliberately manual: a review surface that fires unread builds nothing, so the system leaves the cadence to you. The cost of that choice is silent lapse — nothing tells you three weeks have passed. This recipe closes the gap without a schedule and without context noise: a `SessionStart` hook runs the shipped script `.claude/scripts/digest-nudge.sh`, which compares today against the newest review marker in `.state/review-markers/` (stamped by the digest skill at each completed review). Over the threshold (default 7 days), one gentle line enters the session's starting context telling the agent to offer the digest once at a natural moment. Under it, the script prints nothing, and nothing enters context at all.

## Why this is here

Built in the source vault the day its own review gap hit 26 days unnoticed. The design constraints it satisfies, stated by the user there: fully deterministic (the shell computes the gap, the agent never checks anything), zero tokens under threshold, once per session at start, and no new bookkeeping — it reads state the digest skill already writes, so a completed review silences it automatically.

## What you'll end up with

Sessions opened while the review gap exceeds the threshold begin with the agent knowing, and it offers the digest once, gently. Every other session is byte-for-byte unchanged. The nudge stops on its own the moment a review completes.

## Setup

Agent-driven, one edit. The script already ships at `.claude/scripts/digest-nudge.sh`. Add to the vault's `.claude/settings.json` (project-scoped — the nudge belongs only to vault sessions), merging with any existing `hooks` block rather than replacing it:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh .claude/scripts/digest-nudge.sh"
          }
        ]
      }
    ]
  }
}
```

For a different threshold, pass it as an argument: `sh .claude/scripts/digest-nudge.sh 14`.

## Verify it works

Run `sh .claude/scripts/digest-nudge.sh 0` from the vault root: it should print the nudge line with the current gap (any completed review ever means the gap is over zero). Then run it bare: silent if you are under threshold, the same line if you are over. If `.state/review-markers/` is empty (no review yet completed), the script stays silent by design — the first nudge can only follow the first review.
