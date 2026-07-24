#!/usr/bin/env bash
# bootstrap.sh — scaffold a new exocortex vault from this repo.
#
#   ./tools/bootstrap.sh /path/to/your/vault           # fresh install (never overwrites)
#   ./tools/bootstrap.sh /path/to/your/vault --update  # refresh program files in an
#                                                      # existing vault (overwrites the
#                                                      # program, never your data)
#
# Program files: CLAUDE.md, CONSTITUTION.md, .claude/skills/, templates/,
# .state/README.md, meta/ reference docs. Your data (sources/, notes/, wiki/,
# .state/ working files, meta/DEPLOYMENT.md) is never touched by --update.

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

# Data skeleton — created empty, owned by you from here on.
mkdir -p "$TARGET/sources/inbox" "$TARGET/notes" "$TARGET/wiki/log" \
         "$TARGET/.state/issues" "$TARGET/templates" "$TARGET/meta" \
         "$TARGET/.claude/skills"

PROGRAM_FILES=(CLAUDE.md CONSTITUTION.md GLOSSARY.md templates/default.md
               .state/README.md meta/README.md meta/HANDOFF.md
               meta/VAULT-DOCTRINE.md meta/OKF-SPEC.md)

# Install-only files: seeded once, then owned by the vault. ISSUES.md is the
# vault's derived open-issue index — --update must never overwrite it.
INSTALL_ONLY_FILES=(ISSUES.md)

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

for f in "${PROGRAM_FILES[@]}"; do copy "$f"; done
for f in "${INSTALL_ONLY_FILES[@]}"; do seed "$f"; done

if [ "$MODE" = "--update" ]; then
  rsync -a --delete "$REPO_ROOT/.claude/skills/" "$TARGET/.claude/skills/"
else
  rsync -a --ignore-existing "$REPO_ROOT/.claude/skills/" "$TARGET/.claude/skills/"
fi

# Deployment bindings: template becomes the live file, once. Never overwritten.
if [ ! -e "$TARGET/meta/DEPLOYMENT.md" ]; then
  cp "$REPO_ROOT/meta/DEPLOYMENT.template.md" "$TARGET/meta/DEPLOYMENT.md"
fi

echo "Vault scaffolded at: $TARGET"
echo
echo "Next steps (details in SETUP.md):"
echo "  1. Fill in $TARGET/meta/DEPLOYMENT.md — every UNSET row."
echo "  2. Open Claude Code in the vault; the skills in .claude/skills/ register automatically."
echo "  3. git init the vault, add a PRIVATE remote, and run the vault-snapshot skill."
echo "  4. Optionally schedule process-inbox / lint / digest / vault-snapshot runs."
echo "  5. Drop something into sources/inbox/ and run process-inbox."
