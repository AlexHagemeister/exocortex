---
name: ingest
scope: "Procedure for turning one source item into wiki pages, including the page frontmatter law (scope field), the split operation, the compact operation and the fold, and supersession by the user's verbatim word. Not the queue orchestrator (process-inbox), not a rules-change surface (amend)."
description: "Turn a source into wiki pages: validate, file, summarize, update related concepts. Use when processing an item from sources/inbox/, a notes/ delta handed over by process-inbox, or when the user says 'ingest this' or 'add this to the wiki'."
---

# Ingest — source → wiki

You are turning one source item into durable wiki knowledge. Input is one of: a file in `sources/inbox/`, a new-or-changed note delta from the notes sweep, or a correction statement from the user (which becomes an inbox file first). Read the README of every folder you write to before writing. Folder-local rules live there.

**Delegated immediate ingest** (the "remember this" flow): when a session captures a user statement to the inbox and delegates this skill to file it at once, the delegated run honors `.state/maintainer.lock` (stand down and leave the item for the next drain if held), and step 3's interactive discussion is satisfied by the capturing conversation itself.

## Procedure

### 1. Validate (gate before anything else)

Reject items that are empty, truncated mid-content, or junk (boilerplate-only clips, error pages, binary noise). Rejected inbox items → move to `sources/inbox/quarantine/` and log one line in the day log (`wiki/log/<YYYY-MM-DD>.md`) with the reason. The gate applies no matter which tool captured the item. The inbox is multi-tenant.

Then dedup: compute the content hash (`shasum -a 256`) and check it against the ledger `.state/ingest-hashes.txt` (one `<hash>  <filed path>` per line, create if missing). Already ingested → delete the duplicate inbox item, log it, stop.

