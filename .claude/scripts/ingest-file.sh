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
#             4 sources/inbox/ path reference inside the item (nothing moved —
#               rewrite each to a basename wikilink and retry, or pass
#               --allow-inbox-paths for a legitimate path mention, e.g. inside
#               a verbatim quote)
set -euo pipefail

VAULT="$(cd "$(dirname "$0")/../.." && pwd)"
LEDGER="$VAULT/.state/ingest-hashes.txt"

ALLOW_MISSING=0
ALLOW_INBOX_PATHS=0
ARGS=()
for a in "$@"; do
  case "$a" in
    --allow-missing-frontmatter) ALLOW_MISSING=1 ;;
    --allow-inbox-paths) ALLOW_INBOX_PATHS=1 ;;
    *) ARGS+=("$a") ;;
  esac
done
set -- ${ARGS+"${ARGS[@]}"}

[ $# -ge 2 ] || { echo "usage: ingest-file.sh [--allow-missing-frontmatter] [--allow-inbox-paths] <inbox-item> <stream-folder> [target-filename]" >&2; exit 1; }

ITEM="$1"
STREAM="${2%/}"
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

# A capture that names a sibling by its sources/inbox/ path freezes with a
# dead pointer, because filing moves the sibling and filed sources are never
# edited (paths die at filing; basenames survive). Checked before the move so
# the item is still an editable inbox file when the check fires. Rewriting is
# the agent's judgment (a verbatim quote containing a path is legitimate and
# files with --allow-inbox-paths); references to the item's own path are not
# counted.
SELF_BASE="$(basename "$ITEM")"
INBOX_REFS=$(grep -noE 'sources/inbox/[A-Za-z0-9._/-]+\.md' "$ITEM" | grep -vF "/$SELF_BASE" || true)
if [ -n "$INBOX_REFS" ]; then
  if [ "$ALLOW_INBOX_PATHS" -eq 0 ]; then
    echo "REFUSED: $ITEM references sources/inbox/ paths (line:match below)" >&2
    echo "$INBOX_REFS" >&2
    echo "Rewrite each to a basename wikilink ([[<name-without-.md>]]) now: inbox items" >&2
    echo "are freely editable until filing, and a filed inbox path is a dead pointer" >&2
    echo "the moment its target is filed. For a legitimate path mention (e.g. inside" >&2
    echo "a verbatim quote): ingest-file.sh --allow-inbox-paths ..." >&2
    exit 4
  fi
  echo "WARNING: filing with sources/inbox/ path references (--allow-inbox-paths):"
  echo "$INBOX_REFS"
fi

# Old path as cited from wiki pages (vault-relative), before the move. Since the
# 2026-08-17 link convention, wiki bodies cite sources by name ([[stem]]), which
# keeps resolving after filing. This grep is the safety net for any path-form
# reference (markdown link, path-qualified wikilink) that named the inbox path.
OLD_REL="${ITEM#"$VAULT"/}"

mv "$ITEM" "$TARGET"
printf '%s  %s\n' "$HASH" "$REL_TARGET" >> "$LEDGER"

echo "FILED: $REL_TARGET"
echo "HASH:  $HASH (ledger appended)"

STALE=$(grep -rln --include='*.md' -F "$OLD_REL" "$VAULT/wiki" 2>/dev/null || true)
if [ -n "$STALE" ]; then
  echo "STALE CITATIONS of $OLD_REL — path-form references; rewrite to [[$(basename "$REL_TARGET" .md)]]:"
  echo "$STALE" | sed "s|^$VAULT/||"
else
  echo "STALE CITATIONS: none"
fi
