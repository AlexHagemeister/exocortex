---
name: vault-snapshot
description: Commit and push the vault's git history for diffs, recovery, and remote capture consumption. Run on schedule, before risky operations (migrations, bulk changes), or when the user asks for a backup.
---

# Vault snapshot — observational backup

The vault is itself a git repo; its remote holds the history: diffs, rollback, and the recovery source for expired pages. Device sync is Obsidian Sync, which ignores dotfolders and never touches `.git`. The snapshot is **observational only — never a gate**: nothing in the pipeline waits on it, and trust lives in the `status` field, not in merges. A deployment may run a mechanical hourly subset between full snapshots (bindings in `meta/DEPLOYMENT.md`); it halts rather than judges, so this run also sweeps up anything it left — unpushed work, scan hits, conflicts.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Acquire and release `.state/maintainer.lock` per the protocol in `.state/README.md` — never snapshot while another maintainer run holds the lock.

**Every run, interactive included**: if another run holds a fresh `.state/maintainer.lock` when you reach the commit step, do not `git add -A` — it would sweep that run's mid-flight tree into a commit whose message describes only your work, and diff-based recovery relies on commits meaning what they say. Wait for the lock to clear, or commit only the paths this session touched.

## Bindings

Read `meta/DEPLOYMENT.md` for the vault path and remote. **If the remote is UNSET, stop and ask the user** — do not guess, and do not create a repo in a default location.

**The vault must not live under iCloud or any file-sync layer that touches dotfolders** (Obsidian Sync is fine — it ignores them). If you find the vault inside such a sync layer, stop and tell the user.

## Procedure

1. **Consume remote captures.** If a remote MCP server is deployed (see `meta/DEPLOYMENT.md` → Remote MCP server), run its consumer script: it fetches the `inbox-drops` branch, copies pending capture files into the vault's `sources/inbox/`, and resets the branch to `main`. A missing branch or no pending captures is normal; a failed consume is reported in the run output and day log, never blocks the snapshot.
2. **Scan.** Check the working tree with the pattern below — this is its one home, so results are comparable run to run and local tooling reads it from here instead of keeping a copy. A hit never blocks the snapshot; commit as normal but report the hit loudly in the run output and the day log.

   <!-- Automation may parse the fenced block below at runtime and HALT if it can't read it — keep the fence and the CREDENTIAL_RE= form intact when editing. -->
   ```
   CREDENTIAL_RE=(^|[^A-Za-z0-9])(sk-([A-Za-z0-9]{20,}|(proj|svcacct)-[A-Za-z0-9_-]{40,})|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|AKIA[0-9A-Z]{16}|whsec_[A-Za-z0-9]{24,}|xoxb-[A-Za-z0-9-]{20,})|BEGIN [A-Z ]*PRIVATE KEY
   ```

   Real keys carry a long unbroken alphanumeric run; hyphenated slugs (`task-`, `risk-`, `disk-`) do not, which is what keeps the vault's own vocabulary out of the results even when written in inline code. Widen it only against evidence of a shape it actually missed.
3. **Commit.** `git add -A`, commit with message `snapshot <ISO 8601 timestamp>`. An empty diff is fine — commit nothing and log "no changes".
4. **Push.** `git pull --rebase` then `git push`. A rejected push retries once (pull-rebase again); a rebase conflict stops — report to the user, never resolve wiki content conflicts unattended. A failed push is logged, never blocks the run from finishing.
5. **Log.** One line in the day log (`wiki/log/<YYYY-MM-DD>.md`).

## Recovery (the one write-back)

When a deleted page is needed again (e.g., an expired connection the user wants back): retrieve it from git history (`git log --diff-filter=D`, `git show`), restore it through the normal write path (it re-enters as `draft` unless its prior status is being deliberately restored with the user's say-so), and log the recovery. History is never rewritten.
