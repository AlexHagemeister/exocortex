---
name: lint
description: Run the vault's health checks — contradictions, staleness, withdrawn notes, expiry, conformance. Run weekly minimum on schedule, or when the user asks for a health pass or something seems inconsistent.
---

# Lint — vault health checks

You are the vault's immune system. Run every check below, fix what is mechanical, queue what needs the user, and write a report. Contradictions compound — never skip a scheduled run. Read the README of any folder you write to.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Acquire and release `.state/maintainer.lock` per the protocol in `.state/README.md` — first action and last action of the run.

Output: report to `.state/lint/<YYYY-MM-DD>.md` (findings + actions), items needing the user to `.state/lint/queue.md` (append; digest consumes this), one summary line to the day log (`wiki/log/<YYYY-MM-DD>.md`).

**Eviction guard, applies to every check:** a sync-layer placeholder file (e.g. `.<name>.icloud`) means the content was evicted — the file is *present*, just not local. Treat it as existing-but-unreadable; never as deleted, never as empty. If placeholders block a check, note it in the report and tell the user which files — none should appear on the current deployment.

## Checks

### 0. Graph compile (mechanical substrate)
Run `.claude/scripts/vault_graph.py` on its venv at `.claude/scripts/graph-venv/` (gitignored; rebuild if missing: `python3 -m venv .claude/scripts/graph-venv && .claude/scripts/graph-venv/bin/pip install networkx pyyaml`; a deployment may record local bindings in `meta/DEPLOYMENT.md`). It compiles wiki frontmatter + links into a typed graph and emits: YAML parse failures (feeds check 1), dangling and malformed `depends_on`/`sources`/body links (feeds check 8 — frontmatter edges included, which link-greps miss), the verified→draft dependency surface and `depends_on` cycles (report only), and transitive dependents for check 6's walk. The script emits facts; judgment stays with the checks below. If it fails, note that in the report and run the checks manually.

### 1. Frontmatter and page conformance
Fix mechanical violations (missing field with an obvious value); queue judgment calls.

