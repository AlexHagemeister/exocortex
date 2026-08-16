---
name: ingest
scope: "Procedure for turning one source item into wiki pages, including the page frontmatter law (scope field) and the split operation. Not the queue orchestrator (process-inbox), not a rules-change surface (amend)."
description: "Turn a source into wiki pages: validate, file, summarize, update related concepts. Use when processing an item from sources/inbox/, a notes/ delta handed over by process-inbox, or when the user says 'ingest this', 'add this to the wiki', or asks you to remember content they provide."
---

# Ingest — source → wiki

You are turning one source item into durable wiki knowledge. Input is one of: a file in `sources/inbox/`, a new-or-changed note delta from the notes sweep, or a correction statement from the user (which becomes an inbox file first). Read the README of every folder you write to before writing. Folder-local rules live there.

## Procedure

### 1. Validate (gate before anything else)

Reject items that are empty, truncated mid-content, or junk (boilerplate-only clips, error pages, binary noise). Rejected inbox items → move to `sources/inbox/quarantine/` and log one line in the day log (`wiki/log/<YYYY-MM-DD>.md`) with the reason. The gate applies no matter which tool captured the item. The inbox is multi-tenant.

Then dedup: compute the content hash (`shasum -a 256`) and check it against the ledger `.state/ingest-hashes.txt` (one `<hash>  <filed path>` per line, create if missing). Already ingested → delete the duplicate inbox item, log it, stop.

