---
name: amend
scope: "The procedure for changing rules, skills, and wiki folder structure, including the skill frontmatter law. Approval is always the user's; knowledge changes go through ingest, not here."
description: Change the system's rules, skills, or wiki folder structure, always with the user's approval. Use when a rule needs changing, the same rule has been overridden ~3 times, a skill misfires repeatedly, or a wiki/ folder refactor is requested.
---

# Amend — change the rules, deliberately

The rules are a pact the user authored and may renegotiate, never a cage and never silently bent. You propose. The user decides. You propagate. Nothing in this skill executes without explicit approval. Read the README of any folder you write to.

## When to propose (don't wait to be asked)

- **~3 overrides of the same rule**: scan `wiki/log/` exception entries. Repeated overrides indict the rule, not the user. Exceptions are bugs, amendments are fixes.
- **Issue clusters**: ~3 open issues in `.state/issues/` sharing a rule (this skill is the threshold's one home). Matching is at the level of rule components or subjects appearing within `rule:` values (e.g. ingest/step-5, or maintainer.lock named inside longer values), not exact-string equality of whole values (amendment 2026-08-27).
- **A tripwire fired**: e.g., the digest's review-time tripwire (threshold lives in the digest skill) means the triage cap or scoring needs tightening.

**Scope note (the user's ruling, 2026-08-27):** machine-global Claude Code configuration changed from the user's personal preference (files under `~/.claude`) is recorded in `wiki/craft/` via the pipeline, not amended. Vault-specific configuration destined to ship with the program routes through this skill.

## Amending a rule

1. **Consult CONSTITUTION.md** (vault root): the principles the rules derive from, the anti-pattern catalog, and the residence map. A proposal that contradicts a principle needs the principle changed too (rare and deliberate). **Push back in plain language before asking for approval:** name the principle, explain the tradeoff, offer a conforming alternative and the override. The user still decides after that brief. Never silently refuse, never silently comply.
2. **Locate the rule's one home** via the residence map: invariants → CLAUDE.md; procedures → the owning skill; folder law → that folder's README; user-only norms → CONSTITUTION.md. No rule lives twice. If you find a rule duplicated across surfaces, that's a bug to fix in the same pass.
3. **Propose to the user**: current rule, observed friction (cite log/ISSUES entries), proposed wording, which principle it serves (and any principle it tensions with, from step 1). If the rule is enforcement-grade, meaning mechanically checkable from tool inputs or cheap filesystem state, propose a hook alongside or instead of the prose wording; a rule that could be a hook but lives only in prose is an underused enforcement layer (the user's ruling, 2026-08-27). A hook is the wrong home when the instruction is the behavior itself (the agent would fail first and recover after the hook fires), or when it fires far wider than the rule binds and pays in context noise. Hooks serve rules living where they bind, progressive disclosure, and backstops for prose the agent sometimes drops (the user's refinement, 2026-09-04). "Alongside" holds at proposal time only: when the enforcement ships, the retirement split (below) takes the mechanized part out of the prose. Wait for approval. Do not freestyle core behavior from a vague "make it better". Translate that into a concrete proposal or ask what hurts. If the amendment creates a skill or script, propose its classification, ship or private, in the same approval (the classification record and its location are named in meta/DEPLOYMENT.md). A deployment that publishes nothing has no record to update and skips this.
4. **Execute**: edit the one home. If the change introduces or renames system jargon, update GLOSSARY.md in the same pass. Grep the vault for traceability anchors (`<!-- constitution:`) and restatements of the old rule. Update every echo. Keep runtime vocabulary universal: "you" and "the user", no role nouns.
5. **Guard the budget**: CLAUDE.md has a hard budget of one page. If an amendment grows it past that, something on it belongs in a skill or README instead. Move it, don't squeeze it.
6. **Verify**: run lint's surface-consistency check (check 9) over the touched surfaces.
7. **Log** the amendment in the day log, via `.claude/scripts/day-log.sh` (what changed, why, who approved), and close any issues it resolves per ISSUES.md.
8. **Monitor.** A shipped amendment is a hypothesis, not a settled fact. For any change with observable downstream behavior, open a tracking issue in `.state/issues/` (frontmatter `kind: watch`) linking the day-log entry and the issues or sources where the objectives were first stated. The issue covers:
   - the amended text, quoted from the file it lives in
   - what evidence of working looks like and where it accrues (day logs, lint reports)
   - a close condition a few cycles out. One issue may track several changes approved together only if it states a close condition per item, so each item closes on its own evidence and partial closure is legal; the file closes when every item has (amendment 2026-09-06).
   - Evaluate against both the original friction and the principles the change claimed to serve. Close on evidence. If the evidence goes the other way, propose the adjustment or revert. Don't wait for friction to re-accumulate.

## The retirement split

When deterministic enforcement ships for a rule (a hook, a script check, a schema), the same amendment retires the mechanized part of the rule's prose: delete it or shrink it to a one-line pointer naming the enforcement. The judgment residue, what no code can check, stays as instruction. A rule restated in prose beside its enforcement is a rule living twice. (Adopted 2026-09-01, compilable-knowledge amendment; pacing law lives with the deployment's claim conventions, where those exist.)

## Skill frontmatter law

Every skill in `.claude/skills/` carries a `scope:` frontmatter field, its boundary contract for maintainers: what the skill owns, what it does not, and where the excluded work lives. The router never sees it (only `name` and `description` reach the trigger decision). It exists so recalibration over time has a fixed standard, and a skill whose accumulated work has outgrown its scope is a split candidate. Write it when creating a skill. Update it in the same pass as any change that moves the skill's boundary.

## Folder refactors are migrations

A wiki page's name is its identity. Bare wikilinks survive a folder move, but path-qualified links, index listings, and dated records name the path, and a rename breaks every inbound link unless Obsidian performs it, so wiki/ is never reorganized casually:

1. **Propose**: old → new mapping for every affected path, and why the new shape earns the breakage. Top-level folders are the user's choice, few and stable.
2. **User approves.** No approval, no move.
3. **Execute atomically**:
   - move files (renames go through `obsidian rename` so the app rewrites inbound wikilinks; folder moves may use `mv`)
   - grep the old path vault-wide and rewrite what still names it (path-qualified wikilinks, and any markdown links in dot-folder or transitional surfaces)
   - regenerate every touched `index.md`
   - update `.state/` records citing old paths
   - close with `timeout 60 obsidian unresolved` (grep misses path-qualified links to moved pages)
4. **Log** the migration in the day log with the full mapping. Consider running `vault-snapshot` first so there's a pre-migration point to roll back to.

## Don'ts

- Never edit CLAUDE.md, skills, or READMEs outside this procedure. Even for typos, propose first (cheap ceremony, and it keeps the user's model of the rules exact).
- Never reorganize wiki/ as a side effect of other work.
- Never resolve rule friction by adding a second, contradicting copy of a rule somewhere else. Amend the one home.
