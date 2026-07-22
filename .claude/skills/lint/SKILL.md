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

### 1. Frontmatter conformance
Every `wiki/**/*.md` except `index.md`/`log.md`/`log/`/`README.md`: parseable YAML frontmatter, non-empty `type`, `status` one of draft/verified/stale/disputed, `sources:` non-empty (or body explicitly marks inference-only). Folder READMEs are Meta documentation, not claim-bearing pages — exempt from the `sources:` requirement. **"Parseable" means a real YAML parser accepts it** (`python3 -c "import yaml"` if available, else a strict scan: flag any unquoted scalar value containing `": "` or starting with a YAML-special character) — regex-only validation once passed frontmatter that Obsidian rejected. Apply the same test to `.state/issues/*.md`: `ISSUES.md` is derived from them and cannot be regenerated when one fails to parse. Wiki bodies use standard markdown links with file-relative paths — flag any `[[wikilink]]` (the bundle must parse for external consumers) and any leading-slash link target (Obsidian resolves `/...` from vault root, not bundle root; such links are dead in the viewer). Flag any user-attributed blockquote with no source link in its section (enforces ingest's inline-quote-provenance rule). Sync `sources:` additively: append any body link target under `sources/` missing from the list; never remove entries — `sources:` is built-from provenance and may legitimately exceed the body's links. Fix mechanical violations (missing field with an obvious value); queue judgment calls.

Staged-sections hygiene: `pending_review: true` and the presence of an `## Unreviewed additions` section must imply each other — fix drift mechanically in either direction (set the missing flag; or clear a flag whose sections are gone). Every verified page carrying the flag goes to `.state/lint/queue.md` so the digest surfaces it.

Two type-hygiene rules — lifecycle policy attaches to `type`, never to folder:
- **Type/folder mismatch** (e.g. a non-Connection page in wiki/connections/): flag for the user's review; never apply a folder's lifecycle to a mismatched page — location can be wrong, the frontmatter is the claim.
- **New type without a lifecycle**: a `type` value not seen before (beyond Concept, Source summary, Synthesis, Connection, Meta, Project) gets the default Concept lifecycle (no expiry, standard staleness) and a flag — introducing a type is silently a policy decision, so the user should see it. (`Project` — blessed by the user 2026-07-16 — currently uses the default Concept lifecycle; design real project lifecycle behavior when a project first ends.)

### 2. Staleness decay
For each `verified` page, compare `verified_at` to the per-type half-life (placeholders, tune via `amend`: life/infrastructure facts **30d**, conceptual pages **180d**). Past it → set `status: stale` (leave `verified_at` as history), log. Stale only flags "re-verify before relying" — it destroys nothing, which is why this one clock may use wall-time.

### 3. Contradiction sweep
Scan for incompatible claim pairs across pages (same subject, conflicting values or assertions — grep shared tags/links, compare claims). Both pages → `status: disputed`, both queued for the user. Contradictions are detectable without ground truth — treat every one found as gold, not embarrassment.

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

### 9. Surface consistency
Skim CLAUDE.md, GLOSSARY.md, the skill files, and folder READMEs against CONSTITUTION.md's principles and against each other. A derived surface contradicting the constitution, or two surfaces contradicting each other, is a bug: report it and file it as an issue (per ISSUES.md) — fixing rules goes through `amend`, never a silent edit. Glossary `_Home:_` pointers should resolve to real surfaces.

Also regenerate any `index.md` that has drifted from its folder's actual contents (indexes are derived; regenerate freely).
