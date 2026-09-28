#!/usr/bin/env bash
# conformance.sh: read-only publishing-boundary check for the private vault
# against this repo's MANIFEST. Three parts:
#
#   (a) classification by KIND: every file of a shippable kind in the vault
#       must appear exactly once in MANIFEST, as a ship line or a `# private:`
#       line (directly, or under a listed directory). The kinds are listed in
#       KINDS below. Adding a kind is a publishing decision; adding a path is
#       not needed, which is the point: a new skill, script, README, meta doc
#       or template is caught the day it appears, wherever it appears.
#   (b) reference scan: shipped files naming a private entry (a skill or script
#       name, a private README's folder, a private doc's basename). Hits are
#       printed for the reviewer; some are accepted on purpose (GLOSSARY trial
#       annotations, per the vault's rules), so they never fail the run.
#   (c) drift (with --drift): manifested vault paths that differ from the copy
#       in this repo.
#
# Exit 1 on any unclassified entry, else 0. Never writes. sync.sh runs (a)
# and (b) before copying anything, so a publish cannot skip them.
#
# Requires tools/publish.local.conf (gitignored) defining VAULT_PATH.
#
# The universe of vault files is `git ls-files -co --exclude-standard` in the
# vault: tracked plus untracked-unignored, the same universe sync.sh's leak
# scan uses. Caches and venvs are gitignored, so they never appear.

set -euo pipefail

REPO_ROOT="${CONFORMANCE_REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
CONF="$REPO_ROOT/tools/publish.local.conf"
MANIFEST="$REPO_ROOT/MANIFEST"

die() { echo "ERROR: $*" >&2; exit 2; }

[ -f "$CONF" ] || die "missing $CONF (copy publish.local.conf.example and fill it in)"
# shellcheck source=/dev/null
source "$CONF"
[ -n "${VAULT_PATH:-}" ] || die "VAULT_PATH not set in publish.local.conf"
[ -f "$VAULT_PATH/CLAUDE.md" ] || die "no CLAUDE.md at VAULT_PATH, is '$VAULT_PATH' really the vault?"
[ -f "$MANIFEST" ] || die "missing $MANIFEST"

drift=0
[ "${1:-}" = "--drift" ] && drift=1

