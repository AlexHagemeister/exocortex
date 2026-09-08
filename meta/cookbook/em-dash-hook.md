---
name: em-dash-hook
what: A machine-wide edit hook that catches an em dash the moment an agent writes one and nudges it to fix the line before moving on
type: automation
requires: Claude Code (PostToolUse hooks); jq on PATH
effort: two minutes, one small script and one settings edit
suggest_when: the user has a no-em-dash style rule that agents keep violating in written files despite instructions, in this vault or any project
status: recommended
---

# Em dash hook: enforcement at write time, not review time

A style rule stated in instructions ("no em dashes") degrades over a long session: the model drifts, and the dashes land in files where the user finds them later. This recipe moves enforcement from instructions to the harness. A `PostToolUse` hook on the `Write` and `Edit` tools inspects only the new text an edit introduces. When that text contains an em dash (U+2014), the hook returns a blocking message that lands in the agent's context immediately, telling it to replace the dash (comma, parentheses, colon, or two sentences) and continue. Clean edits pass silently at zero token cost, and em dashes already sitting in a file never fire it, so there is no nagging about legacy prose.

## Why this is here

Built in the source vault after its curator got tired of em dashes showing up in vault files despite a standing rule in every instruction surface. First installed vault-scoped, then promoted machine-wide the same evening because the annoyance was never vault-specific. The larger unlock: any mechanical style rule the model drifts on can be enforced this same way, deterministically, with the correction arriving while the agent still has the edit in hand rather than in a review pass days later.

## What you'll end up with

Every Claude Code session on the machine, in every project, self-corrects em dashes at the moment of writing. The agent sees the nudge as tool feedback, fixes the line, and moves on. Sessions that never write an em dash are byte-for-byte unchanged.

## Setup

Agent-driven, two steps. Machine-wide means the user-level surfaces (`~/.claude/`), not any project's `.claude/`.

1. Write the script to `~/.claude/hooks/em-dash-check.sh` and make it executable (`chmod +x`):

```sh
#!/bin/sh
# PostToolUse hook (Write|Edit): nudge the agent when an edit introduces an em dash.
# Checks only the new text being written, so pre-existing em dashes in a file don't fire it.
input=$(cat)
new_text=$(printf '%s' "$input" | jq -r '[.tool_input.new_string, .tool_input.content, (.tool_input.edits // [] | .[].new_string)] | map(select(. != null)) | join("\n")')
case "$new_text" in
  *—*)
    printf '%s\n' '{"decision":"block","reason":"This edit introduced an em dash (—). House style: no em dashes anywhere. Replace it with a comma, parentheses, a colon, or two sentences, then continue."}'
    ;;
esac
exit 0
```

2. Add to `~/.claude/settings.json`, merging with any existing `hooks` block rather than replacing it:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/em-dash-check.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

To scope it to one project instead, put the script in that project's `.claude/scripts/` and the hook entry in its `.claude/settings.json`, with the command as a relative path. Adapt the same skeleton for any other character or phrase rule by changing the `case` pattern and the message.

## Verify it works

Pipe a synthetic payload through the script: `echo '{"tool_input":{"new_string":"bad — line"}}' | ~/.claude/hooks/em-dash-check.sh` should print the block JSON, and a payload without a dash should print nothing. Then have the agent write an em dash into a scratch file: the nudge should appear as a hook message on that edit (delete the probe file after). If the live probe stays silent while the pipe test passes, the session predates the settings change; a new session picks it up.
