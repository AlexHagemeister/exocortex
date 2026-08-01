#!/bin/bash
# ingest-file.sh <inbox-item> <stream-folder> [target-filename]
#
# Mechanical half of ingest filing (skill: .claude/skills/ingest, step 2):
#   dedup-check against the hash ledger, move to the stream, append the ledger
#   line, grep wiki/ for stale citations of the old inbox path.
# Judgment stays with the agent: stream choice, filename, what to do with
# duplicates, and rewriting any stale citations this script reports.
#
# Exit codes: 0 filed clean · 1 usage/error · 2 duplicate (nothing moved)
set -euo pipefail

VAULT="$(cd "$(dirname "$0")/../.." && pwd)"
LEDGER="$VAULT/.state/ingest-hashes.txt"

[ $# -ge 2 ] || { echo "usage: ingest-file.sh <inbox-item> <stream-folder> [target-filename]" >&2; exit 1; }

ITEM="$1"
STREAM="$2"
[ -f "$ITEM" ] || { echo "ERROR: no such file: $ITEM" >&2; exit 1; }
[ -d "$VAULT/$STREAM" ] || { echo "ERROR: no such stream folder: $STREAM (vault-relative)" >&2; exit 1; }

NAME="${3:-$(basename "$ITEM")}"
TARGET="$VAULT/$STREAM/$NAME"
REL_TARGET="$STREAM/$NAME"

HASH=$(shasum -a 256 "$ITEM" | awk '{print $1}')

touch "$LEDGER"
if EXISTING=$(grep -m1 "^$HASH " "$LEDGER"); then
  echo "DUPLICATE: content already ingested as: ${EXISTING#*  }"
  echo "Nothing moved. Delete the inbox item and log, per ingest step 1."
  exit 2
fi

[ ! -e "$TARGET" ] || { echo "ERROR: target exists: $REL_TARGET" >&2; exit 1; }

# Old path as cited from wiki pages (vault-relative), before the move.
OLD_REL="${ITEM#"$VAULT"/}"

mv "$ITEM" "$TARGET"
printf '%s  %s\n' "$HASH" "$REL_TARGET" >> "$LEDGER"

echo "FILED: $REL_TARGET"
echo "HASH:  $HASH (ledger appended)"

STALE=$(grep -rln --include='*.md' -F "$OLD_REL" "$VAULT/wiki" 2>/dev/null || true)
if [ -n "$STALE" ]; then
  echo "STALE CITATIONS of $OLD_REL — rewrite these to the filed path:"
  echo "$STALE" | sed "s|^$VAULT/||"
else
  echo "STALE CITATIONS: none"
fi
