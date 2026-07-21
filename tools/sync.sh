#!/usr/bin/env bash
# sync.sh — pull the portable system files from the private vault into this
# repo, then leak-scan the result. Never pushes unless invoked as
# `sync.sh --push`, and then only after verifying the remote is the public
# repo (not the private mirror).
#
# Requires tools/publish.local.conf (gitignored), defining:
#   VAULT_PATH        absolute path to the private vault
#   EXPECTED_REMOTE   substring the public origin URL must contain
# and tools/leak-patterns.local.txt (gitignored): one grep -E pattern per
# line of private strings that must never appear in the public tree.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF="$REPO_ROOT/tools/publish.local.conf"
PATTERNS="$REPO_ROOT/tools/leak-patterns.local.txt"

die() { echo "ERROR: $*" >&2; exit 1; }

[ -f "$CONF" ] || die "missing $CONF (copy publish.local.conf.example and fill it in)"
# shellcheck source=/dev/null
source "$CONF"
[ -n "${VAULT_PATH:-}" ] || die "VAULT_PATH not set in publish.local.conf"
[ -n "${EXPECTED_REMOTE:-}" ] || die "EXPECTED_REMOTE not set in publish.local.conf"
[ -f "$VAULT_PATH/CLAUDE.md" ] || die "no CLAUDE.md at VAULT_PATH — is '$VAULT_PATH' really the vault?"
[ -f "$PATTERNS" ] || die "missing $PATTERNS — the leak scan refuses to run without local patterns"

# --- push mode: guard the remote, push, done -------------------------------
if [ "${1:-}" = "--push" ]; then
  origin="$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null)" \
    || die "no 'origin' remote configured"
  case "$origin" in
    *mirror*) die "origin '$origin' looks like the PRIVATE mirror — refusing to push" ;;
  esac
  case "$origin" in
    *"$EXPECTED_REMOTE"*) ;;
    *) die "origin '$origin' does not match EXPECTED_REMOTE ('$EXPECTED_REMOTE')" ;;
  esac
  git -C "$REPO_ROOT" push origin main
  echo "Pushed to $origin"
  exit 0
fi

# --- sync: copy manifest entries from the vault ----------------------------
while IFS= read -r entry; do
  case "$entry" in ''|\#*) continue ;; esac
  src="$VAULT_PATH/$entry"
  dst="$REPO_ROOT/$entry"
  [ -e "$src" ] || die "manifest entry not found in vault: $entry"
  if [ "$entry" = "ISSUES.md" ]; then
    # Convention only — strip the live open-issue index.
    mkdir -p "$(dirname "$dst")"
    awk '{print} /^## Open/{exit}' "$src" > "$dst"
    printf '\n*(none — the list above is regenerated from .state/issues/ in a live vault)*\n' >> "$dst"
  elif [ -d "$src" ]; then
    mkdir -p "$dst"
    rsync -a --delete "$src/" "$dst/"
  else
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  fi
done < "$REPO_ROOT/MANIFEST"

# The real deployment bindings must never land here — only the template ships.
[ ! -e "$REPO_ROOT/meta/DEPLOYMENT.md" ] \
  || die "meta/DEPLOYMENT.md found in repo — only DEPLOYMENT.template.md may ship"

# --- glossary drift: README Key terms vs GLOSSARY.md -----------------------
glossary="$REPO_ROOT/GLOSSARY.md"
readme="$REPO_ROOT/README.md"
[ -f "$glossary" ] || die "GLOSSARY.md missing after sync"
while IFS= read -r line; do
  [ -z "$line" ] && continue
  term="$(sed -n 's/^- \*\*\([^*]*\)\*\* — \(.*\)/\1/p' <<< "$line")"
  def="$(sed -n 's/^- \*\*\([^*]*\)\*\* — \(.*\)/\2/p' <<< "$line")"
  [ -z "$term" ] && continue
  expected="**${term}** — ${def}"
  gloss_line="$(grep -F "**${term}** —" "$glossary" | head -1 || true)"
  if [ "$gloss_line" != "$expected" ]; then
    die "glossary drift on '${term}': README and GLOSSARY.md one-liners must match exactly"
  fi
done < <(awk '/^## Key terms$/{in_section=1; next} in_section && /^## /{exit} in_section && /^- \*\*/{print}' "$readme")

# --- leak scan -------------------------------------------------------------
# Built-in structural patterns + local private patterns, over every file git
# would publish (tracked + untracked-unignored). LICENSE is exempt from the
# local patterns (the copyright line legitimately carries the author's name).
# Structural = absolute home paths (/Users/...), which identify a person;
# generic macOS iCloud container paths in tilde form are documentation, not
# leaks, and are deliberately not flagged.
scan_failed=0
builtin_patterns='/Users/'
files="$(git -C "$REPO_ROOT" ls-files -co --exclude-standard)"
while IFS= read -r f; do
  [ -f "$REPO_ROOT/$f" ] || continue
  case "$f" in tools/sync.sh|tools/bootstrap.sh) continue ;; esac  # these scripts name the patterns they check for
  if grep -nE "$builtin_patterns" "$REPO_ROOT/$f" >/dev/null 2>&1; then
    echo "LEAK (structural) in $f:"; grep -nE "$builtin_patterns" "$REPO_ROOT/$f" | head -5
    scan_failed=1
  fi
  [ "$f" = "LICENSE" ] && continue
  if grep -niEf "$PATTERNS" "$REPO_ROOT/$f" >/dev/null 2>&1; then
    echo "LEAK (private pattern) in $f:"; grep -niEf "$PATTERNS" "$REPO_ROOT/$f" | head -5
    scan_failed=1
  fi
done <<< "$files"

[ "$scan_failed" -eq 0 ] || die "leak scan failed — fix the files above before committing"

echo "Sync complete, leak scan clean. Review before committing:"
git -C "$REPO_ROOT" status --short