**Scope:** every `wiki/**/*.md` except `log.md`/`log/`/`README.md`/derived `index.md` listings — an `index.md` carrying page frontmatter is an authored bundle hub (check 9's discriminator): check it like any page. Folder READMEs are Meta documentation, not claim-bearing pages — exempt from the `sources:` requirement. The YAML parse test also applies to `.state/issues/*.md`: `ISSUES.md` is derived from them and cannot be regenerated when one fails to parse.

**Frontmatter:** parseable YAML, non-empty `type`, `status` one of draft/verified/stale/disputed, `sources:` non-empty (or body explicitly marks inference-only). **"Parseable" means a real YAML parser accepts it** (`python3 -c "import yaml"` if available, else a strict scan: flag any unquoted scalar value containing `": "` or starting with a YAML-special character) — regex-only validation once passed frontmatter that Obsidian rejected.

**Links:** wiki bodies use standard markdown links with file-relative paths — flag any `[[wikilink]]` (the bundle must parse for external consumers) and any leading-slash link target (Obsidian resolves `/...` from vault root, not bundle root; such links are dead in the viewer).

**Quote provenance:** flag any blockquote carrying a speech attribution — a `— the user, <date>` signature or in-section said/wrote framing — with no source link in its section (enforces ingest's inline-quote-provenance rule; editorial callout boxes that merely mention the user are not quotes).

**Sources sync (additive only):** append any body link target under `sources/` missing from the list; never remove entries — `sources:` is built-from provenance and may legitimately exceed the body's links.

**Bundle membership:** a page inside a bundle folder belongs on that hub's satellite list — derivable from the path alone, so append missing entries unsupervised, each summarized from the satellite's own `description` line (hub law requires the summary). Append, never regenerate: the hub is prose. Cross-folder relationship links stay gated; check 8 stays report-only.

**Staged sections:** `pending_review: true` and the presence of an `## Unreviewed additions` section must imply each other — fix drift mechanically in either direction (set the missing flag; or clear a flag whose sections are gone). Every verified page carrying the flag goes to `.state/lint/queue.md` so the digest surfaces it.

**Type hygiene** — lifecycle policy attaches to `type`, never to folder:
- **Type/folder mismatch** (e.g. a non-Connection page in wiki/connections/): flag for the user's review; never apply a folder's lifecycle to a mismatched page — location can be wrong, the frontmatter is the claim.
- **New type without a lifecycle**: a `type` value not seen before (beyond Concept, Source summary, Synthesis, Connection, Meta, Project, Index) gets the default Concept lifecycle (no expiry, standard staleness) and a flag — introducing a type is silently a policy decision, so the user should see it. (`Project` — blessed by the user 2026-07-16 — and `Index` — blessed by the user 2026-07-31 for authored hub listings — use the default Concept lifecycle; design real project lifecycle behavior when a project first ends.)

### 2. Staleness decay
For each `verified` page, compare `verified_at` to the per-type half-life (placeholders, tune via `amend`: life/infrastructure facts **30d**, conceptual pages **180d**). Past it → set `status: stale` (leave `verified_at` as history), log. Stale only flags "re-verify before relying" — it destroys nothing, which is why this one clock may use wall-time.

### 3. Contradiction sweep
Scan for incompatible claim pairs across pages (same subject, conflicting values or assertions — grep shared tags/links, compare claims). **Symmetric** contradictions — two pages asserting incompatible things about a shared subject in the world — dispute both: `status: disputed`, both queued for the user. **Asymmetric** ones — one page wrong *about* another page (its status, existence, or metadata) or about its own frontmatter — queue only the asserting page with a proposed one-line fix; never demote a page for being described wrongly by someone else. Contradictions are detectable without ground truth — treat every one found as gold, not embarrassment.

### 4. Stale note-citations
For every wiki citation of `notes/<path> + read-timestamp`: if the note's current content hash differs from what the cursor recorded after that timestamp — the note changed since it was read. Queue the delta for re-ingest (note it in the report; `process-inbox` picks it up next sweep).

### 5. Deleted-note withdrawal
Consume `.state/deleted-notes.txt` (written by the sweep) plus any citation whose notes/ target has neither file nor sync placeholder. Deletion is withdrawal — a speech act, not a broken link to tolerate. Claims resting **solely** on a deleted note → page `status: disputed`, queued. Claims with surviving corroboration keep their status; remove the dead citation, log. Re-read every citing page at consumption: standing flags or action items sourced to the deleted note are queued for the user — withdrawn evidence must never keep flagging. A citation deliberately kept as an annotated tombstone ("deleted <date>") is already reconciled: keep it, don't re-flag.

### 6. Retraction walk
For every page disputed or invalidated this run: walk its inbound links (grep for links to its path) and every page listing it in `depends_on`; re-examine each dependent — does its claim still stand without the retracted support? Demote to `draft` or `disputed` accordingly. Never retract silently: local healing is global poisoning. Log every retraction.

### 7. Connection expiry (this check is the expiry rule's single home)
For each **`type: Connection`** draft page — wherever it lives, normally `wiki/connections/` — count user review markers in `.state/review-markers/` dated after the page's creation. **≥3 reviewed digests and still unpromoted** → presumed noise: delete the page, log it in the day log (recoverable from git history). The clock counts review events, never wall-clock days — a vacation must not expire good drafts. <!-- constitution: principle 6, human-gated clocks -->

Why type-keyed: expiry exists to garbage-collect *unsolicited machine-generated relationship hypotheses* (sweep exhaust, high volume, low average value). It never applies to other types — a `type: Synthesis` page answered a question the user actually asked, so the presumed-noise rationale fails; Syntheses live under the ordinary draft lifecycle regardless of folder.

### 8. Orphans and red links
List pages with no inbound links (orphans) and dangling link targets (red links). Neither is an error — red links are the backlog of known-missing knowledge. Triage: orphans worth linking, red links worth writing → report (digest may surface the top few); the rest stand.

Also report check 0's **basename-fallback exposure** every run: the count of edges resolving only because one file in `wiki/` carries that name, and the basenames the most edges depend on. Creating any second file with one of those names silently breaks all of them at once, with no edit to the citing pages — so this count is a standing measure of fragility, not a finding to fix. Report it as a number and a trend; any edge listed as ALREADY BROKEN is a real finding and gets repaired to file-relative form (claim-neutral link maintenance).

### 9. Surface consistency
Skim CLAUDE.md, GLOSSARY.md, the skill files, and folder READMEs against CONSTITUTION.md's principles and against each other. A derived surface contradicting the constitution, or two surfaces contradicting each other, is a bug: report it and file it as an issue (per ISSUES.md) — fixing rules goes through `amend`, never a silent edit. Glossary `_Home:_` pointers should resolve to real surfaces.

Also regenerate any `index.md` that has drifted from its folder's actual contents (indexes are derived; regenerate freely — but an `index.md` carrying **page** frontmatter (`type`/`title`/`status`) is an authored bundle hub (hub law: wiki/projects/README.md): never regenerate it as a listing. A derived index's `updated:` stamp is not page frontmatter).

### 10. Bundle and merge candidates
For each flat `type: Project` hub page (no folder of its own): if edits since the last review marker land across several distinct sections — the sections are churning independently — queue it in `.state/lint/queue.md` as a bundle candidate. Splitting existing prose needs the user's eye for the seams; never split unprompted. (New growth doesn't need this check — the projects README routes it to satellites at write time.)

The reverse check, for each satellite inside a bundle: if it has stayed thin — a screenful or less — and unchanged since the review marker before last, queue it in `.state/lint/queue.md` as a merge-back candidate; its claims may belong on the hub. Merging existing prose is the user's call, same as splitting — never merge unprompted.
