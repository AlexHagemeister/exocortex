#!/bin/bash
# day-log.sh: append one entry to the vault's day log, wiki/log/<YYYY-MM-DD>.md.
#
# Usage:
#   day-log.sh [--date YYYY-MM-DD] <entry text...>
#   day-log.sh [--date YYYY-MM-DD] <<'EOF'
#   entry text with `backticks` and "quotes", read from stdin
#   EOF
#
# The date defaults to the vault day, which runs 04:00 to 04:00 local time
# (wiki/chronicle/README.md): before 04:00 the entry goes to the previous
# day's file, from 04:00 on to today's. --date overrides. The file is created
# if missing (day logs carry no heading and no frontmatter). The entry gets a
# "* " prefix unless it already starts with "* " or "- ", and is separated
# from the previous entry by one blank line. Prints the vault-relative path written.
#
# Why a script: the write is append-only (one O_APPEND write, never a
# read-modify-rewrite), so concurrent lock-exempt writers cannot clobber each
# other, and the path is resolved here, so no agent ever types the filename.
#
# Vault root: two levels up from this script, or $EXOCORTEX_VAULT if set.
# Testing only: DAY_LOG_NOW="YYYY-MM-DD HH:MM" stands in for the local clock.
set -eu

DAY_START_HOUR=4

VAULT="${EXOCORTEX_VAULT:-$(cd "$(dirname "$0")/../.." && pwd)}"

usage() { echo "usage: day-log.sh [--date YYYY-MM-DD] [entry text...]  (no text: read stdin)" >&2; exit 1; }

DATE=""
if [ "${1:-}" = "--date" ]; then
  [ $# -ge 2 ] || usage
  DATE="$2"
  shift 2
fi

if [ -n "$DATE" ]; then
  if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "day-log.sh: bad --date '$DATE' (want YYYY-MM-DD)" >&2; exit 1
  fi
  # Reject impossible calendar dates (2026-02-30). BSD date first, then GNU.
  CHECK=$(date -j -f %Y-%m-%d "$DATE" +%Y-%m-%d 2>/dev/null || date -d "$DATE" +%Y-%m-%d 2>/dev/null || true)
  if [ "$CHECK" != "$DATE" ]; then
    echo "day-log.sh: bad --date '$DATE' (not a calendar date)" >&2; exit 1
  fi
else
  NOW="${DAY_LOG_NOW:-$(date '+%Y-%m-%d %H:%M')}"
  if ! [[ "$NOW" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})\ ([0-9]{2}):[0-9]{2}$ ]]; then
    echo "day-log.sh: bad clock '$NOW' (want YYYY-MM-DD HH:MM)" >&2; exit 1
  fi
  DATE="${BASH_REMATCH[1]}"
  HOUR=$((10#${BASH_REMATCH[2]}))
  if [ "$HOUR" -lt "$DAY_START_HOUR" ]; then
    # Before the day boundary: the previous day's log. BSD date first, then GNU.
    DATE=$(date -j -v-1d -f %Y-%m-%d "$DATE" +%Y-%m-%d 2>/dev/null || date -d "$DATE -1 day" +%Y-%m-%d 2>/dev/null) \
      || { echo "day-log.sh: could not compute the previous day" >&2; exit 1; }
  fi
fi

if [ $# -gt 0 ]; then
  ENTRY="$*"
else
  ENTRY=$(cat)
fi

# Refuse an entry that is empty or whitespace only.
if [ -z "$(printf '%s' "$ENTRY" | tr -d '[:space:]')" ]; then
  echo "day-log.sh: refusing an empty entry" >&2; exit 1
fi

case "$ENTRY" in
  "* "*|"- "*) ;;
  *) ENTRY="* $ENTRY" ;;
esac

REL="wiki/log/$DATE.md"
FILE="$VAULT/$REL"
[ -d "$VAULT/wiki/log" ] || { echo "day-log.sh: no wiki/log/ under $VAULT" >&2; exit 1; }

# Separator: nothing for an empty or missing file, one blank line otherwise,
# plus a newline first if the file does not end in one.
SEP=""
if [ -s "$FILE" ]; then
  SEP=$'\n'
  [ -n "$(tail -c 1 "$FILE")" ] && SEP=$'\n\n'
fi

# One append, one write call. Never rewrite the file.
printf '%s%s\n' "$SEP" "$ENTRY" >> "$FILE"
echo "$REL"
