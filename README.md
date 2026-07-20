# exocortex

An agent-maintained personal knowledge system, shipped as pure markdown.

An **exocortex** is one vault playing three roles at once: a *research brain* (compiled knowledge of the world), a *memory brain* (compiled knowledge of your work and life), and an *agent substrate* (the context that lets an AI agent act as a colleague rather than a smart stranger). You drop sources in and write notes; an AI maintainer — Claude Code, running a small set of skills — compiles them into a wiki with epistemic guardrails built into every write path.

This repository is the **program**: the rules, principles, and skill procedures that govern the maintainer, plus setup tooling. It contains no personal data. Your knowledge — sources, notes, the compiled wiki — stays in your own vault (itself a git repo with a private remote, if you keep history). The two never mix: the boundary is defined in [CONSTITUTION.md](CONSTITUTION.md) § *Sharing and boundaries*.

**Lineage:** Karpathy's LLM-wiki pattern (Apr 2026) → Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog) v0.1 (Jun 2026) → this system.

## How it works

- **One write pipeline.** Knowledge enters the wiki only through `sources/inbox/`, a sweep of your notes, or a skill. No ad-hoc writes.
- **Sources are frozen speech.** A source is a record of what was said, never edited — truth-status lives one layer up, in the wiki, where claims can be disputed and retracted without falsifying the record. Corrections arrive as *new* sources, even when they come from you.
- **Trust is graduated, not gated.** The agent writes freely as `draft`; promotion to `verified` is a human act; every reader weights pages by status. A mostly-draft wiki is healthy by design.
- **Rules live where they bind.** Invariants in [CLAUDE.md](CLAUDE.md) (one page, hard budget), procedures in [.claude/skills/](.claude/skills/), folder law in each folder's README, principles in [CONSTITUTION.md](CONSTITUTION.md). No rule lives twice.
- **The system is its own tester.** Friction gets filed as issues ([ISSUES.md](ISSUES.md)); repeated rule overrides trigger amendment proposals; a weekly digest surfaces everything for human review. The rules are a pact you authored and may renegotiate — never a cage.

The maintainer's skill set: `ingest` · `process-inbox` · `session-capture` · `query` · `lint` · `digest` · `vault-snapshot` · `amend`.

## What's in this repo

| Path | What it is |
|---|---|
| [CLAUDE.md](CLAUDE.md) | The one-page invariant core every agent session loads |
| [CONSTITUTION.md](CONSTITUTION.md) | Principles, roles, anti-patterns, residence map |
| [.claude/skills/](.claude/skills/) | The eight maintainer skill procedures |
| [ISSUES.md](ISSUES.md), [.state/README.md](.state/README.md) | Friction-log and bookkeeping conventions |
| [templates/](templates/) | Note frontmatter template |
| [meta/](meta/) | Reference docs: the design doctrine and build handoff (historical), the pinned OKF spec, and the deployment-bindings template |
| [SETUP.md](SETUP.md), [tools/](tools/) | Deployment guide, vault bootstrap script, and the maintainer's publish tooling |

## Deploying your own

You need [Claude Code](https://claude.com/claude-code) and a directory for your vault ([Obsidian](https://obsidian.md) makes a nice viewer, but the files are the interface). Then:

```sh
git clone <this repo>   # somewhere NOT managed by iCloud/Dropbox/etc.
cd exocortex
./tools/bootstrap.sh /path/to/your/vault
```

…and follow [SETUP.md](SETUP.md) from there: fill in your `meta/DEPLOYMENT.md` bindings, git-init the vault with a private remote, optionally schedule the maintenance skills, and start dropping things into `sources/inbox/`. For everyday capture, the [Obsidian Web Clipper](https://obsidian.md/clipper) pointed straight at your inbox — with a provenance-carrying template and its optional LLM tidy pass — makes clipping a one-click act; SETUP.md § 6 has the exact configuration.

## License

The system files are MIT-licensed ([LICENSE](LICENSE)). The pinned copy of the OKF spec ([meta/OKF-SPEC.md](meta/OKF-SPEC.md)) is from Google's [knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog) repository, Apache 2.0.
