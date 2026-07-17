# .state/ — pipeline bookkeeping

Skill-owned only: sweep cursors, ingest hash ledger, query-traffic log, lint reports, digest review markers. Excluded from ingestion and from the bundle; never ships. Files here are working state, not knowledge — nothing in this folder is a source or a claim.

**issues/** — friction-log issue files, one per issue with `status` frontmatter; ISSUES.md at the vault root is their derived open-index (convention lives there). Resolved files stay as history.

**maintainer.lock** — advisory concurrency lock for scheduled maintainer runs (added 2026-07-16, user-approved). A running scheduled task writes `<task-name> <ISO 8601 timestamp>` here at start and deletes it at end; other scheduled runs seeing a lock under 2 hours old stand down and retry on their next schedule; a lock 2+ hours old is treated as a crashed run's residue and replaced (with a log note). Interactive sessions are not bound by the lock but should be aware of it.
