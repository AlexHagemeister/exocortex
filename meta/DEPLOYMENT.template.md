# DEPLOYMENT — environment bindings

Everything machine-, account-, or tool-specific lives here. Skills reference this file and never hardcode these values, so the program stays portable. Edit values here (this file is the user's; agents propose changes). Replace every UNSET before relying on the skills that read it.

| Binding | Value |
|---|---|
| Vault path | UNSET — absolute path to this vault on this machine |
| Sync layer | UNSET — e.g. iCloud, Syncthing, Dropbox, or none. **No git repo may live inside a sync-managed vault** — eviction/conflict behavior corrupts repos. |
| Sync pinning | UNSET — if the sync layer evicts files (iCloud does), pin the vault "Keep Downloaded" on every machine that touches it. Skills still defensively check for eviction placeholders. |
| Git mirror repo | UNSET — non-synced local path for the vault's git mirror (history, diffs, recovery). Remote optional; snapshots push after commit, non-blocking. |
| Remote MCP server | UNSET — optional remote capture endpoint; skills skip this when unset. |
| Scheduler / runner | UNSET — which machine runs scheduled maintainer tasks, and the schedule (suggested: process-inbox daily, lint weekly, digest weekly, mirror-snapshot daily). |
| Unattended-run permissions | UNSET — where the machine-local permission allowlist lives (e.g. `.claude/settings.local.json`) so scheduled runs don't stall on prompts. Keep deletions out of the allowlist — those should always prompt. |
| Capture tool | UNSET — whatever drops files into sources/inbox/. The ingest validation gate applies regardless; the program assumes no particular capture tool. |
| Surfaces | UNSET — which surfaces act as maintainer (typically: Claude Code sessions opened in the vault) vs. read-only contributors via sources/inbox/ drops. |
| Staleness half-lives | life/infrastructure facts ~30d · conceptual pages ~180d (placeholders — tune from lint output) |
