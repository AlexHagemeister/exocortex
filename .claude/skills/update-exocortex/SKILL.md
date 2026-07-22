---
name: update-exocortex
description: Pull the latest exocortex program release and apply it to this vault — reconciling local amendments, never touching data. Use when the user asks to update their exocortex, update this system's rules and skills, or check for exocortex updates.
---

# Update exocortex — take upstream, keep what's yours

The program repo ships new rules and skills; this skill brings them into an existing vault. It updates **program files only** (CLAUDE.md, CONSTITUTION.md, GLOSSARY.md, shipped skills, templates, meta reference docs) and never touches wiki/, sources/, notes/, .state/ working files, or meta/DEPLOYMENT.md. Local rule amendments are legitimate forks — an update must never silently undo one.

## Bindings

Read `meta/DEPLOYMENT.md`:

- **Program repo clone** — local path + upstream URL. If UNSET, help the user clone the program repo to a stable path and record it, then continue.
- **Program version** — the installed release. If the row is absent, derive it from the clone's current HEAD before pulling, and add the row when done.

If this vault is the program's *source* (publish-program is configured here), stop: you are upstream, updates flow the other way.

## Procedure

1. **Check.** `git fetch` in the clone; compare the installed version to the latest release. Nothing new → report "up to date", done. Otherwise summarize the CHANGELOG entries in between — that is the payload the user is approving.
2. **Gate.** The user decides whether to apply. Updating the operating rules is their act, every time.
3. **Rollback point.** Run `vault-snapshot` (or at minimum commit a clean vault state) so the whole update is one revertible commit.
4. **Pull and reconcile.** `git pull` in the clone. Diff every shipped program file against the vault's copy. Each difference is one of:
   - upstream change only → take it;
   - a local amendment (made via `amend`) → surface it and ask: keep yours, take upstream, or merge;
   - a user-added local skill not shipped upstream → preserve it (`bootstrap.sh --update` deletes unknown files under `.claude/skills/` — set it aside first).
5. **Apply.** `./tools/bootstrap.sh <vault> --update` from the clone, then restore kept-local, merged, and user-added files from step 4.
6. **Verify.** Show the user the vault's git diff — it should contain exactly the approved payload plus reconciliations. Commit (`update: program <old> → <new>`).
7. **Record.** Stamp the new version in DEPLOYMENT.md § Program version; one line in the day log (`wiki/log/<YYYY-MM-DD>.md`): old → new, what was reconciled or kept.
