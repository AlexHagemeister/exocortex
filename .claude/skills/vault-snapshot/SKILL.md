---
name: vault-snapshot
description: Commit and push the vault's git history for diffs, recovery, and remote capture consumption. Run on schedule, before risky operations (migrations, bulk changes), or when the user asks for a backup.
---

# Vault snapshot — observational backup

The vault is itself a git repo; its remote holds the history: diffs, rollback, and the recovery source for expired pages. Device sync is Obsidian Sync, which ignores dotfolders and never touches `.git`. The snapshot is **observational only — never a gate**: nothing in the pipeline waits on it, and trust lives in the `status` field, not in merges. A mechanical hourly subset (`snapshot-lite`, bindings in `meta/DEPLOYMENT.md`) may run between full snapshots; it halts rather than judges, so this run also sweeps up anything it left — unpushed work, scan hits, conflicts.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Acquire and release `.state/maintainer.lock` per the protocol in `.state/README.md` — never snapshot while another maintainer run holds the lock.

## Bindings

Read `meta/DEPLOYMENT.md` for the vault path and remote. **If the remote is UNSET, stop and ask the user** — do not guess, and do not create a repo in a default location.

**The vault must not live under iCloud or any file-sync layer that touches dotfolders** (Obsidian Sync is fine — it ignores them). If you find the vault inside such a sync layer, stop and tell the user.

## Procedure

1. **Consume remote captures.** If a remote MCP server is deployed (see `meta/DEPLOYMENT.md` → Remote MCP server), run its consumer script: it fetches the `inbox-drops` branch, copies pending capture files into the vault's `sources/inbox/`, and resets the branch to `main`. A missing branch or no pending captures is normal; a failed consume is reported in the run output and day log, never blocks the snapshot.
2. **Scan.** Check the working tree for credential-shaped strings (e.g. `sk-`, `ghp_`, `AKIA`, `whsec_`, private-key blocks) — a hit never blocks the snapshot; commit as normal but report the hit loudly in the run output and the day log.
3. **Commit.** `git add -A`, commit with message `snapshot <ISO 8601 timestamp>`. An empty diff is fine — commit nothing and log "no changes".
4. **Push.** `git pull --rebase` then `git push`. A rejected push retries once (pull-rebase again); a rebase conflict stops — report to the user, never resolve wiki content conflicts unattended. A failed push is logged, never blocks the run from finishing.
5. **Log.** One line in the day log (`wiki/log/<YYYY-MM-DD>.md`).

## Recovery (the one write-back)

When a deleted page is needed again (e.g., an expired connection the user wants back): retrieve it from git history (`git log --diff-filter=D`, `git show`), restore it through the normal write path (it re-enters as `draft` unless its prior status is being deliberately restored with the user's say-so), and log the recovery. History is never rewritten.
