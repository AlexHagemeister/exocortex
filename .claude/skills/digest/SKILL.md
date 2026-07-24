---
name: digest
description: Compile the review surface — new connections, disputes, promotion shortlist, friction log. Run on the deployment schedule or when the user asks "what needs my review" or wants the digest.
---

# Digest — the user's review surface

This is the system's one human loop: the user reads the digest, acts on it, and never audits the vault wholesale. Everything below is push — insights and decisions reach the user unprompted. Read the README of any folder you write to.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Compile only — never promote, never write a review marker — and acquire/release `.state/maintainer.lock` per the protocol in `.state/README.md` as the run's first and last action. End the run summary with: "Digest ready for review — open it in any vault session and say 'review the digest'."

The last review marker in `.state/review-markers/` defines "since last review" for everything below.

## Compile

**Decision budget: ~10–15 items total per digest**, leverage-ranked across sections 2–4 using the triage scoring below. Everything past the budget carries over, ranked, to the next digest, with a one-line count of what carried — carried items are not a backlog. The review's value is depth per item, not coverage (the user, 2026-07-20: it's "basically akin to journaling", and doing it well "takes time for each file") — size every digest for unhurried engagement.

Write to `.state/digests/<YYYY-MM-DD>.md` and present it in full to the user:

1. **Recap** — a few lines: what entered the wiki since last review (ingests, syntheses, notable log entries).
2. **New connection pages** — every `wiki/connections/` page created since last review, with its one-line description. Also note connections one review short of lint check 7's expiry bar — last call.
3. **Disputes and withdrawals** — everything in `.state/lint/queue.md`: contradiction pairs, deleted-note demotions, judgment calls. These need adjudication.
3b. **Verified pages with unreviewed additions** — every `pending_review: true` page, with one line per staged addition (and any flagged contradictions with the core called out).
4. **Promotion shortlist** — see triage below. **Hard cap: 5–10 items.**
5. **Issues needing the user** — open issues explicitly queued for his decision or at the amend skill's cluster threshold; the rest of the open set is a one-line count (routine evidence-based closures belong to issue grooming, not this surface). When the user settles one, close it per ISSUES.md.
6. **Program update, if one exists** — `git fetch` the program clone (path in meta/DEPLOYMENT.md; skip silently if UNSET) and compare the latest release to the installed version. Newer release → one line: the version, and "say 'update my exocortex' to see what changed." Outside the decision budget; never applies anything.

## Promotion triage (leverage-ranked, hard-capped)

Score draft pages by:
- **Graph centrality** — hub pages many others link to or depend on; verifying a hub de-risks everything downstream.
- **Query traffic** — drafts recently relied on in answers (`.state/query-traffic.txt`); the most-used claims should verify fastest.
- **Dispute adjacency** — drafts that disputed pages depend on, or that sit near contested territory.

Take the top 5–10, never more. Everything below the cap **stays draft indefinitely — that is correct, not a backlog.** Verified is scarce by design; do not present the draft fraction as a problem or pad the list. <!-- constitution: principle 3, gate on status -->

## Review

Run the shortlist through the `audit-exocortex` skill's loop — one page per turn, its brief format and verdict mechanics. Promotions in digest context record `"user confirmed in digest review, <date>"` as the `sources:` line.

For each **staged addition** the user confirms: merge it into the page's core prose (integrated, not appended), delete the annex section, clear `pending_review` when no annex sections remain, log. If the user corrects it instead, route their statement through the correction flow; if they reject it, delete the annex section and log the rejection. Explicit assent only — a nod at the digest as a whole promotes nothing. Disputes: apply whatever the user adjudicates (which claim wins, what demotes), via the correction flow where their ruling is new speech (write it to `sources/inbox/` with provenance `"the user, <date>"`).

**When the user finishes reviewing** (says so, or has acted on the items): write the marker `.state/review-markers/<YYYY-MM-DD>` (second review same day: `-2`, then `-3`, …) — this review event is what connection-expiry and draft-lifecycle clocks count. Never write a marker for an unreviewed digest. If act-evidence shows a review that never got its marker (`verified_at` stamps or day-log review entries since the last marker), write it retroactively — dated to the acts, noted as reconstructed. Unattended runs surface the evidence in the digest instead of writing the marker.

## The 15-minute tripwire

If review runs past ~15 minutes (or the user says it's too long): the cap or the scoring is wrong. Tighten via an `amend` proposal — **fix the digest, never the user's schedule.** Do not ask the user to review more often or longer. (The user choosing to review in smaller, more frequent sittings is a different thing — expected and healthy; the weekly schedule is an anchor, not a batch size, and each sitting writes a marker and advances the clocks.)
