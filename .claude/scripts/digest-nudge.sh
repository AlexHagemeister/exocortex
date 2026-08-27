#!/bin/sh
# Session-start digest nudge. Prints one gentle reminder when the newest
# review marker in .state/review-markers/ is older than the threshold
# (default 7 days, override with the first argument); prints nothing and
# exits 0 otherwise, so under threshold zero tokens enter context.
# Wired as a Claude Code SessionStart hook in the vault's .claude/settings.json
# (see meta/cookbook/digest-nudge.md). Runs from the vault root.
threshold="${1:-7}"
dir=".state/review-markers"
[ -d "$dir" ] || exit 0
last=$(ls "$dir" 2>/dev/null | sort | tail -1)
[ -n "$last" ] || exit 0
# BSD date (macOS) first, GNU date (Linux) fallback.
epoch=$(date -j -f %Y-%m-%d "$last" +%s 2>/dev/null || date -d "$last" +%s 2>/dev/null) || exit 0
days=$(( ($(date +%s) - epoch) / 86400 ))
[ "$days" -gt "$threshold" ] || exit 0
echo "It has been $days days since the last completed digest review (last marker: $last). When a natural moment arises this session, offer once, gently, to compile or review the digest. One mention, never insistent, and drop it if the user declines or ignores it."