# --- manifest: ship lines and private lines ---------------------------------
# Ship lines: every non-comment, non-empty line. Private lines: after the
# `# private:` header, any comment whose first token is a path that exists in
# the vault. A path-shaped token after the header that does NOT exist is
# reported as stale, so a deleted file cannot hide behind an old private line.
ship="$(grep -v '^#' "$MANIFEST" | grep -v '^[[:space:]]*$' | sed 's#/$##')"
private=""
stale=""
in_private=0
while IFS= read -r line; do
  case "$line" in
    "# private:"*) in_private=1; continue ;;
  esac
  [ "$in_private" -eq 1 ] || continue
  case "$line" in \#*) ;; *) in_private=0; continue ;; esac
  tok="$(sed -nE 's/^#[[:space:]]+([A-Za-z0-9_./-]+).*/\1/p' <<< "$line")"
  [ -n "$tok" ] || continue
  case "$tok" in */*|*.*) ;; *) continue ;; esac
  tok="${tok%/}"
  if [ -e "$VAULT_PATH/$tok" ]; then
    private="${private}${tok}"$'\n'
  else
    stale="${stale}${tok}"$'\n'
  fi
done < "$MANIFEST"
classified="$(printf '%s\n%s' "$ship" "$private" | grep -v '^$')"

# --- vault universe ---------------------------------------------------------
universe="$(git -C "$VAULT_PATH" ls-files -co --exclude-standard)"

# KINDS: one grep -E pattern per line, matched against vault-relative paths.
# Each hit is reduced to the entry that MANIFEST would name (a skill's
# directory, a script's top-level file or directory, a README's own path).
KINDS='^[^/]+\.md$
^\.claude/skills/[^/]+/
^\.claude/scripts/[^/]+
^\.claude/agents/[^/]+
(^|/)README\.md$
^meta/[^/]+
^templates/[^/]+'

# User-owned zones: a README below the zone root is the user's own file, not
# folder law. The zone-root README itself still counts.
USER_ZONES='^(notes|attachments|staging|drawings)/.+/README\.md$'

entries=""
while IFS= read -r kind; do
  [ -n "$kind" ] || continue
  hits="$(grep -E "$kind" <<< "$universe" || true)"
  [ -n "$hits" ] || continue
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if grep -qE "$USER_ZONES" <<< "$f"; then continue; fi
    case "$kind" in
      '^\.claude/skills/[^/]+/') e="$(sed -E 's#^(\.claude/skills/[^/]+)/.*#\1#' <<< "$f")" ;;
      '^\.claude/scripts/[^/]+')  e="$(sed -E 's#^(\.claude/scripts/[^/]+)/.*#\1#' <<< "$f")" ;;
      '^meta/[^/]+')              e="$(sed -E 's#^(meta/[^/]+)/.*#\1#' <<< "$f")" ;;
      *)                          e="$f" ;;
    esac
    entries="${entries}${e}"$'\n'
  done <<< "$hits"
done <<< "$KINDS"
entries="$(sort -u <<< "$entries" | grep -v '^$')"

is_classified() {
  local e="$1" m
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    [ "$e" = "$m" ] && return 0
    case "$e" in "$m"/*) return 0 ;; esac
  done <<< "$classified"
  return 1
}

# --- (a) classification -----------------------------------------------------
unclassified=""
count=0
while IFS= read -r e; do
  [ -n "$e" ] || continue
  count=$((count + 1))
  is_classified "$e" || unclassified="${unclassified}${e}"$'\n'
done <<< "$entries"

echo "(a) classification: $count entries of shippable kinds checked"
if [ -n "$unclassified" ]; then
  echo "UNCLASSIFIED (on neither side of MANIFEST, an unmade publishing decision):"
  printf '  %s\n' $unclassified
fi
if [ -n "$stale" ]; then
  echo "STALE private lines (path no longer in the vault):"
  printf '  %s\n' $stale
fi

# --- (b) reference scan -----------------------------------------------------
# Shipped file set: every ship entry, directories expanded through the universe.
shipped_files=""
while IFS= read -r m; do
  [ -n "$m" ] || continue
  if [ -d "$VAULT_PATH/$m" ]; then
    shipped_files="${shipped_files}$(grep -E "^${m}/" <<< "$universe" || true)"$'\n'
  else
    shipped_files="${shipped_files}${m}"$'\n'
  fi
done <<< "$ship"
shipped_files="$(grep -v '^$' <<< "$shipped_files")"

# Deployment-authored files the program tells every consumer to write for
# themselves are named by shipped files on purpose and never scanned.
REFERENCE_EXEMPT='meta/DEPLOYMENT.md
meta/chronicle-surfaces.md
CLAUDE.local.md'

echo "(b) reference scan: shipped files naming private entries"
refhits=0
while IFS= read -r p; do
  [ -n "$p" ] || continue
  grep -qxF "$p" <<< "$REFERENCE_EXEMPT" && continue
  base="$(basename "$p")"
  case "$p" in
    .claude/skills/*)   pats="skills/${base}"; case "$base" in *-*) pats="${pats}|\b${base}\b" ;; esac ;;
    .claude/scripts/*)  if [ -d "$VAULT_PATH/$p" ]; then pats="scripts/${base}"; else pats="\b${base}\b"; fi ;;
    */README.md)        pats="$(dirname "$p")" ;;
    *)                  pats="\b${base}\b" ;;
  esac
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    # ISSUES.md ships convention-only (sync.sh strips the open-issue list),
    # so only its convention section is scanned.
    if [ "$f" = "ISSUES.md" ]; then
      hits="$(awk '{print} /^## Open/{exit}' "$VAULT_PATH/$f" | LC_ALL=C grep -nE "$pats" || true)"
    else
      hits="$(LC_ALL=C grep -nE "$pats" "$VAULT_PATH/$f" 2>/dev/null || true)"
    fi
    if [ -n "$hits" ]; then
      echo "  $f names private '$p':"
      head -3 <<< "$hits" | sed 's/^/    /'
      refhits=$((refhits + 1))
    fi
  done <<< "$shipped_files"
done <<< "$private"
[ "$refhits" -eq 0 ] && echo "  none"

# --- (c) drift --------------------------------------------------------------
if [ "$drift" -eq 1 ]; then
  echo "(c) drift: manifested vault paths differing from this repo"
  dhits=0
  while IFS= read -r m; do
    [ -n "$m" ] || continue
    src="$VAULT_PATH/$m"; dst="$REPO_ROOT/$m"
    if [ "$m" = "ISSUES.md" ]; then
      a="$(awk '{print} /^## Open/{exit}' "$src")"
      b="$(awk '{print} /^## Open/{exit}' "$dst" 2>/dev/null || true)"
      [ "$a" = "$b" ] || { echo "  $m (convention section)"; dhits=$((dhits + 1)); }
    elif [ -d "$src" ]; then
      if ! diff -rq "$src" "$dst" >/dev/null 2>&1; then
        echo "  $m/"; diff -rq "$src" "$dst" 2>&1 | head -5 | sed 's/^/    /' || true; dhits=$((dhits + 1))
      fi
    elif ! cmp -s "$src" "$dst"; then
      echo "  $m"; dhits=$((dhits + 1))
    fi
  done <<< "$ship"
  [ "$dhits" -eq 0 ] && echo "  none"
fi

[ -z "$unclassified" ] || exit 1
exit 0