Note deltas skip quarantine (notes/ is the user's zone, so never move a note or touch its body). If a note delta is unusable, skip it and log why.

### 2. File (freeze happens here)

Move the inbox item to its permanent stream folder, choosing by the stream READMEs. **File before you cite.** Provenance always references the final path. (`.claude/scripts/ingest-file.sh <inbox-item> <stream-folder>` does the move + hash + ledger append + stale-citation grep in one call.)

- **Filing**: the stream folders are `sources/articles/` (external material), `sources/sessions/` (session captures), `sources/meetings/` (recorded conversation transcripts), `sources/life/` (personal exports). If the best stream's declared modality would still mislabel the item (e.g. agent web research, a maintainer-authored artifact), add one `modality:` line to the item's frontmatter before filing, stating what the item actually evidences. The stream README stays the default for everything else.
- **Naming**: use a stable, descriptive, date-prefixed filename (`2026-07-16-title-slug.md`) dated by the source's own local date, not the ingest run's. This path is cited forever.
- **Freezing**: before filing, inbox items are freely editable. After filing, the source is frozen. Never edit or delete it, because a source records what was said, not what's true.
- **Metadata fixing**: a `title:`/`description:` written by a capture tool is unverified. Skim the body against it and fix it now, because the stream index is generated from those fields and freezes with them.
- **Citation rewrite**: append the new hash to the ledger. After filing, grep `wiki/` for the item's old inbox path and rewrite any citations to the filed path.

Notes are never filed. They stay in `notes/`, and you cite `notes/<path>` **plus the timestamp you read it** (mutability for the user, pinned provenance for the wiki).

### 3. Read under the stream's modality

Read the source in full. Honor the stream README's declared evidential semantics, or the item's own `modality:` frontmatter, which overrides the stream default. They bound what kind of claim the source can support (e.g., a calendar entry evidences intention, never occurrence, and a session summary is paraphrase of what was said, not what's true).

If this is an interactive session, briefly discuss takeaways with the user before writing: what seems important, what connects to existing pages.

### 4. Write the source-summary page

One wiki page distilling the source, in the appropriate `wiki/` topic folder (check `wiki/index.md`. If no folder fits, ask the user. New top-level folders are the user's call, because a path is an identity and renames break links). When several inbox items are one **attachment set** (an item plus the attachments it explicitly cites at capture, never mere topical similarity or same-day arrival), file each separately but write one summary page citing all of them. A member gets its own page only when it carries claims the primary item's page doesn't. Fill this template:

```yaml
---
type: Source summary
title: <source title>
description: <one sentence>
scope: "<boundary contract: what belongs, what is excluded and where it lives instead>"
tags: []
timestamp: <now, ISO 8601>
status: draft
verified_at:
depends_on: []
sources: ["<final filed path, or notes/<path> + read timestamp, or URL>"]
---
```

**YAML discipline**: double-quote any frontmatter value containing `": "` (colon-space) or starting with a special character. An unquoted colon silently breaks the mapping and the page stops rendering in Obsidian. This binds every write path that touches frontmatter, not just the template above. `updated:`, where a page carries one, holds a bare date and nothing else. Prose annotations there broke nine pages for two days, and what changed already has two homes: the day log, and the `## Unreviewed additions` heading on a verified page.

**Description is the retrieval hook**: write it in third person as *what the page holds + when to fetch it*. For an agent deciding whether to load the page (search results, indexes, MCP), this line is often all it sees.

**`scope:` is the boundary contract** (meaning in GLOSSARY.md), written on every wiki page at birth: what belongs, what is excluded, and where each exclusion lives instead. Each exclusion names its true home ("member status lives on [the hub](...)"), so a failed lookup reroutes without loading the body. One concise sentence is enough on a page whose boundaries are simple. An authored bundle hub's scope also carries the bundle's routing law. Keep exclusions out of `description`. That line attracts the right readers, and `scope:` bounds the page.

Body sections (keep observation and inference under separate headings, always): <!-- constitution: laundered inference -->

```markdown
# What the source says

<claims, attributed per the stream's modality>

# What we conclude

<your inferences, explicitly marked as inference>
```

### 5. Update related concept pages (5–15)

Find existing wiki pages the source bears on (start from `wiki/index.md`, drill via links) and update them, and create new concept pages where a red link or a clear gap exists. Every page write follows the same rules:

- Same frontmatter template as above, with `type: Concept` (or another descriptive type).
- **`status: draft`, always.** Sole exception: a claim quoting the user **verbatim** is born `verified` (set `verified_at`). Paraphrases are NOT. Paraphrase is where misstatement lives.
- **No claim without provenance.** Every substantive claim traces to a `sources:` entry or is explicitly marked as your inference. Never write a guess with the typography of a fact.
  - State each claim plainly, and mark its epistemic status once: one attribution sentence per claim-cluster, not hedges woven into every clause.
  - A verbatim user quote carries an inline link to its source at the quote: in-prose quotes make the quoted words the link anchor. Blockquotes end with a citation line `— [the user, <date>](<relative path>)`.
  - Page-level `sources:` records what the page was *built from*. That is not enough for quotes that travel to other pages, and it lists every source the body links inline.
  - A citation to named external work that arrives from conversation rather than a filed source stays marked as the conversation's claim about that work. It may inform a body, but never becomes a page's title, filename, or organizing frame until checked against the work itself.
- **Standard markdown links only, file-relative paths** (same folder: `[orders](orders.md)`; other folder: `[orders](../concepts/orders.md)`). Never wikilinks, and never leading-slash paths. Obsidian resolves `/...` from the vault root, not the bundle root, so those links are dead in the viewer and clicking them spawns phantom files. File-relative is OKF-legal (spec §5.2). Dangling links are legal and useful. Red links are the backlog of known-missing knowledge.
- `depends_on:` lists the concept paths this page's claims rest on.
- **Never state another page's status or existence in prose.** Status and page-sets are designed to change, so such sentences are guaranteed to rot. Link the page and let readers weight it by its own frontmatter.
- Respect the user's style bindings in all prose you write: the word banlist and any style rules recorded beside it (both in `meta/DEPLOYMENT.md` § Style banlist). They bind at write time. Wiki pages are future agent context, so style debt compounds. Pages already carrying a violation get fixed opportunistically when a skill next touches them, never in a bulk sweep.

**Split under growth pressure, never at birth.** When a write would leave a page failing the boundary tests (CLAUDE.md § Page scoping), split along a subject seam: move the detail to a new page, keep a summary and a link on the parent, update both pages' `scope:` to name the new boundary, and rewrite every inbound link in the same pass. A path is an identity, so split conservatively and name for permanence. Never pre-create pages for subjects that might grow. The satellite pattern in wiki/projects/README.md is this rule's folder-local form.

**Adding to an existing `status: verified` page** (staged-sections convention): never edit the verified core prose.

- New material appends under a dated heading `## Unreviewed additions (YYYY-MM-DD)` (multiple dated sections may accumulate), each claim with provenance, and you set `pending_review: true` in the frontmatter. The page-level `verified` then means "the reviewed core is verified". Annex content is draft-grade until the user confirms it (digest merges it into the core and clears the flag).
- If annex material *contradicts* the verified core, flag the contradiction inside the annex and let it queue for the digest, and never auto-dispute the page.
- Core immutability has two exceptions. The first is the correction flow: a correction from the user (provenance "the user, <date>") authorizes rewriting the core directly.
- The second is link maintenance (add a missing source link, repair a broken path), which asserts nothing new and runs unsupervised.

Draft pages need none of this. Edit them freely.

### 6. Connections

If the source reveals a substantive insight that two things relate (beyond a note merely mentioning a known entity, which is an ordinary link), create a page in `wiki/connections/` per that folder's README. Never write links into note bodies. Navigational `related:`/tag pointers in note frontmatter are the sweep's write-back (per process-inbox), not ingest's. Backlinks surface wiki-side links on the note automatically.

### 7. Close out

- Regenerate `index.md` in every folder you touched (source-stream folders you filed into count as touched). Derived files are sections of `* [Title](path) - description` lines pulled from frontmatter. Regenerate freely, never hand-maintain. `.claude/scripts/regen-index.py <folder>` does it mechanically and slots new pages for you to categorize. **Exception**: an `index.md` carrying page frontmatter (`type`/`title`/`status`) is an authored bundle hub, not a listing. Never regenerate it. Link new satellites from it instead (link maintenance).
- Append one entry per action to today's day log, `wiki/log/<YYYY-MM-DD>.md` (create it if missing, newest-first `* **Update**: …` lines).

## Corrections (when the source is the user's statement)

A correction file (provenance `"the user, <date>"`) reconciles rather than adds: locate every wiki page citing the corrected claim (grep `sources:` and body), rewrite the affected claims citing the correction, and leave the superseded source in place. It stays as historical record, and the wiki layer outweighs it. A verbatim correction from the user is born `verified`. If a claim is withdrawn entirely, re-examine pages listing it in `depends_on` or linking to it. Never retract silently.

## Don'ts

- **Laundered inference** — a guess written as a fact. Status fields and the observation/inference split exist to prevent it.
- **Promiscuous capture** — the user's sources decide the wiki's topics. Lookups never open new ones. On a page the user's material justifies, cited external reference content is welcome: who an entity is, established background, corroboration of a claim. Lookup-derived content doesn't cascade. Nothing found via lookup justifies creating further pages or importing further material. (notes/ and life exports are exempt: the user's own speech and scheduled personal exports are pre-curated by definition.)
- **Never edit a filed source, ever.** Corrections arrive as new sources.
