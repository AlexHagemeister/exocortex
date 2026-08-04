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
#             3 missing title:/description: (nothing moved — add them and retry,
#               or pass --allow-missing-frontmatter to file as-is)
set -euo pipefail

VAULT="$(cd "$(dirname "$0")/../.." && pwd)"
LEDGER="$VAULT/.state/ingest-hashes.txt"

ALLOW_MISSING=0
ARGS=()
for a in "$@"; do
  case "$a" in
    --allow-missing-frontmatter) ALLOW_MISSING=1 ;;
    *) ARGS+=("$a") ;;
  esac
done
set -- ${ARGS+"${ARGS[@]}"}

[ $# -ge 2 ] || { echo "usage: ingest-file.sh [--allow-missing-frontmatter] <inbox-item> <stream-folder> [target-filename]" >&2; exit 1; }

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

# Derived indexes pull their entries from title:/description:. A capture filed
# without them sits in the stream index as a slug with no retrieval hook, and
# the index is derived, so it cannot be patched afterward. Filing is the freeze:
# this is the last moment the fields can be added. Checked before the move so
# the item is still an editable inbox file when the check fires.
MISSING=""
grep -qE '^title:[[:space:]]*[^[:space:]]' "$ITEM" || MISSING="title:"
grep -qE '^description:[[:space:]]*[^[:space:]]' "$ITEM" || MISSING="${MISSING:+$MISSING and }description:"
if [ -n "$MISSING" ]; then
  if [ "$ALLOW_MISSING" -eq 0 ]; then
    echo "REFUSED: $ITEM has no $MISSING" >&2
    echo "Nothing moved. Write them from the item's own content now — inbox items are" >&2
    echo "freely editable until filing, and filing freezes the path and the frontmatter." >&2
    echo "To file as-is anyway: ingest-file.sh --allow-missing-frontmatter ..." >&2
    exit 3
  fi
  echo "WARNING: filing without $MISSING — its index entry will be a bare slug."
fi

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
