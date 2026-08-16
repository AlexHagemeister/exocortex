---
name: obsidian-cli
what: Obsidian's official command-line interface as an interactive link-graph, schema-aggregation, and sync-recovery layer for vault maintenance
type: connector
requires: Obsidian desktop app with the vault open while the CLI runs; Obsidian Sync for the recovery commands only
effort: 2 minutes, one settings toggle
suggest_when: a link-graph question grep can't answer (alias-aware backlinks, orphan or broken-link sweeps), a frontmatter or tag schema-drift check across the whole vault, or content lost in the gap between vault snapshots
status: experimental
---

# Obsidian CLI: the link-graph and recovery layer

Obsidian ships an official CLI (`obsidian <command>`), enabled with one toggle in the desktop app under Settings → General; the command reference lives on Obsidian's help site (help.obsidian.md). It talks to the running app rather than parsing files itself, which is the whole point: file tools like grep see text, the CLI sees the vault the way Obsidian does, with wikilinks resolved, aliases honored, and tags and properties indexed. That makes it the only tool that can answer certain link-graph and schema questions in one call. It is not a replacement for file tools: in the vault where it was trialed, grep stayed first for content search, and the CLI earned its place in a narrower niche.

## Why this is here

Three uses earned the recommendation in real vault work:

1. **Link integrity, alias-aware.** The CLI's first sweep (`obsidian unresolved verbose`) caught a real rename casualty that plain grep passes had missed, because grep can't resolve wikilink aliases. It also taught the standing lesson that comes with the capability: investigate before fixing. Most dangling wiki links turned out to be intentional (known-missing markers, dated records, declared forward references); red links are often a designed backlog, not breakage.
2. **Schema-drift detection in one call.** `properties counts` and `tags counts` made frontmatter drift and tag-vocabulary junk visible across ~200 pages during a whole-system review, work that would otherwise take a custom script per question.
3. **Recovery between snapshots.** `sync:history`, `sync:deleted`, and `history:restore` reach Obsidian Sync's version history, the only layer that fills gaps between scheduled git snapshots.

The trial also mapped the limits, which the recipe states so you don't relearn them: the link graph is blind to frontmatter-only edges (a `depends_on:` entry produces no backlink), there are no multi-hop or algorithmic queries (a compiled graph layer does that better), and per-page `backlinks` dispatches to the app once per call, too slow for bulk tallies across hundreds of pages.

The larger unlock: an agent doing lint, audit, or post-ingest checking gets Obsidian's resolver as ground truth instead of approximating it with regexes, and the vault gains an undo layer independent of git.

## What you'll end up with

- **Link-integrity commands** for lint and audit passes, and for checking that a bulk ingest introduced no typo'd links: `unresolved`, `backlinks`, `orphans`, `deadends`, `aliases`.
- **Aggregation commands** for schema-drift checks: `properties counts sort=count`, `tags counts`.
- **Recovery commands** (Obsidian Sync required): `sync:history`, `sync:deleted`, `diff`, `history:restore`.
- **Odds and ends**: `random:read folder=wiki` for audit sampling, `outline`, `tasks`, `search:context`, `base:query`, and `eval` as an escape hatch.
- A usage note in the deployment's session context so agents actually reach for it at the right moments.

## Setup

What only the user can do:

1. Open Obsidian's Settings → General and enable the CLI. That is the whole install.

What the agent does:

2. Verify the binding with a harmless read command (see Verify below).
3. Add a usage note to the deployment's session context: CLAUDE.local.md while trialing (feature staging), CLAUDE.md if adopted. The note should name the niche commands and when to reach for them (link integrity during lint/audit/post-ingest, schema-drift checks, recovery), and carry the constraints:
   - The app must be running. Scheduled or unattended runs must never depend on the CLI.
   - Piping CLI output can hang; redirect to a file instead.
   - Links into dot-folders always report as unresolved (Obsidian doesn't index them); treat those as false positives.
   - Investigate dangling links before fixing them; intentional red links are common.
   - Never use `delete permanent`.
   - Content search stays with grep and file tools; the CLI is not a retrieval layer.

## Verify it works

With the app open on the vault, run `obsidian tags counts` with output redirected to a file. A populated result means the CLI is live. If the command errors, the app is closed or the toggle didn't take.
