#!/usr/bin/env bash
# bootstrap.sh — scaffold a new exocortex vault from this repo.
#
#   ./tools/bootstrap.sh /path/to/your/vault           # fresh install (never overwrites)
#   ./tools/bootstrap.sh /path/to/your/vault --update  # refresh program files in an
#                                                      # existing vault (overwrites the
#                                                      # program, never your data)
#
# The program file list lives in MANIFEST — one home, shared with tools/sync.sh:
# directory entries sync whole folders, file entries copy one file. Your data
# (sources/, notes/, wiki/, staging/, .state/ working files, meta/DEPLOYMENT.md)
# is never touched by --update, and skills or scripts you added locally are left
# alone — only the shipped folders and files are synced.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-}"
MODE="${2:-}"

die() { echo "ERROR: $*" >&2; exit 1; }
[ -n "$TARGET" ] || die "usage: bootstrap.sh /path/to/vault [--update]"

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"
[ "$TARGET" != "$REPO_ROOT" ] || die "the vault cannot be this repo — pick a separate directory"

case "$TARGET" in
  *"Mobile Documents"*|*iCloud*)
    echo "WARNING: this path looks iCloud-synced. The vault is designed to be a git repo,"
    echo "         and iCloud corrupts repos (eviction, conflict copies). Pick a non-synced"
    echo "         path; for devices use a dotfolder-ignoring layer like Obsidian Sync."
    echo "         See SETUP.md." ;;
esac

# Data skeleton — created empty, owned by you from here on. The wiki topic
# folders match what wiki/README.md declares; keep the two in step.
mkdir -p "$TARGET/sources/inbox" "$TARGET/notes" "$TARGET/wiki/log" \
         "$TARGET/wiki/concepts" "$TARGET/wiki/projects" "$TARGET/wiki/people" \
         "$TARGET/wiki/life" "$TARGET/wiki/craft" "$TARGET/wiki/connections" \
         "$TARGET/.state/issues" "$TARGET/templates" "$TARGET/meta" \
         "$TARGET/attachments" "$TARGET/staging" "$TARGET/drawings" \
         "$TARGET/.claude/skills" "$TARGET/.claude/scripts"

MANIFEST_FILE="$REPO_ROOT/MANIFEST"
[ -f "$MANIFEST_FILE" ] || die "MANIFEST missing from repo — cannot determine program files"

copy() { # copy $1 (repo-relative) into the vault, honoring mode
  local src="$REPO_ROOT/$1" dst="$TARGET/$1"
  mkdir -p "$(dirname "$dst")"
  if [ "$MODE" = "--update" ] || [ ! -e "$dst" ]; then
    cp "$src" "$dst"
  fi
}

seed() { # copy $1 (repo-relative) into the vault only if absent
  local src="$REPO_ROOT/$1" dst="$TARGET/$1"
  mkdir -p "$(dirname "$dst")"
  [ -e "$dst" ] || cp "$src" "$dst"
}

sync_dir() { # sync directory $1 (repo-relative, no trailing slash), honoring mode
  local src="$REPO_ROOT/$1" dst="$TARGET/$1"
  mkdir -p "$dst"
  if [ "$MODE" = "--update" ]; then
    rsync -a --delete "$src/" "$dst/"
  else
    rsync -a --ignore-existing "$src/" "$dst/"
  fi
}

# Install-only files are seeded once, then owned by the vault. ISSUES.md is the
# vault's derived open-issue index — --update must never overwrite it.
while IFS= read -r entry; do
  case "$entry" in ''|\#*) continue ;; esac
  [ -e "$REPO_ROOT/$entry" ] || die "MANIFEST entry missing from repo: $entry"
  if [ "${entry%/}" != "$entry" ]; then
    sync_dir "${entry%/}"
  elif [ "$entry" = "ISSUES.md" ]; then
    seed "$entry"
  else
    copy "$entry"
  fi
done < "$MANIFEST_FILE"

# Deployment bindings: template becomes the live file, once. Never overwritten.
if [ ! -e "$TARGET/meta/DEPLOYMENT.md" ]; then
  cp "$REPO_ROOT/meta/DEPLOYMENT.template.md" "$TARGET/meta/DEPLOYMENT.md"
fi

# Wiki indexes: seeded once (root index = the query entry point, plus one
# derived-listing stub per topic folder), then owned by the pipeline —
# regenerated in the vault, never synced back from this repo. These stay out
# of MANIFEST deliberately: a live vault's indexes list personal pages.
seed "wiki/index.md"
for idx in "$REPO_ROOT"/wiki/*/index.md; do
  seed "wiki/$(basename "$(dirname "$idx")")/index.md"
done

echo "Vault scaffolded at: $TARGET"
echo
echo "Next steps (details in SETUP.md):"
echo "  1. Fill in $TARGET/meta/DEPLOYMENT.md — every UNSET row."
echo "  2. Build the lint graph venv (needs python3):"
echo "       python3 -m venv $TARGET/.claude/scripts/graph-venv"
echo "       $TARGET/.claude/scripts/graph-venv/bin/pip install networkx pyyaml"
echo "  3. Open Claude Code in the vault; the skills in .claude/skills/ register automatically."
echo "  4. git init the vault (if it isn't a repo yet), add a PRIVATE remote, and run the vault-snapshot skill."
echo "  5. Optionally schedule process-inbox / lint / digest / vault-snapshot runs."
echo "  6. Drop something into sources/inbox/ and run process-inbox."
