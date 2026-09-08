# Changelog

Notable changes to the exocortex program, per release. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/) — pre-1.0, a patch means nothing behaves differently after updating (fixes, wording, restructuring); a minor means the maintainer will do something it didn't do before, so read the notes before updating.

To update an installed vault, tell your maintainer "update my exocortex" (the `update-exocortex` skill) — or see [SETUP.md § Updating](SETUP.md#updating-an-existing-deployment) for the by-hand path. Watch this repo (Watch → Custom → Releases) to be notified of new versions.

## [Unreleased]

## [0.14.0] — 2026-09-07

### Added
- **CLAUDE.md § Reporting to the user.** Six rules for every message that reports work: observation and inference separated by structure, fidelity to the record (absence is absence of record, quotes are verbatim or not called quotes), the plain version of a decision before any system vocabulary, name-with-context for anything the user has not seen this session, judgment calls reported with their reasoning, and a stated model plus a found contradiction is a fix rather than a question. The judgment-call trigger is sharpened to "another reasonable agent could have decided otherwise."
- **CLAUDE.md opens with a letter to the agent** ("Hello", "Who you are"): the Curator's framing of what the maintainer is for, ahead of the operating rules.
- **`sources/research/` stream**: the agent's own compiled findings from external surfaces (web research passes, live-page reads, verification sweeps), distinct from articles/ (external material) and sessions/ (conversation). Named in ingest's filing rule and the sources/ README; its folder-law README ships.
- **Lint check 11, the entropy scorecard** (report only): instruction-layer lines, enforcement-script count, and open issues, compared against the previous report each run, so an amendment that adds prose without retiring any is visible as a trend. Check 0 also reports pages still carrying the retired `sources:`/`depends_on:` fields, and will run a claim extractor read-only where a deployment carries one (quote-provenance findings become parser-grade there; without one, that finding class is skipped and nothing else degrades).
- **Digest**: a lint recency gate before compiling (run lint first, or open with the queue's age); a quarantined-captures section (2b) so nothing sits in `sources/inbox/quarantine/` unseen; judgment calls may be presented grouped by pattern with one verdict per group; and the decision item shape is now law: the thing linked, the problem, the fix, a default with one line of reasoning, and what happens on no action.
- **Session capture**: the agent may capture unprompted when a session produced a decision, ruling, or durable fact, announcing it before the session ends so the user can veto; captures record the harness `session_id` when one is exposed; a closing `# Ingest brief` section carries the routing knowledge (which pages, which claims superseded) while the capturing agent still holds it, and ingest reads it as a recommendation to verify, never an override.
- **`ingest-file.sh` exit 4**: refuses to file a capture that names a sibling by its `sources/inbox/` path (a dead pointer the moment either file is filed); `--allow-inbox-paths` for a legitimate mention such as a verbatim quote.
- **ISSUES.md recurrence convention**: a `## Recurrence <date>` block appended to an open issue's body, never editing what is above it, so "N recurrences" close conditions can mature.
- **`maintainer.lock` carries the holder's PID** and a `kill -0` liveness check: a dead holder's lock is cleared with a day-log note instead of waiting out the two-hour age rule; a run that stands down writes one day-log line saying so.
- **Chronicle**: collectors are launched in the foreground, all in one message, so their reports reach the compiler and not whichever session is live when they finish; collectors report timestamps as the source rendered them with the zone named, and conversion happens once at compile time; a failed tool retries once then reports the surface as unreached, never as empty; subject attribution is itself an inference (a record of unidentified speakers never defaults a first-person claim to the user).
- **`wiki/log/` links are frozen with their entries**: a dead link in a day log is dated history, so page moves skip the folder and lint's dangling count excludes it.
- **Amend**: proposals name a hook alongside or instead of prose when a rule is mechanically checkable, with the test for when a hook is the wrong home; the retirement split (when enforcement ships, the same amendment shrinks the prose to a pointer); a watch issue may track several changes only with a close condition per item; the issue-cluster threshold matches on rule components inside `rule:` values, not whole-string equality.
- **CONSTITUTION residence map** gains a row for the substrate scripts: read `.claude/scripts/` before asserting the vault lacks some machinery, since rule surfaces bind behavior and never inventory capability.
- **Two cookbook recipes**: `em-dash-hook.md` (a PostToolUse hook that catches an em dash at write time, for any project with that style rule) and `ios-inbox-shortcuts.md` (two iPhone Shortcuts that drop a dated, provenance-stamped note into `sources/inbox/`, no AI in the loop).

### Changed
- **Ingest organizes pages by subject, never by source.** A source updates the pages that own its subjects, cited inline; a new page is written only for a subject no page owns or one the user flags for a deep pass. One-page-per-source and its attachment-set exception are retired (the term now names a filing shape). Also: the born-verified exception narrows to a verbatim **verdict, ruling, or correction** (first-pass information in the user's words is born draft); structural satellite names (index, README, a bundle design's fixed satellites) are exempt from the creation-time uniqueness gate; the first mention of any person, entity, or project with a page is a wikilink; the `## Unreviewed additions` section exists only on verified pages (a demotion folds it into the body); an unattended compaction queues a one-line digest notice; blockquote citation lines use an en dash (the em dash form is grandfathered).
- **Audit corrections always route through the inbox**: the single-home shortcut that allowed a direct page edit is gone, and CLAUDE.md § Corrections binds unconditionally.
- **Process-inbox**: the notes sweep ignores `README.md` and `SKILL.md` anywhere under `notes/` (repo scaffolding, not notes); `#no-ingest` notes still appear in `notes/index.md`, since the opt-out gates the wiki, not the user's browsing surface; "conservative" in unattended runs means following each skill's procedure, never skipping a step the owning skill runs unattended.
- **Query** syntheses carry a `scope:` field like every other page.
- **Folder law**: an artifact evidences its own existence and where attention was (as inference), never what anyone said; a cookbook recipe likewise; `sources/meetings/` treats a tool-generated summary block as evidence only that the tool produced it; `sources/sessions/` holds the user's own typed or dictated statements (a conversation of one); `wiki/craft/` drops its link-direction rule (a project may be linked as evidence); `wiki/projects/` records that uniform satellite naming is a convention justified per use, not a mandate. Folder README titles use the colon form.
- **Five shipped skills describe deployment boundaries without naming deployment-private files** (lint, amend, ingest, digest, update-exocortex), matching the 2026-08-31 fix for audit-exocortex and vault-snapshot.
- **README** drops the recipe and script counts from the cookbook and repo-map rows (they drifted twice) and points at the folders for the current list.
- **`regen-index.py` and `regen-issues.py`** stamp `updated:` with date and 12-hour time; `regen-index.py` unescapes quoted frontmatter values. **`vault_graph.py`** resolves a bare name that matches a vault-root file to that file (not a collision). **`notes-cursor-diff.py`** matches the sweep exclusion above.
- **MANIFEST** private block now lists every deployment-local trial explicitly (claim conventions, email triage, school brief, the seven enforcement hooks, register, spaced repetition, and two utilities).

### Migration note
- Subject-organized ingest applies to pages written from now on; nothing reorganizes an existing vault's per-source pages. The `maintainer.lock` PID format is backward compatible (a two-field lock falls back to the age rule).

## [0.13.0] — 2026-08-26

### Added
- **Chronicle graduates from pilot to cookbook recipe** (`meta/cookbook/chronicle.md`, experimental). The `chronicle` skill and `wiki/chronicle/README.md` folder law now ship; the feature stays opt-in — nothing runs until you follow the recipe (create the folder, author your surface registry at `meta/chronicle-surfaces.md`, add the step to your maintenance chain). New GLOSSARY entry **chronicle**.
- **Top-of-mind session import is pre-wired.** Shipped CLAUDE.md now carries the `@artifacts/top-of-mind.md` import — inert until the file exists, so nothing changes for deployments without one. The recipe (`meta/cookbook/top-of-mind-file.md`) drops its wiring step and gains two maintenance rules: an update is a sweep, not an append (prune passed entries before stamping `updated:`), and entries that grow state belonging on their linked hub are drift to push back out.
- **Digest-nudge recipe** (`meta/cookbook/digest-nudge.md`, recommended) with its shipped script `.claude/scripts/digest-nudge.sh`: a SessionStart hook that stays completely silent until the gap since the last completed digest review passes a threshold (default 7 days), then tells the agent once, at session start, to gently offer the digest. Deterministic, zero context cost under threshold, reads the review markers the digest skill already writes.
- **Message-timestamp hook recipe** (`meta/cookbook/message-timestamps.md`, recommended, referenced from SETUP.md § 6). One `UserPromptSubmit` hook running `date`, so every user message re-anchors the agent's clock and dated writes stop drifting in long sessions. One settings edit, zero maintenance; existing deployments can ask their maintainer to apply it.
- **Obsidian CLI enablement is now a setup step** (SETUP.md § 5). Existing Obsidian deployments: toggle it on (Settings → General) so lint, audit, and snapshot recovery use Obsidian's own link resolver instead of the fallbacks. One toggle, under a minute; details in `meta/cookbook/obsidian-cli.md`.
- **`wiki/agent/` joins the shipped scaffold**: agent capability self-knowledge and operating instructions: what the agent's tools and surfaces can do on a deployment, and how it should perform recurring tasks. The folder-law README ships (admission rules, the boundary with `craft/`, with skills, and with the rules layer); pages accrue per deployment through the pipeline. Bootstrap scaffolds the folder with a derived-listing index stub (entities/ gains its missing stub in the same pass).
- **Claim-neutrality guard scripts ship**: `.claude/scripts/compaction-guard.py` (the mechanical half of ingest's compaction guard, previously a shipped-ingest dependency that did not ship) and `.claude/scripts/style-sweep-guard.py` (the bulk style-sweep check that links, dates, quotes, and numbers survive a rewrite).

### Changed
- **CLAUDE.md opens with a deployed-vault check**: a session started in the program repo (or an unfinished install, detected by a missing or unfilled `meta/DEPLOYMENT.md`) now refuses vault work and redirects to INSTALL.md or the user's real vault, instead of playing maintainer over scaffolding. Inert in any deployed vault. INSTALL.md's verify and hand-off steps now state the session handoff explicitly: the install session ends, and every exocortex session opens inside the vault directory.
- **Artifacts organize by project** (`artifacts/README.md`): an artifact tied to a project lives in a subfolder mirroring the project's bundle (`artifacts/<project>/`), the project hub links its artifact folder, and the zone root holds only unassociated artifacts.
- **README and onboarding now name the wiki's folders**: the front-door README lists the shipped topic folders with one-line purposes plus new Bundles and Projects sections (what counts as effort-shaped work, how a page grows into a project bundle, and that "set up a project bundle for X" is a normal request); ORIENTATION.md gains a matching map section.
- **Scheduled maintenance is now one sequenced orchestrator task** (SETUP.md § 6), replacing the per-skill cadence table: a single daily task delegates process-inbox → (weekly) lint → vault-snapshot to subagents one at a time, records failures without stopping the chain, and ends with one "Needs you" report. Reason: separate tasks all fire at once when the machine wakes late and collide on the maintainer lock and `.state/`. Existing deployments with per-skill tasks: consolidate — the old shape still works, it just races. A prompt template ships in § 6.
- **Links by name, provenance inline (amendment 2026-08-17).** Wiki bodies link with Obsidian wikilinks by name: `[[page-name]]` when the basename is unique vault-wide, `[[folder/path/name]]` when it is not (index, README, colliding names). Markdown links stay only for dot-folder targets and non-markdown files. The frontmatter fields `sources:` and `depends_on:` are retired: every claim carries its citation inline at the sentence it supports, and every body link into wiki/ is a dependency edge. Promotions write a **review receipt** sentence at the top of the body ("Verified by Alex in the digest review of <date> ([[wiki/log/<date>|day log]])") instead of a `sources:` ledger string. Ingest gains a creation-time uniqueness gate (never create a second wiki page with a name that already exists). CONSTITUTION § Folder churn: identity is name, and renames go through Obsidian so inbound links follow. The bundle's OKF claim now records the link form as a documented deviation from spec §5 (meta/README.md). New GLOSSARY entries **wikilink** and **review receipt**.
- **Lint** check 0 compiles body links only, typed by target folder; check 1 requires an inline citation instead of `sources:` non-empty, flags a surviving `sources:`/`depends_on:` field, and flags a verified page without a receipt sentence (the sources-sync rule is gone); check 6 walks inbound links via `obsidian backlinks` or the graph; check 8 reports vault-wide basename collisions and ambiguous bare links (the frontmatter-fallback exposure metric is gone). The verified-on-draft check is a ranked per-page count of draft targets linked from verified pages, report-only, read by the digest as a promotion signal.
- **`vault_graph.py`** resolves body wikilinks by name (unique / path-qualified / ambiguous / dangling), no longer walks frontmatter, reports basename collisions and any page still carrying a retired field, and reports link cycles as strongly connected components (cycle enumeration hung on the dense body-link graph). **`regen-index.py`** emits wikilink entries and refuses to overwrite an authored index when a folder has no listable pages. **`ingest-file.sh`** keeps its stale-citation grep as a safety net for path-form references.
- Query, digest, audit-exocortex, amend (§ Folder refactors are migrations), process-inbox, connections README, and the public README worked example updated to the same convention.

### Migration note
- Existing vaults: this is a three-pass migration (body markdown links → wikilinks; anchor every `sources:` entry inline; delete the two fields). The source vault ran it with two scripts kept private as one-time tooling. `update-exocortex` does not migrate a deployed vault's pages; the new rules apply to pages written from now on, and lint reports the old form as findings until a deployment runs its own passes.

## [0.12.0] — 2026-08-16

### Added
- **Page scoping: every wiki page carries a `scope:` boundary contract, and CLAUDE.md gains a § Page scoping section.** A page holds one subject, evidenced, singly-homed, tested three ways (the description predicts the body, a new fact has one obvious home, the contents rot at the same rate). Ingest writes `scope:` at birth and owns a new split-under-growth-pressure operation. Lint check 1 flags a missing `scope:` on pages created after 2026-08-08. Audit briefs quote the scope. New GLOSSARY entry **scope**.
- **Skill frontmatter law: every shipped skill carries a maintainer-facing `scope:` field**, the fixed standard for recalibrating a skill and the signal it should split. Law in amend § Skill frontmatter law.
- **Judgment is data.** When no rule pins a call down, the maintainer logs one `Judgment:` line (the call, the reasoning, the intent evidence), interactive sessions included. The digest sweeps those lines to you (item 4c, capped at 5). CONSTITUTION principle 7 gains a sentence; the anti-pattern catalog gains **silent judgment**.
- **`regen-issues.py` generates ISSUES.md; both friction-log indexes now have generators.** Lint check 1 requires `title`, `status`, `opened`, and `rule` on issue files.
- **New wiki folder `entities/`** (organizations, places, events, artworks) with folder law and boundaries to people/, projects/, life/, concepts/. Scaffolded by bootstrap. Lint blesses `Entity` and `Person`.
- **`wiki/log/` gains a README**: day logs are dated history, never citation targets.
- **Lint check 1 flags raw HTML in wiki prose.** `<q>` strips mechanically, other tags queue.
- **Lint check 10 queues consolidation candidates**: pages carrying three or more dated `## Unreviewed additions` sections.
- **Cookbook recipe: Obsidian CLI** for alias-aware link integrity, schema-drift counts, and Sync recovery. Experimental; unattended runs must never depend on it.
- **Folder grain law** on concepts/, people/, craft/, life/, entities/ READMEs, each with its own `scope:`.

### Changed
- **CLAUDE.md now says where it binds: inside this vault only.** Work in another repo follows that project's own instructions.
- **Staleness half-lives are keyed by `type`, not by folder.** Person, Entity, Project 90 days; Concept, Connection, Synthesis, Source summary 180 days; Chronicle, Meta, Index never go stale. Deployments may bless further types in DEPLOYMENT.md with a stated half-life. The old "life/infrastructure 30d, conceptual 180d" placeholders are gone.
- **publish-program's conformance check now classifies wiki folder READMEs and scans for links into unshipped wiki paths**, so a shipped README can't reference a folder a fresh install lacks.
- **Amend step 8: a monitoring issue quotes the amended text** rather than describing it.
- **`regen-index.py` lists non-markdown stream items and distinguishes DROPPED from DELISTED**; its `updated:` stamp is a bare date.
- **Ingest's prose-style rule points at the deployment profile** (DEPLOYMENT.md § Style banlist) instead of carrying any specific rule.
- **README is authored in the vault and derived in the repo; MANIFEST ships it**, plus `wiki/entities/README.md`, `wiki/log/README.md`, and `regen-issues.py`.
- **Setup docs point at one cadence home.** DEPLOYMENT.template.md and bootstrap's closing hint refer to SETUP.md § 6 (the digest starts manual) instead of restating a schedule.
- README rewritten around the trust argument: lineage and the laundered-inference problem open, the constitution's eight principles in full, then skills and routines, the notes-wiki fusion, the derived graph, progressive-disclosure retrieval, a campaign demo, the cookbook, and an honest expectations section. Claims aligned with shipped behavior: the digest starts manual, MCP deploy effort is about an hour, notes write-back is additive frontmatter only. Karpathy attribution linked to his llm-wiki gist.
- **Skill and rule prose restyled**: em dashes and clause-joining semicolons removed throughout, no behavior change.

### Fixed
- **The `#no-ingest` opt-out now matches block-form frontmatter tags** (what Obsidian's properties panel writes). Previously only inline `#no-ingest` or a single-line `tags:` value matched, so list-tagged notes were ingested despite the tag. Read your notes before updating: some that used to ingest will now be skipped, as intended.
- **`ingest-file.sh` accepts a trailing slash on the stream argument.**
- **`tools/sync.sh`'s glossary drift check works again**; it had matched the old em-dash separator since the Aug 4 restyle and passed silently. It now fails if it compares zero terms.

## [0.11.0] — 2026-08-07

### Changed
- **CLAUDE.md now imports CONSTITUTION.md at session start.** The "read it at session start" directive is replaced by an `@CONSTITUTION.md` import line, which Claude Code expands into context at launch: the principles arrive in every session with no tool call and no reliance on agent discipline. Origin: a recorded failure where the mandated read silently decayed and an active-project update was handled without vault context. A missing import target is inert (verified), so nothing breaks for surfaces that read CLAUDE.md as plain text.
- **The query skill searches past session transcripts before declaring a matter unrecorded.** When the vault comes up empty on a question about past work with the agent, query now checks the session's tool roster for a transcript-search surface (Claude Code desktop's session-management tools, for example) and searches it before asking the user. A transcript is cited like a source, never ingested directly; durable findings route through the pipeline.
- **The top-of-mind recipe wires the roster into session start.** New setup step: an `@artifacts/top-of-mind.md` import line in CLAUDE.md (or CLAUDE.local.md while trialing) loads the roster into every session. The header spec gains a read rule for agents (a message touching a listed thread means fetch its hub before acting), and the verify section reflects the no-tool-call reality.

### Added
- **GLOSSARY: feature staging.** The trial tier for session directives: unverified imports and rules live in CLAUDE.local.md (deployment-local, never ships) until the user promotes them into the shipped surfaces via amend. Disambiguated from the staging/ import folder.

## [0.10.0] — 2026-08-06

### Added
- **The cookbook: `meta/cookbook/`, an opt-in recipe library, ships with eight recipes.** Connectors (Granola meeting transcripts, Google Calendar, Gmail, Apple Reminders, iMessage), capture tooling (Obsidian Web Clipper), the exocortex-mcp companion server, and the top-of-mind-file workflow. Everything is inert until you opt in: recipes are program content, never swept, ingested, or cited, and the folder's README is the law for how they surface (only when conversation friction matches, at most one suggestion per session, with one exception: the install handoff may overview the whole cookbook as orientation). Each recipe is an earned recommendation from real vault use and carries enough setup detail for your maintainer to drive the install on your yes. Surfaces: new CLAUDE.md zone row, GLOSSARY entries **cookbook** and **recipe**, new MANIFEST path.
- **`ORIENTATION.md`, a one-page capability tour, is installed at every vault root.** What you can ask for, in usage terms: the daily loop, the review habit, corrections, rule changes, updates, and the cookbook. "What can you do?" in any vault session re-opens it. Exists because a real cold-start deployment reached week two without knowing the digest existed.
- **Updates now end with an introduction.** `update-exocortex` gains a step: after applying a release, the maintainer walks you through what you can now say or do, tailored to how you use your vault, and flags anything that changes an existing habit. A diff recital is not an introduction.

### Changed
- **The install handoff teaches the capability surface.** INSTALL.md § 4 rewritten: walk ORIENTATION.md with the new user, set the review habit, and overview the cookbook. The old "ignore digest, lint, and rule-changing until something actually bites" framing is gone; the rules can wait, but people only ask for what they know exists.
- **The digest starts manual.** The install default no longer schedules it. Run "what needs my review" at whatever cadence you feel like (daily is normal during heavy capture, weekly suits a settled vault) and ask to schedule it once you know your rhythm. `process-inbox`, `vault-snapshot`, and `lint` are scheduled as before. Existing deployments keep whatever schedule they have.
- **Ingest treats capture-tool frontmatter as unverified.** A `title:`/`description:` written by a capture tool gets skimmed against the body and fixed at filing time, because the stream index is generated from those fields and freezes with them.
- **Digest's connection-expiry section is exempt from the decision budget.** Section 2 is now a complete listing, never budgeted or carried over, because connection expiry presumes you actually saw the page.
- **README and GLOSSARY restyled into plain sentences.** Em dashes and clause-joining colons and semicolons are gone, replaced with short sentences, commas, and parentheses. No term meanings or claims changed.

## [0.9.0] — 2026-08-04

### Added
- **New zone: `artifacts/` — a shared workspace for co-built work products.** Slide decks, HTML pages, documents, anything the user and maintainer build together, any file type; the maintainer creates and edits artifacts there when the user directs. Sweep, ingest, index, and citation-as-evidence are forbidden: the pipeline never reads the folder, and the folder law records why — linking to an artifact carries no authorship claim, but citing a claim as evidence requires a speaker, and co-built files have mixed authorship, so claims that matter route through `sources/inbox/` with attribution. Fills the gap between `notes/` (user-written) and `wiki/` (agent-written). Surfaces: a new CLAUDE.md zone row, `artifacts/README.md` (new MANIFEST path), and a GLOSSARY **artifacts** entry.

## [0.8.0] — 2026-08-04

### Changed
- **`drawings/` is now a shared sketch space — the maintainer may create and edit drawings there.** Excalidraw files, Obsidian canvases, anything sketch-shaped; previously the folder was the user's alone, read-only to agents. Sweep, ingest, and index remain forbidden: nothing in `drawings/` enters the pipeline, and a drawing whose content matters still routes through `sources/inbox/` in the user's words. There is deliberately no authorship marker distinguishing agent drawings from the user's — the rule starts minimal, and a protection mechanism gets proposed only if an incident shows the need. Surfaces changed: the CLAUDE.md zone row, `drawings/README.md`, and the GLOSSARY **drawings** entry.

## [0.7.0] — 2026-08-04

Both minor-bump behaviors came out of one incident chain: nine wiki pages carried unparseable frontmatter for two days, and three frontmatter edges silently died when an unrelated page was created elsewhere in the vault. The maintainer now refuses one risky write and reports one standing fragility measure it previously ignored.

### Added
- **`ingest-file.sh` refuses to file an inbox item missing `title:` or `description:`** (exit 3, nothing moved). Derived stream indexes pull their entries from those two fields, and filing freezes a source forever — so a capture filed without them sits in its index as a bare slug with no retrieval hook, permanently. The check runs *before* the move, which is the last moment the fields can still be written; the refusal message says exactly that. `--allow-missing-frontmatter` files as-is for items whose content genuinely can't supply them.
- **Lint check 8 reports basename-fallback exposure every run** (new report section in `vault_graph.py`): the count of frontmatter edges that resolve only because exactly one file in `wiki/` carries that basename, plus the basenames the most edges depend on. Creating any second file with one of those names silently breaks all of its dependent edges at once, with no edit to the citing pages — the count is a standing fragility measure, not a to-do list. Edges already broken by a collision are real findings and get repaired to file-relative form.

### Changed
- **Ingest's YAML-discipline rule now states it binds every write path that touches frontmatter**, not just the page template — the nine broken pages were stamped by write paths that never read the template — and **`updated:`, where a page carries one, holds a bare date and nothing else**: what changed already has two homes (the day log, and the `## Unreviewed additions` heading on a verified page).

## [0.6.1] — 2026-08-01

### Added
- **Provenance write-discipline, one sentence in each failure's home** (amendments 2026-07-31, each shipped after a real failure case): session-capture — a commitment voiced in the record ("I'll send that now") is written as committed, never as done, because the record ends before the action would occur; ingest — a citation to named external work that arrives from conversation rather than a filed source stays marked as the conversation's claim, and never becomes a page's title, filename, or organizing frame until checked against the work itself. Both instantiate the constitution's laundered-inference anti-pattern.
- **Lint learns bundle membership** (check 1): a page inside a bundle folder belongs on its hub's satellite list — derivable from the path alone, so lint appends missing entries unsupervised, each summarized from the satellite's own `description` line. Append, never regenerate: the hub is prose. Cross-folder relationship links remain gated.

### Changed
- **Lint check 1 respecified as a whole** — restructured from one accreted paragraph into labeled sub-sections (Scope / Frontmatter / Links / Quote provenance / Sources sync / Bundle membership / Staged sections / Type hygiene), every prior rule preserved. `Index` joins the known-type list (authored hub listings, default Concept lifecycle). meta/README.md now documents the OKF §6 deviation — authored bundle hubs carry page frontmatter and are checked as pages — beside the existing §5.2 one.

## [0.6.0] — 2026-07-31

### Added
- **Get-to-know-you conversation at install** (INSTALL.md § 1b, offered and never required): after the setup questions, the installing agent invites a short conversation — one specific open question at a time ("what are some active projects you've got going on?"), follow-ups that follow the answer, three to six exchanges, never a form and never homework. The transcript becomes the vault's **first capture**, filed to `sources/inbox/` with the user's words in marked quotes and provenance `"the user, <date> (install interview)"`. The § 3 smoke test then compiles it, so a new vault's first wiki pages are about its owner — their projects, their people — all `draft`, all citing their own words. README Quick-start mentions it.
- **The full wiki scaffold ships in the repo.** All seven declared topic folders (concepts, projects, people, life, craft, connections, log) now exist in the clone and in fresh vaults — four more folder READMEs join MANIFEST (concepts, people, craft, connections), so every folder wiki/README.md declares arrives with its folder law. Seed `index.md` stubs (root + six topic folders) are bootstrapped once as the query skill's entry points, then owned by the vault's pipeline; they deliberately stay out of MANIFEST so a live vault's personal indexes can never sync into this repo. Fixes the fresh-install gap where the query skill's entry point (`wiki/index.md`) didn't exist and ingest had to create declared folders mid-run.

### Fixed
- **`#no-ingest` now matches real Obsidian tag semantics** (`notes-cursor-diff.py`): the tag written inside backticks or code fences no longer counts (a note *discussing* the tag was silently dropped from the sweep — found by a clean-room install test), and a `tags:` line only counts inside the frontmatter block. `notes/README.md` (folder law, not a note) is now explicitly invisible to the sweep, in script and skill text.
- Ingest's day-log step referenced a `log.md` index that has never existed; reference removed. Bootstrap's next-steps output no longer tells you to `git init` a vault that already is a repo.

### Added
- **Substrate scripts now ship.** `.claude/scripts/` joins the program: `vault_graph.py` (lint check 0's graph compile), `notes-cursor-diff.py` (the notes sweep's mechanical walk), `regen-index.py` (derived-index regeneration), `ingest-file.sh` (ingest's move-hash-ledger step). **One-time setup after updating:** build the graph venv, `python3 -m venv .claude/scripts/graph-venv` then `.claude/scripts/graph-venv/bin/pip install networkx pyyaml` (lint check 0 also carries these commands and falls back to manual checks if the script can't run). The program definition (CONSTITUTION § Sharing and boundaries, GLOSSARY "program") now says system files, not markdown.
- **Folder-law READMEs for every zone**: drawings/, notes/, sources/ plus its four stream folders, wiki/, wiki/projects/, wiki/life/. Every GLOSSARY `_Home:_` pointer now resolves to a shipped surface, so a fresh install passes lint check 9 by construction.

### Changed
- **The repo no longer ships its own publishing machinery.** The `publish-program` skill (the tool that produces these releases) was creator tooling riding in the consumer surface; it now lives only in the program's source vault. MANIFEST enumerates every shipped skill and script explicitly and carries a declared-private list: every skill and script in the source vault appears on exactly one side, so nothing ships (or stays private) without a recorded decision. GLOSSARY entries for creator-side skills now say so.
- **`bootstrap.sh` reads MANIFEST** instead of keeping its own file list (the two had drifted; this release would have shipped skills referencing scripts that bootstrap never delivered). Side benefit: `--update` now syncs only shipped folders, so skills and scripts you added locally survive updates without the set-aside step (update-exocortex step 4 updated to match).
- The digest's program-update item is now consumer-only (the source-vault drift report moved into the creator's publish procedure); lint check 0 carries its environment setup inline instead of pointing at deployment bindings; vault-snapshot's hourly-subset wording is deployment-neutral.

## [0.4.0] — 2026-07-24

### Added
- **Self-interview in the digest** (compile item 4b + interview verdicts): each digest may carry 1–3 question-shaped items about the user — blind-spot (a receipted, unconfirmed pattern-claim), disclosure (the system doesn't know, so it asks), or negative-space (a structural absence neither party has named). Confronting material is explicitly in scope; the self-model page's Off limits section is the only topic restriction, and zero items is always fine. Verdicts complete all bookkeeping: confirm enters the claim on `wiki/life/self-model.md` with digest-review provenance, reject is itself recorded self-knowledge, "not that topic" adds to Off limits and is never re-asked. GLOSSARY gains **self-interview** and **self-model page**; the page law lives in `wiki/life/README.md`.
- **Agent-maintained notes index**: the notes sweep now regenerates `notes/index.md` — categorized sections of wikilinked entries with descriptions pulled from note frontmatter. Wikilinks survive the user reorganizing their notes; category assignments are curated and the user's recategorizations stick across regenerations. The index is the one agent-authored file in notes/ (CLAUDE.md zone row updated) and is invisible to the sweep itself.
- **Audit briefs sort items by who the decision belongs to** (audit-exocortex): **needs-you** items (real tradeoffs, facts only the user holds, anything touching promotion) lead, each with a recommendation and its reason; **recommend-and-run** items (mechanical fixes, one-way evidence) execute unless vetoed by item number — silence is consent for that class only, and never for promotion to `verified` or meaning changes on a verified core.
- **The digest surfaces new program releases** — each digest run fetches the program clone and, when a newer release exists, adds one line pointing at "update my exocortex." Notification now rides the surface users already review; applying still gates on their approval. INSTALL's handoff mentions this plus the GitHub Watch → Releases option.
- Onboarding handoff now suggests the Obsidian Web Clipper by name — articles and YouTube pages clip straight to the inbox; most new users don't know it exists.
- README shows the product instead of describing it: a worked capture-to-cited-answer example (transcript + the actual before/after files), a "your first five minutes" section, a Mermaid pipeline diagram, license badge, collapsible reference sections.
- **Companion cross-links**: README § "Optional companion" and SETUP's capture section point at [exocortex-mcp](https://github.com/AlexHagemeister/exocortex-mcp) — the optional remote MCP server (query + capture from claude.ai and the Claude mobile app), now public with the same repo hygiene; it links back. Auto-updating release badge in the README header.
- **Upstream bug reports are now the documented norm** (ISSUES.md): when friction is in the shipped program rather than local amendments or data, maintainers file it on this repo's issue tracker in receiving-end detail — file, line, expected vs. observed, environment. Public-post rules apply: no vault content, no personal data, and the user approves before anything goes up (unattended runs draft locally for the digest). Formalizes the flow that produced issue #1.

### Changed
- **Core immutability gains a second exception** (ingest): link maintenance — adding a missing source link, repairing a broken path — runs unsupervised on verified pages; it asserts nothing new. (The correction flow remains the only way to change what a verified core *says*.)
- **The leak scan now covers both publish paths.** `publish-program` previously blessed editing the repo's own files (README, SETUP, tools/) directly, and only the vault→repo sync path ran `tools/sync.sh`. So a repo-direct commit could reach the remote unscanned, and one did. The skill now requires the scan over any repo-direct change before it is committed; `sync.sh` already walks every file git would publish, not only the files it copied.
- **`meta/HANDOFF.md` carries a supersession banner**, matching the one `meta/VAULT-DOCTRINE.md` has had since the start. Both ship as construction artifacts, records of how the system was designed, and HANDOFF had nothing marking two of its premises as expired: the vault is now itself a git repo snapshotted by `vault-snapshot` (the `mirror-snapshot` skill and separate mirror repo are gone), and the iCloud eviction hazards it warns about no longer describe a deployment on Obsidian Sync. The dated instructions are preserved verbatim; only the framing is new. A matching dated note lands in the doctrine's § 9, whose closing line had predicted exactly this change.
- Leak scan: `sync.sh` gains a documented `PUBLIC_ALLOWLIST` — the author's own public repo and badge URLs are stripped before the private-pattern scan, so public self-references pass while any other private-pattern occurrence still fails the publish (user-approved carve-out; additions remain publishing decisions).

## [0.3.0] — 2026-07-23

### Added
- Ko-fi support link: button in the README (§ Support) and a one-time mention at install handoff (INSTALL.md § 4, item 7).
- **`staging/` import folder** ships in the vault skeleton, with a README (zone: user-owned, invisible to the pipeline). Migrating users drop their exported corpus there and move batches into `notes/` or `sources/inbox/` deliberately — the move is the activation. SETUP § 9 rewritten around it; any other import route still works.
- **Obsidian setup section** (SETUP § 5, INSTALL interview + execute steps): open-as-vault, default attachment location → `attachments/`, default new-note location → `notes/`, Templater configured to auto-apply the shipped note template on file creation in `notes/` (the core Templates plugin can't fire on creation), and a field-tested caution scoping frontmatter-rewriting plugins away from wiki/.
- **Prerequisites now name the full dependency surface**: git (required), a GitHub account + `gh` CLI (optional, recommended for the private backup remote and bug reports). Onboarding walks users through account signup and `gh auth login` when wanted — always the user's own acts; the agent guides and never touches credentials.
- GLOSSARY entries: `update-exocortex` (was the one skill without a term home) and `staging`.

### Changed
- CLAUDE.md `.state/` zone row: "issue files any time" carve-out, resolving the self-contradiction with the file-an-issue instruction.
- Lint check 1's quote-provenance trigger narrowed to speech-attributed blockquotes — editorial callout boxes that merely mention the user no longer flag (was ~10 false positives per run on deliverables pages).
- The digest review-time tripwire number is stated only in the digest skill; the amend skill now points instead of restating it.
- meta/README's index-frontmatter policy line reconciled with practice (pre-2026-07-20 `updated:` stamps are grandfathered).
- vault-snapshot notes the optional hourly mechanical subset (snapshot-lite) and sweeps up anything it left behind — unpushed work, scan hits, conflicts (rode along from a 2026-07-22 vault amendment).

### Fixed
- `bootstrap.sh --update` now refreshes `GLOSSARY.md` (it was missing from the program-file copy list, so updated vaults silently kept a stale glossary) and never overwrites a live vault's `ISSUES.md` — the issue index is vault-owned and is now seeded only on fresh install (issue #1, reported by @amattinger).

## [0.2.0] — 2026-07-22

### Added
- **`update-exocortex` skill — updating is now a first-class, in-vault act.** Say "update my exocortex" in a vault session: the skill fetches the latest release, summarizes the changelog, waits for your go-ahead, commits a rollback point, reconciles your local amendments (keep yours / take upstream / merge — never silently overwritten) and sets aside skills you added locally before `bootstrap.sh --update` would delete them, applies, and stamps the new version. `meta/DEPLOYMENT.md` gains a `Program version` row (template updated; stamped at install). INSTALL.md and SETUP.md § Updating now delegate to the skill instead of duplicating the procedure.
- **`audit-exocortex` skill** — the interactive page-review loop: one page per turn, a reading brief with precisely addressed items, explicit verdicts (correct / add / promote / skip). The digest's review step now runs through it; promotion stays an explicit human act. GLOSSARY entry added.
- **GLOSSARY.md** — canonical system vocabulary (term meanings with Avoid/Home pointers). Ships with the program; CLAUDE.md points agents at it when jargon is ambiguous. Public README gains a Key terms skim subset; `tools/sync.sh` fails the publish if those one-liners drift from GLOSSARY.md.
- Folder law READMEs for `attachments/` and `templates/` (zone rows already existed; agents can now satisfy "read the README before writing").
- **Onboarding posture** (INSTALL §4 Hand off + SETUP §7): minimum viable use first; invite "explain it simply"; rules change via `amend` with approval — not freestyle; principle tension → plain-language tradeoff brief, then the user decides.
- **Voice — your maintainer's communication style is now yours to choose.** The setup interview asks how your maintainer should talk to you; INSTALL.md § 1a elicits it by example (the same digest message in three voices — pick, blend, or write your own) and saves a confirmed spec, never just a label. The spec lives in your `meta/DEPLOYMENT.md` `## Voice` section (user-owned, survives updates); CLAUDE.md binds sessions to adopt it — tone only, never the epistemic rules: status labels, provenance, disputes, and corrections stay plain in every voice.
- Zone rows for `attachments/` and `templates/` in CLAUDE.md — both user-owned; the agent reads freely, writes only with explicit approval.
- Digest skill: retroactive review markers — when act-evidence shows a review that never got its marker, reconstruct it (dated to the acts, noted as reconstructed); unattended runs surface the evidence instead.
- Ingest: verbatim user quotes carry an inline source link at the quote; lint check 1 enforces it.
- Lint check 5: consuming a deleted note re-reads every citing page — standing flags sourced to withdrawn evidence are queued, never silently kept; annotated tombstones recognized as already reconciled.

### Changed
- CONSTITUTION § Sharing: program definition matches MANIFEST (shippable system markdown; `.state/` contents never ship, its README may).
- Amend skill: when a proposal tensions with a principle, push back with tradeoffs before asking for approval; jargon changes update GLOSSARY.md in the same pass.
- Issue-workflow residence: `~3` cluster threshold lives in amend; close procedure lives in ISSUES.md; digest points.
- Digest last-call for connection expiry points at lint check 7 instead of deriving a duplicate number.
- Lint check 1: folder `README.md` files exempt from the `sources:` requirement (Meta documentation, not claim pages).
- Status-weighting ladder now lives only in CLAUDE.md; the query skill points to it instead of restating it.
- `publish-program` skill now carries the release protocol: changelog maintenance, version tagging, and GitHub releases are part of the publish procedure.
- Note template timestamps use a human-readable date format.
- Ingest: page `description` fields are written as retrieval hooks — third person, what the page holds + when to fetch it — since that line is often all an agent sees when deciding whether to load the page (per Anthropic's context-engineering guidance).
- Query: long multi-page syntheses place fetched content above the question and quote load-bearing passages before reasoning — both measurably improve long-context accuracy.
- Lint and process-inbox eviction guards generalized to sync-layer-neutral wording (iCloud kept as a filename example, dropped as an environment assumption).
- Two stale path references corrected: CONSTITUTION's residence map now names `meta/OKF-SPEC.md`; meta/README's move-instructions name the real dependents instead of a deleted skill.
- Ingest: inline quote-link form specified — in-prose quotes make the quoted words the link anchor; blockquotes end with a `— [the user, <date>](<path>)` citation line. Frontmatter `sources:` pinned as built-from provenance; lint check 1 syncs it additively (append missing body-link targets, never remove).
- Lint check 1: the YAML-parseability test now also covers `.state/issues/*.md` (the issue index is derived from them and cannot regenerate over a broken file).
- GLOSSARY: "bundle" sense widened — bundles are contained folders of related knowledge and nest freely; unqualified "the bundle" still means the wiki/ export surface. README Key terms and skill roster refreshed to match.

## [0.1.0] — 2026-07-19

First versioned release: the system as it stands after the vault-as-repo migration.

### Architecture
- The vault is itself a git repo with a private remote. The `vault-snapshot` skill (replacing `mirror-snapshot`) commits, pull-rebases, and pushes on schedule — history, rollback, and recovery live in the vault's own git history.
- Device sync, if wanted, is a dotfolder-ignoring layer (Obsidian Sync). iCloud and Dropbox must not hold the vault — they corrupt the repo.

### Added
- `INSTALL.md` — agent-guided install: one pasted prompt; the agent interviews, sets up, verifies, and hands off.
- SETUP.md § 8 — corpus-migration workflow for notes arriving from another app: batched, topic-coherent, review-paced.
- Ingest topic-tether rule: on a page the user's material justifies, cited external reference content is welcome; lookups never open new topics and lookup-derived content doesn't cascade.
- README rewritten as TL;DR → quick start → capabilities → workflow → rationale.
