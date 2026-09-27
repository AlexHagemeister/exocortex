# .state/ — pipeline bookkeeping

Skill-owned only: sweep cursors, ingest hash ledger, deleted-notes list, query-traffic log, lint reports and queue, digest compiles, review markers, system-review reports. Excluded from ingestion and from the bundle; never ships. Files here are working state, not knowledge — nothing in this folder is a source or a claim.

**issues/** — friction-log issue files, one per issue with `status` frontmatter; ISSUES.md at the vault root is their derived open-index (convention lives there). Resolved files stay as history.

**reviews/** — whole-system review reports, one per run; the score trend across them is the system's health curve.

**maintainer.lock**: advisory concurrency lock for maintainer runs (added 2026-07-16, user-approved). Take, heartbeat, release, and check it only through `.claude/scripts/lock.sh` (`acquire <task>`, `touch <task>`, `release <task>`, `check`), never by hand. Hand-written locks recorded a dead PID for a month (moot 2026-09-24), so the script owns the mechanics since 2026-09-26: the lock line, atomic acquisition, the liveness test (a dead recorded PID, or a lock untouched for 30 minutes, is residue it clears with a day-log note), and the "stood down, lock held by <holder>" day-log line a run leaves when it finds a live holder (added 2026-08-27, so held-lock frequency stays visible). The judgment stays with the run:

- **Who is bound:** every run of a skill that takes the lock, scheduled or interactive. Hand edits outside a skill are not bound, but run `lock.sh check` before bulk writes (2026-09-26, replacing "interactive sessions are not bound").
- **Heartbeat** (2026-09-24): run `lock.sh touch <task>` at every step boundary (per inbox item in process-inbox, per check in lint, before the commit in vault-snapshot) and at least every 10 minutes while working. The 30-minute window sits above the longest observed single step (25 minutes, 2026-09-23). If a step can run longer, touch inside it.
- **A live holder means stand down** and retry on the next schedule. Never wait on the lock in a loop.
- **Resumed runs re-check** (2026-08-17): a run resuming after an interruption runs `lock.sh touch <task>` before its next write and stands down if the script says it is no longer the holder, since interrupted runs are the usual way a lock outlives its owner.
- **Reporting writes are never lock-gated** (2026-08-17): a day-log entry or a new file in `.state/issues/` proceeds under any lock, because a run that stands down silently is indistinguishable from one that never fired. The exemption is safe because day-log entries go through `.claude/scripts/day-log.sh`, which only appends (2026-09-26).