Note deltas skip quarantine (notes/ is the user's zone, so never move a note or touch its body). If a note delta is unusable, skip it and log why.

### 2. File (freeze happens here)

Move the inbox item to its permanent stream folder, choosing by the stream READMEs. **File before you cite.** Provenance always references the final path. (`.claude/scripts/ingest-file.sh <inbox-item> <stream-folder>` does the move + hash + ledger append + stale-citation grep in one call.)

- **Filing**: the stream folders are `sources/articles/` (external material), `sources/research/` (the agent's own compiled findings from external surfaces: web research passes, live-page reads, site re-checks, verification sweeps; stream minted 2026-09-04), `sources/sessions/` (session captures), `sources/meetings/` (recorded conversation transcripts), `sources/life/` (personal exports). If the best stream's declared modality would still mislabel the item (e.g. a maintainer-authored artifact, an agent outline of one external document), add one `modality:` line to the item's frontmatter before filing, stating what the item actually evidences. The stream README stays the default for everything else.
- **Naming**: use a stable, descriptive, date-prefixed filename (`2026-07-16-title-slug.md`) dated by the source's own local date, not the ingest run's. This path is cited forever.
- **Freezing**: before filing, inbox items are freely editable. After filing, the source is frozen. Never edit or delete it, because a source records what was said, not what's true.
- **Metadata fixing**: a `title:`/`description:` written by a capture tool is unverified. Skim the body against it and fix it now, because the stream index is generated from those fields and freezes with them.
- **Citation rewrite**: append the new hash to the ledger. After filing, grep `wiki/` for the item's old inbox path and rewrite any citations to the filed path.

Notes are never filed. They stay in `notes/`, and you cite the note by name (`[[Note name]]`) **plus the date you read it** (mutability for the user, pinned provenance for the wiki).

### 3. Read under the stream's modality

Read the source in full. Honor the stream README's declared evidential semantics, or the item's own `modality:` frontmatter, which overrides the stream default. They bound what kind of claim the source can support (e.g., a calendar entry evidences intention, never occurrence, and a session summary is paraphrase of what was said, not what's true).

If this is an interactive session, briefly discuss takeaways with the user before writing: what seems important, what connects to existing pages.

If the source carries an `# Ingest brief`, treat it as the capturing agent's routing recommendation: start from the pages it names, but verify each against the page's current state before editing, since the brief may predate other changes. It never overrides the filing rules or the page-scoping tests, and a brief-less source is ingested exactly as before.

### 4. Write the source-summary page

Pages are organized by subject, never by source (amendment 2026-09-06, replacing one-page-per-source and its exceptions). A source updates the pages that own its subjects, cited inline at the claims it supports; the stream index carries the source's own discoverability. Write a new page only when the source introduces a subject no page owns, or when the user flags it for a deep pass, in the appropriate `wiki/` topic folder (check `wiki/index.md`. If no folder fits, ask the user. New top-level folders are the user's call, because they are the bundle's shape). Several sources on one subject (an attachment set, one conversation captured in pieces, a thread across days) feed one page citing all of them; a member earns its own page only for a subject no other page owns. Sharing a subject is the test, never same-day arrival or topical nearness (the user's membership-creep ruling, 2026-08-06, now enforced by CLAUDE.md's page-scoping tests). A correction reconciles pages (§ Corrections) and never earns one. Fill this template for a new page:

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
---
```

Cite the source inline in the body (the filed path as a wikilink, a notes/ page by name with its read date, or the URL), at the claims it supports. There is no page-level source list.

**YAML discipline** is enforced where the deployment has a frontmatter-validation hook (a real parser that validates every frontmatter write and names the fix on rejection); on other deployments, follow the shape below by hand. `updated:`, where a page carries one, holds exactly `YYYY-MM-DD H:MM am|pm` (12-hour local time, e.g. `2026-08-27 6:28 pm`) and nothing else: no prose, no timezone suffix (amendment 2026-08-27; a bare date without time is legacy, conforming-but-stale). Prose annotations there broke nine pages for two days, and what changed already has two homes: the day log, and the `## Unreviewed additions` heading on a verified page.

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
- **`status: draft`, always.** Sole exception: a claim quoting the user's verbatim **verdict, ruling, or correction** (the user settling a claim's truth, not merely stating information) is born `verified` (set `verified_at`). First-pass information in the user's words (a roster, a recollection, a plan) is faithfully his speech but not reviewed truth: born `draft` like everything else (narrowed 2026-08-31). Paraphrases are NOT verified in either case. Paraphrase is where misstatement lives.
- **No claim without provenance, at the claim.** Every substantive claim carries its citation inline, in the sentence it supports: a wikilink to the source file, a URL, or the user's dated words in parentheses ("Alex, 2026-08-10, in chat"). Or it is explicitly marked as your inference. A source that no sentence rests on is not cited on this page. Background reading a page leans on as a whole gets one sentence ("Built on [[x]] and [[y]]."), not a list. Never write a guess with the typography of a fact.
  - State each claim plainly, and mark its epistemic status once: one attribution sentence per claim-cluster, not hedges woven into every clause.
  - A verbatim user quote carries an inline link to its source at the quote: in-prose quotes make the quoted words the link anchor. Blockquotes end with a citation line `– [[<source-name>|the user, <date>]]` (en dash, since 2026-09-01; the em dash form written before then is grandfathered, and the claim extractor accepts both).
  - A citation to named external work that arrives from conversation rather than a filed source stays marked as the conversation's claim about that work. It may inform a body, but never becomes a page's title, filename, or organizing frame until checked against the work itself.
- **Wikilinks, by name.** `[[page-name]]` when the file's basename is unique across the whole vault (wiki/, notes/, sources/, everything but dot-folders). `[[wiki/projects/krux/index]]` (path-qualified, no `.md`) when it is not: index, README, and any colliding name. Alias with `|` freely. Never markdown links to vault files, never leading-slash paths, never `.md` inside the brackets. Links to files Obsidian cannot wikilink (anything under a dot-folder) stay markdown. Dangling links are legal and useful. Red links are the backlog of known-missing knowledge. Close any pass that wrote or moved links with `timeout 60 obsidian unresolved` (app running; dot-folder and folder targets are deliberate; grep-based checks miss path-qualified links to moved pages). (Convention since 2026-08-17; a documented deviation from OKF §5, recorded in meta/README.md.)
- **Uniqueness gate at creation.** Before writing a new wiki page, check its basename vault-wide (`obsidian file file=<name>`, or Glob when the app is closed). If it collides, choose a different name, or path-qualify every inbound link you write. Never create a second page with a name that already exists in wiki/, with one class excepted: **structural satellite names** (index.md, README.md, and the fixed satellite filenames a bundle design reuses across folders, such as the course bundles' logistics, next-actions, and objectives) always collide by design and are always path-qualified. The ban is for topic pages (amendment 2026-09-06).
- **Names are links too.** The first mention on a page of any person, entity, or project that holds a wiki page is a wikilink; later mentions on the same page may stay plain. A hub that describes another hub links it (amendment 2026-09-06, from the 2026-08-22 navigation probe).
- **Dependencies are links.** A claim that rests on another wiki page links to it in the sentence. Every link into wiki/ is a dependency edge for lint's purposes. There is no dependency list and no special phrasing.
- **Review receipts in prose.** When the user promotes a page, write one sentence at the top of the body linking to the record of the review: "Verified by Alex in the digest review of 2026-07-24 ([[wiki/log/2026-07-24|day log]])." Where no record file exists, the sentence carries date and context. `status:` and `verified_at:` stay in frontmatter as the machine label.
- **Never state another page's status or existence in prose.** Status and page-sets are designed to change, so such sentences are guaranteed to rot. Link the page and let readers weight it by its own frontmatter.
- Respect the user's style bindings in all prose you write: the word banlist and any style rules recorded beside it (both in `meta/DEPLOYMENT.md` § Style banlist). They bind at write time. Wiki pages are future agent context, so style debt compounds. Pages already carrying a violation get fixed opportunistically when a skill next touches them, or in a claim-neutral bulk style sweep the user directs (snapshot commit first; quoted speech, headings, receipts, code, and frozen records untouched; a mechanical check per page that links, URLs, dates, and quoted strings are unchanged; one day-log line per batch).

**Split under growth pressure, never at birth.** When a write would leave a page failing the boundary tests (CLAUDE.md § Page scoping), split along a subject seam: move the detail to a new page, keep a summary and a link on the parent, update both pages' `scope:` to name the new boundary, and path-qualify or regenerate any inbound links that named the old path (bare wikilinks keep resolving), except in `wiki/log/`, whose links are frozen with their entries (folder law in wiki/log/README.md). A name is an identity, so split conservatively and name for permanence and uniqueness. Never pre-create pages for subjects that might grow. The satellite pattern in wiki/projects/README.md is this rule's folder-local form.

**Adding to an existing `status: verified` page.** Never add, remove, or change a verified claim. Re-expressing the body is not a change to a claim (see Compaction below). <!-- constitution: principle 3, gate on status -->

- New material goes into the page's one `## Unreviewed additions` section as a dated entry (`- (YYYY-MM-DD) claim, with its inline citation`), and you set `pending_review: true`. A page never carries a second such section: if one exists, join it. The page-level `verified` then means "the reviewed core is verified"; the section is draft-grade until the user confirms it (the fold, below). The section exists only on verified pages: when a page is demoted to `draft`, merge its entries into the body (rename the heading or fold the entries into the sections that own them, no guards needed on a draft) and clear the flag, because on a draft page nothing is set apart from anything (amendment 2026-09-06).
- If an entry *contradicts* the verified core, flag the contradiction inside the entry and let it queue for the digest, and never auto-dispute the page.
- Verified claims change only through the correction flow (§ Corrections) or link maintenance (add a missing source link, repair a broken path), which asserts nothing new and runs unsupervised.

**Draft pages** supersede in place: later material updates the section that owns the subject and cites the new source inline. Write a dated section only for material that is itself an event record. Edit drafts freely otherwise.

**Compaction** re-expresses a verified page for cohesion without changing any claim. It runs unattended, at three moments: (a) at the fold, when the user confirms annex entries; (b) when ingest adds to a page whose annex section already holds three or more entries (compile the section into one coherent draft-grade block unless the section already carries a compaction receipt, in which case append the entry in the compiled shape; and also compact the core if the core carries no compaction receipt since its last review receipt, unless the page is a split candidate, since split precedes compact: then queue the core for the digest); (c) when an audit or digest flagged the page incohesive, at the next ingest touch or on request. Compaction never runs on draft pages and never on a length threshold. Expect cohesion, not shrinkage: a rewrite that keeps every claim rarely shortens a page much. Pages shrink over time through supersession (§ Corrections), not compaction.

- Procedure: read the whole page. Rewrite the body as one document organized by subject. Every claim keeps its date and its inline citation at the sentence it backs. Every review receipt sentence stays verbatim. Hedges and caveats stay with their claims. Inference stays marked as inference, observation and inference stay under separate headings, and the form otherwise fits the page. The annex section is compiled, never folded, except at the fold. Retitling an annex heading is not a merge.
- Guards, both required. Mechanical: `.claude/scripts/compaction-guard.py before after` (`--fold` at a fold) requires frontmatter identical except `updated:` (and `pending_review:`/`verified_at:` at a fold) and equal sets of wikilink targets, external URLs, ISO dates, and receipt sentences between the two bodies (at a fold, receipts compare by the review dates they name, since the folded headings carry the confirmation), the new compaction receipt excepted; additions fail as well as drops. The guard checks a compaction, not an ingest addition. Semantic: a second agent that has not seen the rewrite extracts numbered claims with citations from both bodies; every old claim must trace to a new one with its citation attached, and every new claim must trace to an old one. An unmatched new claim is the smuggling case and fails. Neither guard proves neutrality; together with git and audit sampling they make a bad rewrite detectable rather than silent. <!-- constitution: laundered inference -->
- On pass: replace the body, append the compaction receipt beside the review receipt ("Compacted YYYY-MM-DD, guards passed (link, URL, date sets equal; N claims traced both ways); last curator review YYYY-MM-DD, [[wiki/log/YYYY-MM-DD|day log]]"), one day-log line; a compaction performed by an unattended run also queues a one-line notice for the digest (its section 3), so unattended compactions land in front of the user. On refusal: apply nothing, queue the page and the guard report for the digest (its section 3).
- **The fold.** When the user confirms annex entries, run compaction with those entries treated as core, then delete them from the section; clear `pending_review` when the section is empty. A confirmed later state claim may replace an earlier "as of" claim on the same subject, with the earlier date kept in the sentence ("routed as of 07-27, having been stalled as of 07-25"). That supersession is where cohesion is won.

### 6. Connections

If the source reveals a substantive insight that two things relate (beyond a note merely mentioning a known entity, which is an ordinary link), create a page in `wiki/connections/` per that folder's README. Never write links into note bodies. Navigational `related:`/tag pointers in note frontmatter are the sweep's write-back (per process-inbox), not ingest's. Backlinks surface wiki-side links on the note automatically.

### 7. Close out

- Regenerate `index.md` in every folder you touched (source-stream folders you filed into count as touched). Derived files are sections of `* [[name|Title]] - description` lines pulled from frontmatter. Regenerate freely, never hand-maintain. `.claude/scripts/regen-index.py <folder>` does it mechanically and slots new pages for you to categorize. **Exception**: an `index.md` carrying page frontmatter (`type`/`title`/`status`) is an authored bundle hub, not a listing. Never regenerate it. Link new satellites from it instead (link maintenance).
- Append one entry per action to today's day log, `wiki/log/<YYYY-MM-DD>.md` (create it if missing, newest-first `* **Update**: …` lines).

## Corrections (when the source is the user's statement)

A correction file (provenance `"the user, <date>"`) reconciles rather than adds: locate every wiki page carrying the corrected claim, rewrite the affected claims citing the correction, and leave the superseded source in place. It stays as historical record, and the wiki layer outweighs it. A verbatim correction from the user is born `verified`. If a claim is withdrawn entirely, re-examine pages linking to it. Never retract silently.

**The walk is exhaustive and enumerated.** Backlinks of the superseded source (`obsidian backlinks path=<source>`, or grep the basename when the app is closed) find citers, and a vault-wide grep for the claim's distinctive tokens (its dates, values, names) finds restatements that never cited the source. Run both: a page can carry the claim without citing it. The day-log line lists the full reconciled set, fixed and checked-clean pages alike, so a missed carrier is visible in the record rather than silent until the next lint. (Added 2026-08-24 after a reconciliation healed one page and left two carriers stale for a week.)

The same authority extends by speaker, not by file shape: a dated statement in the user's own words, quoted verbatim in any filed source (a correction file, a session capture's verbatim section), authorizes reconciling the claims it supersedes, citing that source at the claim. Paraphrase does not. The superseded claim collapses to its supersession line; the source stays frozen.

## Don'ts

- **Laundered inference** — a guess written as a fact. Status fields and the observation/inference split exist to prevent it.
- **Promiscuous capture** — the user's sources decide the wiki's topics. Lookups never open new ones. On a page the user's material justifies, cited external reference content is welcome: who an entity is, established background, corroboration of a claim. Lookup-derived content doesn't cascade. Nothing found via lookup justifies creating further pages or importing further material. (notes/ and life exports are exempt: the user's own speech and scheduled personal exports are pre-curated by definition.)
- **Never edit a filed source, ever.** Corrections arrive as new sources.
