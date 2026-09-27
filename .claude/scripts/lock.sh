#!/bin/bash
# lock.sh: the maintainer.lock protocol, mechanized.
#
# Lock file: .state/maintainer.lock, one line "<task> <ISO 8601 UTC> <pid>".
# The pid recorded is the session process (the first non-shell ancestor of
# this script), never a per-call shell that dies within a second.
#
# Subcommands:
#   lock.sh check           read-only. Prints "free", or
#                           "live|stale|dead <age>min <lock line>".
#                           Exit 0 free, 1 live, 3 stale or dead.
#   lock.sh acquire <task>  take the lock. Free: create it. Live: print the
#                           holder, write the stand-down day-log line, exit 1.
#                           Stale or dead: clear it with a day-log line and take
#                           it. Prints "acquired" or "replaced <state>", exit 0.
#   lock.sh touch <task>    heartbeat. Exit 0 if <task> holds the lock, else
#                           "not holder" on stderr and exit 2 (a resumed run
#                           learns it lost the lock).
#   lock.sh release <task>  remove the lock if <task> holds it, else exit 2.
#                           Never removes another task's lock.
#   Usage errors exit 64.
#
# Liveness: a numeric pid that fails kill -0 means dead. Otherwise the lock
# file's mtime decides: touched within STALE_MIN minutes is live, older is
# stale. Old two-field locks use the mtime rule alone.
#
# Judgment rules (when to take the lock, touching inside long steps, who is
# bound by it) live in .state/README.md, not here.
#
# Vault root: two levels up from this script, or $EXOCORTEX_VAULT if set.
set -u

STALE_MIN=30

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT="${EXOCORTEX_VAULT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
export EXOCORTEX_VAULT="$VAULT"
LOCK="$VAULT/.state/maintainer.lock"
DAYLOG="$SCRIPT_DIR/day-log.sh"

usage() {
  echo "usage: lock.sh check | acquire <task> | touch <task> | release <task>" >&2
  exit 64
}

# The session process: walk up from our parent past any shells (the per-call
# Bash tool shell, a wrapping bash or sh) to the first non-shell ancestor.
# Usually the grandparent. Falls back to $PPID.
session_pid() {
  local p="$PPID" comm next i
  for i in 1 2 3 4 5 6 7 8; do
    comm=$(ps -o comm= -p "$p" 2>/dev/null) || break
    comm="${comm##*/}"; comm="${comm#-}"
    case "$comm" in
      sh|bash|zsh|dash|ksh|fish) ;;
      *) echo "$p"; return ;;
    esac
    next=$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')
    case "$next" in ''|*[!0-9]*|0|1) break ;; esac
    p="$next"
  done
  echo "$PPID"
}

mtime() { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0; }

pid_alive() { kill -0 "$1" 2>/dev/null || ps -p "$1" >/dev/null 2>&1; }

# Sets STATE (free|live|stale|dead), LINE, AGE (minutes), MT (epoch mtime).
judge() {
  STATE=free; LINE=""; AGE=0; MT=0
  [ -e "$LOCK" ] || return 0
  LINE=$(head -n 1 "$LOCK" 2>/dev/null)
  MT=$(mtime "$LOCK")
  AGE=$(( ( $(date +%s) - MT ) / 60 ))
  local pid
  pid=$(printf '%s\n' "$LINE" | awk '{print $3}')
  case "$pid" in
    ''|*[!0-9]*) ;;
    *) if ! pid_alive "$pid"; then STATE=dead; return 0; fi ;;
  esac
  if [ "$AGE" -lt "$STALE_MIN" ]; then STATE=live; else STATE=stale; fi
}

holder() { printf '%s\n' "$LINE" | awk '{print $1}'; }

# Atomic create: noclobber in a subshell, so two racing creators cannot both win.
create() {
  local line="$1 $(date -u +%Y-%m-%dT%H:%M:%SZ) $(session_pid)"
  ( set -C; printf '%s\n' "$line" > "$LOCK" ) 2>/dev/null
}

log() { bash "$DAYLOG" "$1" >/dev/null || echo "lock.sh: day-log write failed" >&2; }

stand_down() {
  echo "held: $LINE (touched $AGE min ago)"
  log "**Stood down**: $TASK stood down, lock held by $LINE (touched $AGE min ago)."
  exit 1
}

# Remove a lock judged stale or dead, but only if it is still that same lock
# (same line, same mtime). Renaming first means a lock another run created in
# the meantime is put back rather than deleted.
clear_judged() {
  local tmp="$LOCK.clearing.$$"
  mv "$LOCK" "$tmp" 2>/dev/null || return 0
  if [ "$(head -n 1 "$tmp" 2>/dev/null)" = "$LINE" ] && [ "$(mtime "$tmp")" = "$MT" ]; then
    rm -f "$tmp"
  else
    ln "$tmp" "$LOCK" 2>/dev/null
    rm -f "$tmp"
  fi
}

CMD="${1:-}"
TASK="${2:-}"

case "$CMD" in
  check)
    judge
    if [ "$STATE" = free ]; then echo free; exit 0; fi
    echo "$STATE ${AGE}min $LINE"
    [ "$STATE" = live ] && exit 1
    exit 3
    ;;
  acquire)
    [ -n "$TASK" ] || usage
    mkdir -p "$VAULT/.state"
    judge
    case "$STATE" in
      free)
        if create "$TASK"; then echo acquired; exit 0; fi
        judge; stand_down ;;
      live)
        stand_down ;;
      stale|dead)
        OLD_STATE="$STATE"; OLD_LINE="$LINE"; OLD_AGE="$AGE"
        clear_judged
        if create "$TASK"; then
          log "**Lock**: $TASK cleared a $OLD_STATE lock ($OLD_LINE, touched $OLD_AGE min ago) and took it."
          echo "replaced $OLD_STATE"; exit 0
        fi
        judge; stand_down ;;
    esac
    ;;
  touch|release)
    [ -n "$TASK" ] || usage
    judge
    if [ "$STATE" = free ]; then echo "not holder: free" >&2; exit 2; fi
    if [ "$(holder)" != "$TASK" ]; then echo "not holder: $LINE" >&2; exit 2; fi
    if [ "$CMD" = touch ]; then touch "$LOCK"; else rm -f "$LOCK"; fi
    exit 0
    ;;
  *)
    usage ;;
esac
