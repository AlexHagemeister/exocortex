# SETUP — deploying an exocortex vault

Read [README.md](README.md) first for what the system is. This is the mechanical guide — if you'd rather have Claude Code walk you through it interactively, use [INSTALL.md](INSTALL.md) instead (one pasted prompt; the agent runs this guide for you).

## Prerequisites

- **[Claude Code](https://claude.com/claude-code)** — the maintainer agent. The skills in this repo register automatically when a session opens inside the vault.
- **A vault directory.** Any folder works. [Obsidian](https://obsidian.md) is a pleasant viewer (the note template uses [Templater](https://github.com/SilentVoid13/Templater) syntax), but nothing depends on it — the files are the interface.
- **A device-sync layer, if you want one — it must ignore dotfolders.** The vault is itself a git repo (step 4), and sync eviction and conflict resolution corrupt anything that syncs `.git/`. [Obsidian Sync](https://obsidian.md/sync) qualifies: it ignores `.git/`, `.claude/`, and `.state/` (those travel via git), though mind its per-file size limit (5 MB on the Standard plan — resize large images). iCloud, Dropbox, and default Syncthing do **not** qualify — never put the vault inside them. (The original vault started life in iCloud with a separate mirror repo and migrated out; the current architecture is the result.)

## 1. Clone and bootstrap

```sh
git clone <this repo>          # anywhere non-synced
cd exocortex
./tools/bootstrap.sh /path/to/your/vault
```

This scaffolds the folder skeleton (`sources/inbox/`, `notes/`, `wiki/`, `.state/`, `templates/`, `meta/`), installs the program files, and creates your `meta/DEPLOYMENT.md` from the template. It never overwrites existing files on a fresh run.

## 2. Fill in your deployment bindings

Open `<vault>/meta/DEPLOYMENT.md` and replace every UNSET row. This file is *yours* — machine paths, sync layer, git remote, scheduler. Skills read their environment from here and never hardcode it; it is the one file that must never be published.

## 3. Open Claude Code in the vault

Start a session in the vault directory. CLAUDE.md loads as the session's operating rules and the skills register. Sanity check: ask it *"what are your vault rules?"* — it should recite the zone table, not improvise.

## 4. Make the vault a git repo

The vault is itself a git repo; its history is your backup — diffs, rollback, recovery for expired pages. Snapshots are observational only, never a gate.

```sh
cd /path/to/your/vault
git init
printf '.obsidian/\n.state/maintainer.lock\n' >> .gitignore
```

Add a **private** remote, record it in `meta/DEPLOYMENT.md`, then ask the maintainer to run the `vault-snapshot` skill (commit + pull --rebase + push, daily). Your vault repo contains your personal data — it must never share a remote with a public repo.

## 5. Schedule the maintenance loop (optional but recommended)

Via Claude Code scheduled tasks (or any runner), on whatever machine you designate in DEPLOYMENT.md:

| Skill | Suggested cadence |
|---|---|
| `process-inbox` | daily |
| `vault-snapshot` | daily |
| `lint` | weekly |
| `digest` | weekly |

**Task prompts are pointers, not copies.** Every rule has exactly one home — the skill file in the vault — so a scheduled task must never paste skill text into its prompt (a copy silently drifts the first time the skill is amended). The whole prompt is a pointer:

> Unattended scheduled maintainer run for the exocortex vault at `/path/to/your/vault` — read CLAUDE.md at the vault root first (its rules bind the run), then work inside that directory and execute `.claude/skills/process-inbox/SKILL.md` exactly, including its unattended-runs rules. Everything normative lives in the vault, not here.

The "read CLAUDE.md first" instruction is deliberately in the prompt even though each maintenance skill's own unattended-runs line also demands it: a scheduled agent wakes up *without* the vault rules in context (unlike an interactive session opened in the vault, where CLAUDE.md auto-loads), and an agent that skips that read will improvise writes the rules forbid. State it in both places; it's the one duplication that pays for itself, and the skill line remains the normative home.

For unattended runs, also maintain a machine-local permission allowlist (e.g. `.claude/settings.local.json`) so scheduled runs don't stall on prompts — and deliberately leave deletions out of it, so those always prompt a human.

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
