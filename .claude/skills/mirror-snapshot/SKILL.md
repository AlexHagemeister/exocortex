---
name: mirror-snapshot
description: Snapshot the vault into its external git mirror for history, diffs, and recovery. Run on schedule, before risky operations (migrations, bulk changes), or when the user asks for a backup.
---

# Mirror snapshot — observational backup

The mirror is a separate, non-iCloud git repo holding the vault's history: diffs, rollback, and the recovery source for expired pages. It is **observational only — never a gate**: nothing in the pipeline waits on it, and trust lives in the `status` field, not in merges.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Acquire and release `.state/maintainer.lock` per the protocol in `.state/README.md` — never snapshot while another maintainer run holds the lock.

## Bindings

Read `meta/DEPLOYMENT.md` for the mirror repo path. **If it is UNSET, stop and ask the user** which machine and path should host it — do not guess, and do not create a repo in a default location.

**Git and iCloud must not cohabit.** Never run `git init` inside the vault, and never place the mirror anywhere iCloud (or another sync layer) manages — eviction and conflict behavior corrupt repos. If you find a `.git/` inside the vault, stop and tell the user.

## Procedure

1. **Eviction pre-check.** Scan the vault for `.<name>.icloud` placeholders (`find <vault> -name '.*.icloud'`). Placeholders mean iCloud evicted those files — a snapshot taken now silently omits their content. Force-download first (`brctl download <path>` per file, then wait and re-check), and if content still isn't local, **refuse the snapshot** and tell the user to pin the vault ("Keep Downloaded" in Finder).
2. **Consume remote captures.** If a remote MCP server is deployed (see `meta/DEPLOYMENT.md` → Remote MCP server), run its consumer script: it fetches the mirror's `inbox-drops` branch, copies pending capture files into the vault's `sources/inbox/`, and resets the branch to `main`. This runs before the copy so captures enter this snapshot and are not clobbered by the `--delete` pass. A missing branch or no pending captures is normal; a failed consume is reported in the run output and day log, never blocks the snapshot.
3. **Copy.** `rsync -a --delete` the vault into the mirror repo's working tree, excluding `.obsidian/` (app cache/config, not knowledge), any `.git/`, and `.state/maintainer.lock` (transient run-state, meaningless in a snapshot).
4. **Commit.** In the mirror repo: first scan the copied tree for credential-shaped strings (e.g. `sk-`, `ghp_`, `AKIA`, `whsec_`, private-key blocks) — a hit never blocks the snapshot; commit as normal but report the hit loudly in the run output and the day log. Then `git add -A`, commit with message `snapshot <ISO 8601 timestamp>`, then `git push` if a remote is configured — a failed push is logged, never blocks. An empty diff is fine — commit nothing and log "no changes".
5. **Log.** One line in the day log (`wiki/log/<YYYY-MM-DD>.md`).

## Recovery (the one write-back)

When a deleted page is needed again (e.g., an expired connection the user wants back): retrieve it from mirror history (`git log --diff-filter=D`, `git show`), restore it through the normal write path (it re-enters as `draft` unless its prior status is being deliberately restored with the user's say-so), and log the recovery. The mirror itself is never edited by hand.
