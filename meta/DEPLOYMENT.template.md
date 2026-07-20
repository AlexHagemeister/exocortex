# DEPLOYMENT — environment bindings

Everything machine-, account-, or tool-specific lives here. Skills reference this file and never hardcode these values, so the program stays portable. Edit values here (this file is the user's; agents propose changes). Replace every UNSET before relying on the skills that read it.

| Binding | Value |
|---|---|
| Vault path | UNSET — absolute path to this vault on this machine |
| Sync layer | UNSET — device sync for the vault, e.g. Obsidian Sync, or none. **Must ignore dotfolders** (`.git/`, `.claude/`, `.state/` travel via git) — a layer that syncs or evicts them (iCloud, Dropbox) corrupts the repo. Note any per-file size limit. |
| Sync pinning | UNSET — if any synced location feeding the vault evicts files (iCloud does), pin it "Keep Downloaded" on every machine that touches it. Skills still defensively check for eviction placeholders. |
| Vault git repo | UNSET — the vault is itself a git repo; add a **private** remote for history, diffs, and recovery. Snapshots via `vault-snapshot` (commit + pull --rebase + push), non-blocking. |
| Program repo clone | UNSET — local path of the cloned program repo and its upstream URL. Updates pull here first, then apply via `bootstrap.sh --update`. |
| Remote MCP server | UNSET — optional remote capture endpoint; skills skip this when unset. |
| Scheduler / runner | UNSET — which machine runs scheduled maintainer tasks, and the schedule (suggested: process-inbox daily, lint weekly, digest weekly, vault-snapshot daily). |
| Unattended-run permissions | UNSET — where the machine-local permission allowlist lives (e.g. `.claude/settings.local.json`) so scheduled runs don't stall on prompts. Keep deletions out of the allowlist — those should always prompt. |
| Capture tool | UNSET — whatever drops files into sources/inbox/. The ingest validation gate applies regardless; the program assumes no particular capture tool. |
| Surfaces | UNSET — which surfaces act as maintainer (typically: Claude Code sessions opened in the vault) vs. read-only contributors via sources/inbox/ drops. |
| Staleness half-lives | life/infrastructure facts ~30d · conceptual pages ~180d (placeholders — tune from lint output) |

## Voice

How your maintainer talks to you. Written during setup (INSTALL.md § 1a), and yours to change anytime — edit this section directly, or tell the maintainer "be less formal" and it updates the spec for you. Delete the section to get the default (plain, technical, concise). **Scope: tone only.** Status labels, provenance, disputes, and corrections stay plain no matter what this section says — a warm maintainer must not round a `disputed` page up to reassurance.

Example spec (replace with yours):

- Register: casual and warm; contractions fine.
- Verbosity: short by default; expand only when asked.
- Humor: light and occasional — never in corrections, disputes, or failed checks.
- Emoji: none.
- Bad news (contradictions, failed lint, stale pages): direct, first line, no cushioning.
