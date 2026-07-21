# exocortex

An agent-maintained personal knowledge system, shipped as pure markdown.

**TL;DR** — You capture things (articles, meeting notes, decisions, stray thoughts) and write notes however you already do. An AI maintainer compiles all of it into a personal wiki: cross-linked, provenance-tracked, and marked with how much each claim can be trusted. Your knowledge compounds instead of rotting in a pile of notes — and any agent you work with inherits the context to act like a colleague who's been in the room for years, not a smart stranger meeting you fresh every session. It's all markdown in a folder you own; no app, no database, no lock-in.

## Quick start

Paste this into [Claude Code](https://claude.com/claude-code) — or whatever coding agent you use — with this repo's URL filled in:

> Clone `<this repo's URL>`, read its INSTALL.md, and help me set up my own exocortex vault on this machine.

That's the install. The agent interviews you (vault location, sync, private remote, scheduling), runs the setup, fills in your deployment bindings, and smoke-tests the pipeline before handing you the keys. [INSTALL.md](INSTALL.md) is its script; [SETUP.md](SETUP.md) is the same procedure as a manual guide. Updating later is the same move — one prompt to your agent; releases are announced in [CHANGELOG.md](CHANGELOG.md) (watch the repo to get notified). (Claude Code is the maintainer runtime the system is built for — the skills register automatically in its vault sessions — but any capable agent can run the install.)

## What you get

- **A wiki that writes itself.** Drop a source in the inbox and the maintainer files it, summarizes it, links it to what you already know, and updates the pages it affects. You never organize anything by hand.
- **Answers with receipts.** Ask a question and the `query` skill answers from *your* accumulated knowledge, citing the pages and sources behind every claim — weighted by how verified each one is.
- **An honest knowledge base.** Every claim is traceable to who said it and when. Machine inferences are labeled as inferences. Contradictions get flagged as disputes instead of silently overwritten. A guess never wears the typography of a fact.
- **Agents with real context.** The vault doubles as an agent substrate: any session opened inside it knows your projects, your people, your history, and your rules. This is the difference between delegating to a colleague and re-briefing a stranger.
- **Your words stay yours.** The maintainer never edits your notes — it reads them, links to them, and compiles from them. Sources are frozen records; corrections arrive as new statements, never rewrites of old ones.
- **Rules you can renegotiate.** The whole system runs on legible markdown rules (you're looking at them). When a rule chafes, the `amend` skill changes it — with your approval, logged, reversible.

## What using it feels like

**Capture without ceremony.** Clip an article from your browser, drop a meeting transcript in the inbox, or just tell the agent "remember this" mid-conversation. Provenance is recorded at capture time; nothing needs tidying first. Bringing years of notes from another app? There's a migration workflow for that — batched and review-paced ([SETUP.md § 8](SETUP.md)).

**Maintenance happens while you're not looking.** Scheduled runs drain the inbox, sweep your notes for changes, snapshot history to a private git remote, and lint the wiki for contradictions and staleness. You wake up to a vault that's more organized than you left it.

**You stay the editor-in-chief.** A periodic digest surfaces what needs human eyes: new connections the agent proposed, disputes it found, drafts worth promoting. Reviewing it takes minutes; promoting a page to `verified` is deliberately a human act. Curation is the one job the system refuses to automate — what enters and what gets trusted is yours to decide, and the system's quality is bounded by exactly that.

**You ask, it knows.** Months later, "what did we decide about X, and why?" gets an answer with the decision, the reasoning, the source, and the date — because the system was built for the retrieval moment, not the filing moment.

## Why this is an unlock

LLMs reset every session; your context doesn't survive the conversation. Notes apps have the opposite problem: everything survives, nothing is synthesized, and the pile grows less useful as it grows. This system closes the loop between the two — machine labor does the synthesis continuously, epistemic guardrails keep the result trustworthy, and the whole thing lives in files any agent can read. The payoff compounds: every captured source makes the wiki smarter, and every agent session starts from everything you've ever fed it.

**Lineage:** Karpathy's LLM-wiki pattern (Apr 2026) → Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog) v0.1 (Jun 2026) → this system.

## How it works

This repository is the **program**: the rules, principles, and skill procedures that govern the maintainer, plus setup tooling. It contains no personal data. Your knowledge — sources, notes, the compiled wiki — stays in your own vault (itself a git repo with a private remote, if you keep history). The two never mix: the boundary is defined in [CONSTITUTION.md](CONSTITUTION.md) § *Sharing and boundaries*.

- **One write pipeline.** Knowledge enters the wiki only through `sources/inbox/`, a sweep of your notes, or a skill. No ad-hoc writes.
- **Sources are frozen speech.** A source is a record of what was said, never edited — truth-status lives one layer up, in the wiki, where claims can be disputed and retracted without falsifying the record. Corrections arrive as *new* sources, even when they come from you.
- **Trust is graduated, not gated.** The agent writes freely as `draft`; promotion to `verified` is a human act; every reader weights pages by status. A mostly-draft wiki is healthy by design.
- **Rules live where they bind.** Invariants in [CLAUDE.md](CLAUDE.md) (one page, hard budget), procedures in [.claude/skills/](.claude/skills/), folder law in each folder's README, principles in [CONSTITUTION.md](CONSTITUTION.md). No rule lives twice.
- **The system is its own tester.** Friction gets filed as issues ([ISSUES.md](ISSUES.md)); repeated rule overrides trigger amendment proposals; a weekly digest surfaces everything for human review. The rules are a pact you authored and may renegotiate — never a cage.

The maintainer's skill set: `ingest` · `process-inbox` · `session-capture` · `query` · `lint` · `digest` · `vault-snapshot` · `amend`.

## Key terms

- **program** — shippable system markdown per MANIFEST: rules, skills, glossary, and supporting conventions; no personal data.
- **bundle** — wiki/ alone, OKF-conformant export surface; not the vault and not the program.
- **vault** — the whole personal knowledge installation: sources, notes, wiki, attachments, and pipeline bookkeeping.
- **wiki** — agent-maintained compiled knowledge layer in wiki/; claims carry status and provenance.
- **ingest** — skill that files a source and compiles it into wiki pages.
- **digest** — skill that compiles the user-facing review surface from pipeline output.
- **lint** — skill that runs vault health checks and queues fixes.
- **draft** — wiki status: hypothesis-grade; usable but say so when it matters.
- **verified** — wiki status: human-promoted ground truth; scarce by design.
- **provenance** — traceable origin of a claim (source path, URL, or the user's dated words).

Full glossary → [GLOSSARY.md](GLOSSARY.md)

## What's in this repo

| Path | What it is |
|---|---|
| [CLAUDE.md](CLAUDE.md) | The one-page invariant core every agent session loads |
| [CONSTITUTION.md](CONSTITUTION.md) | Principles, roles, anti-patterns, residence map |
| [GLOSSARY.md](GLOSSARY.md) | Canonical system vocabulary (term meanings, not procedures) |
| [.claude/skills/](.claude/skills/) | The maintainer skill procedures |
| [ISSUES.md](ISSUES.md), [.state/README.md](.state/README.md) | Friction-log and bookkeeping conventions |
| [templates/](templates/) | Note frontmatter template |
| [meta/](meta/) | Reference docs: the design doctrine and build handoff (historical), the pinned OKF spec, and the deployment-bindings template |
| [INSTALL.md](INSTALL.md) | Agent-guided setup — paste one prompt into your coding agent and it installs the system |
| [SETUP.md](SETUP.md), [tools/](tools/) | Manual deployment guide, vault bootstrap script, and the maintainer's publish tooling |

## Deploying by hand

The [Quick start](#quick-start) above is the recommended path. To do it yourself instead ([Obsidian](https://obsidian.md) makes a nice viewer, but the files are the interface):

```sh
git clone <this repo>   # somewhere NOT managed by iCloud/Dropbox/etc.
cd exocortex
./tools/bootstrap.sh /path/to/your/vault
```

…and follow [SETUP.md](SETUP.md) from there: fill in your `meta/DEPLOYMENT.md` bindings, git-init the vault with a private remote, optionally schedule the maintenance skills, and start dropping things into `sources/inbox/`. For everyday capture, the [Obsidian Web Clipper](https://obsidian.md/clipper) pointed straight at your inbox — with a provenance-carrying template and its optional LLM tidy pass — makes clipping a one-click act; SETUP.md § 6 has the exact configuration.

## License

The system files are MIT-licensed ([LICENSE](LICENSE)). The pinned copy of the OKF spec ([meta/OKF-SPEC.md](meta/OKF-SPEC.md)) is from Google's [knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) repository, Apache 2.0.
