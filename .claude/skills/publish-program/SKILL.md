---
name: publish-program
description: Sync the vault's portable system files into the public program repo, leak-scan, and push after the user reviews the diff. Use after an approved amendment changes rules or skills, or when the user asks to publish or update the public repo.
---

# Publish program — ship the rules, never the data

The public program repo carries the system's shippable surface — per CONSTITUTION.md § Sharing and boundaries: the program is markdown with no personal data. This skill moves changes vault → repo. It never moves anything repo → vault, never runs unattended, and never pushes without the user seeing the diff.

## Bindings

Read `meta/DEPLOYMENT.md` for the public program repo's local clone path. **If it is UNSET, stop and ask the user.** The clone is a separate repo from the private mirror; the two never share a remote or a command.

## Procedure

1. **Sync.** Run `tools/sync.sh` in the clone. It copies only MANIFEST-allowlisted paths and leak-scans the result. A scan failure stops everything — report the hits to the user; never "fix" a hit by weakening the scan.
2. **Review.** Show the user the resulting `git diff` (or state "no changes"). Wait for their approval — publishing is their act, every time.
3. **Push.** On approval: commit in the clone (`sync from vault <ISO 8601 date>`), then `tools/sync.sh --push` — the script verifies the remote is the public repo, not the mirror, before pushing.
4. **Log.** One line in the day log (`wiki/log/<YYYY-MM-DD>.md`).

## Scope changes are publishing decisions

Adding a path to MANIFEST publishes a new part of the vault — propose it to the user explicitly, never bundle it silently into a sync. The repo's own files (README, SETUP, tools/) are edited in the repo directly; the vault remains the one home for every rule and skill, so rule changes always go amend-first, publish-second.
