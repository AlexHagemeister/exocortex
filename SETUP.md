# SETUP — deploying an exocortex vault

Read [README.md](README.md) first for what the system is. This is the mechanical guide.

## Prerequisites

- **[Claude Code](https://claude.com/claude-code)** — the maintainer agent. The skills in this repo register automatically when a session opens inside the vault.
- **A vault directory.** Any folder works. [Obsidian](https://obsidian.md) is a pleasant viewer (the note template uses [Templater](https://github.com/SilentVoid13/Templater) syntax), but nothing depends on it — the files are the interface.
- **A sync layer, if you want one** (iCloud, Syncthing, …). One hard rule if you use one: **never put a git repo inside a sync-managed folder.** Sync eviction and conflict resolution corrupt repos. Git lives outside the vault (step 4). If your sync layer evicts files (iCloud does), pin the vault "Keep Downloaded" on every machine.

## 1. Clone and bootstrap

```sh
git clone <this repo>          # anywhere non-synced
cd exocortex
./tools/bootstrap.sh /path/to/your/vault
```

This scaffolds the folder skeleton (`sources/inbox/`, `notes/`, `wiki/`, `.state/`, `templates/`, `meta/`), installs the program files, and creates your `meta/DEPLOYMENT.md` from the template. It never overwrites existing files on a fresh run.

## 2. Fill in your deployment bindings

Open `<vault>/meta/DEPLOYMENT.md` and replace every UNSET row. This file is *yours* — machine paths, sync layer, mirror location, scheduler. Skills read their environment from here and never hardcode it; it is the one file that must never be published.

## 3. Open Claude Code in the vault

Start a session in the vault directory. CLAUDE.md loads as the session's operating rules and the skills register. Sanity check: ask it *"what are your vault rules?"* — it should recite the zone table, not improvise.

## 4. Set up the private mirror

The mirror is a separate git repo holding your vault's history — diffs, rollback, recovery for expired pages. It is observational only, never a gate.

```sh
git init ~/your-vault-mirror        # non-synced path; NOT inside the vault
```

Record the path in `meta/DEPLOYMENT.md`, optionally add a **private** remote, then ask the maintainer to run the `mirror-snapshot` skill. Your mirror will contain your personal data — it must never share a remote with a public repo.

## 5. Schedule the maintenance loop (optional but recommended)

Via Claude Code scheduled tasks (or any runner), on whatever machine you designate in DEPLOYMENT.md:

| Skill | Suggested cadence |
|---|---|
| `process-inbox` | daily |
| `mirror-snapshot` | daily |
| `lint` | weekly |
| `digest` | weekly |

For unattended runs, maintain a machine-local permission allowlist (e.g. `.claude/settings.local.json`) so scheduled runs don't stall on prompts — and deliberately leave deletions out of it, so those always prompt a human.

## 6. Set up frictionless capture

The inbox is multi-tenant: *any* tool that drops a markdown file into `sources/inbox/` works, and the ingest validation gate applies regardless. That said, the smoothest setup we know is the [Obsidian Web Clipper](https://obsidian.md/clipper) (free browser extension for Chrome, Firefox, Edge, and Safari — including Safari on iOS), configured once so every clip lands ingest-ready:

- **Save location.** Point the clipper at your vault with note location `sources/inbox/`. Clips then flow through the normal pipeline on the next `process-inbox` run — no manual filing.
- **A capture template with provenance built in.** The wiki cites provenance forever, so capture it at clip time. Add frontmatter properties to your clipper template: `title: {{title}}`, `source: {{url}}`, `author: {{author}}`, `published: {{published}}`, `clipped: {{date}}`. Use a date-prefixed note name (ingest files sources as `YYYY-MM-DD-title-slug.md`, so arriving that way helps).
- **Clip the content, not the link.** The ingest gate quarantines empty or boilerplate-only clips. Capture the full article body (the clipper converts it to clean markdown), or use **highlight capture** to clip just the passages that matter — both are substantive; a bare URL is not.
- **Template triggers.** The clipper can auto-select a template by site — useful if you want, say, recipes or papers pre-tagged toward different wiki folders while everything still routes through the same inbox.
- **Interpreter (optional LLM tidy pass).** The clipper's Interpreter feature runs your clip through a model you configure (your own API key — Anthropic, OpenAI, or a local model) to strip boilerplate, summarize, or extract fields per your template prompts. A tidier clip sails through ingest validation; the gate stays in place either way, so this is polish, not a requirement.

Record whatever you choose in the **Capture tool** row of `meta/DEPLOYMENT.md`.

## 7. Use it

- **Capture:** clip from the browser (above), or drop anything (meeting notes, statements, exports) as files into `sources/inbox/`, then run `process-inbox` — or just tell the maintainer "remember this."
- **Write:** your `notes/` are yours alone; the sweep picks up changes without ever editing your words.
- **Ask:** the `query` skill answers from the vault with status-weighted citations.
- **Review:** the weekly `digest` is your curation surface — promote drafts, adjudicate disputes, review friction. Promotion to `verified` is the one job that stays human.

## Updating an existing deployment

When this repo updates:

```sh
git pull
./tools/bootstrap.sh /path/to/your/vault --update
```

`--update` overwrites the **program files only** (CLAUDE.md, CONSTITUTION.md, skills, meta reference docs) and never touches your data or your `meta/DEPLOYMENT.md`. If you've locally amended rules via the `amend` skill, diff before pulling — your local amendments are yours to keep or reconcile.

## Publishing your own fork (maintainers of the program)

`tools/sync.sh` pulls the portable system files from a private vault into this repo, gated by [MANIFEST](MANIFEST) (an explicit allowlist — nothing outside it is ever copied) and a leak scan. It needs two gitignored local files (`tools/publish.local.conf`, `tools/leak-patterns.local.txt` — see the `.example`), and `sync.sh --push` refuses to push to any remote that doesn't match your configured public repo. Most deployments never need this — it's the vault-to-repo publishing path, not the install path.
