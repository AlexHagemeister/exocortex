---
name: amend
description: Change the system's rules, skills, or wiki folder structure — always with the user's approval. Use when a rule needs changing, the same rule has been overridden ~3 times, a skill misfires repeatedly, or a wiki/ folder refactor is requested.
---

# Amend — change the rules, deliberately

The rules are a pact the user authored and may renegotiate — never a cage, and never silently bent. You propose; the user decides; you propagate. Nothing in this skill executes without explicit approval. Read the README of any folder you write to.

## When to propose (don't wait to be asked)

- **~3 overrides of the same rule** — scan `wiki/log/` exception entries. Repeated overrides indict the rule, not the user; exceptions are bugs, amendments are fixes.
- **Issue clusters** — ~3 open issues in `.state/issues/` sharing a `rule:` value (this skill is the threshold's one home).
- **A tripwire fired** — e.g., digest review exceeding ~15 minutes means the triage cap or scoring needs tightening.

## Amending a rule

1. **Consult CONSTITUTION.md** (vault root) — the principles the rules derive from, the anti-pattern catalog, and the residence map. A proposal that contradicts a principle needs the principle changed too — rare and deliberate. **Push back in plain language before asking for approval:** name the principle, explain the tradeoff, offer a conforming alternative and the override. The user still decides after that brief — never silent refuse, never silent comply.
2. **Locate the rule's one home** via the residence map: invariants → CLAUDE.md; procedures → the owning skill; folder law → that folder's README; user-only norms → CONSTITUTION.md. No rule lives twice — if you find a rule duplicated across surfaces, that's a bug to fix in the same pass.
3. **Propose to the user**: current rule, observed friction (cite log/ISSUES entries), proposed wording, which principle it serves (and any principle it tensions with, from step 1). Wait for approval. Do not freestyle core behavior from a vague "make it better" — translate that into a concrete proposal or ask what hurts.
4. **Execute**: edit the one home. If the change introduces or renames system jargon, update GLOSSARY.md in the same pass; if the term is in the public README Key terms subset, update that too (or publish will fail the drift check). Grep the vault for traceability anchors (`<!-- constitution:`) and restatements of the old rule; update every echo. Keep runtime vocabulary universal — "you" and "the user", no role nouns.
5. **Guard the budget**: CLAUDE.md has a hard budget of one page. If an amendment grows it past that, something on it belongs in a skill or README instead — move it, don't squeeze it.
6. **Verify**: run lint's surface-consistency check (check 9) over the touched surfaces.
7. **Log** the amendment in the day log, `wiki/log/<YYYY-MM-DD>.md` (what changed, why, who approved), and close any issues it resolves per ISSUES.md.
8. **Monitor** — a shipped amendment is a hypothesis, not a settled fact. For any change with observable downstream behavior, open a tracking issue in `.state/issues/` linking the day-log entry and the issues or sources where the objectives were first stated: what each change should do, what evidence of working looks like and where it accrues (day logs, lint reports), and a close condition a few cycles out. Evaluate against both the original friction and the principles the change claimed to serve. Close on evidence; if the evidence goes the other way, propose the adjustment or revert — don't wait for friction to re-accumulate.

## Folder refactors are migrations

A wiki page's path IS its identity — a rename breaks every inbound link, so wiki/ is never reorganized casually:

1. **Propose**: old → new mapping for every affected path, and why the new shape earns the breakage. Top-level folders are the user's choice, few and stable.
2. **User approves.** No approval, no move.
3. **Execute atomically**: move files; rewrite every inbound link vault-wide (grep old paths across wiki/ — links are file-relative standard markdown, so a move changes both the moved page's outbound links and every inbound link); regenerate every touched `index.md`; update `.state/` records citing old paths.
4. **Log** the migration in the day log with the full mapping. Consider running `vault-snapshot` first so there's a pre-migration point to roll back to.

## Don'ts

- Never edit CLAUDE.md, skills, or READMEs outside this procedure — even for typos, propose first (cheap ceremony, and it keeps the user's model of the rules exact).
- Never reorganize wiki/ as a side effect of other work.
- Never resolve rule friction by adding a second, contradicting copy of a rule somewhere else — amend the one home.
