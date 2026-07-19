---
name: digest
description: Compile the review surface — new connections, disputes, promotion shortlist, friction log. Run on the deployment schedule or when the user asks "what needs my review" or wants the digest.
---

# Digest — the user's review surface

This is the system's one human loop: the user reads the digest, acts on it, and never audits the vault wholesale. Everything below is push — insights and decisions reach the user unprompted. Read the README of any folder you write to.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context — its rules bind the run. Compile only — never promote, never write a review marker — and acquire/release `.state/maintainer.lock` per the protocol in `.state/README.md` as the run's first and last action. End the run summary with: "Digest ready for review — open it in any vault session and say 'review the digest'."

The last review marker in `.state/review-markers/` defines "since last review" for everything below.

## Compile

Write to `.state/digests/<YYYY-MM-DD>.md` and present it in full to the user:

1. **Recap** — a few lines: what entered the wiki since last review (ingests, syntheses, notable log entries).
2. **New connection pages** — every `wiki/connections/` page created since last review, with its one-line description. Also note connections nearing expiry (2 reviewed digests without promotion) — last call.
3. **Disputes and withdrawals** — everything in `.state/lint/queue.md`: contradiction pairs, deleted-note demotions, judgment calls. These need adjudication.
3b. **Verified pages with unreviewed additions** — every `pending_review: true` page, with one line per staged addition (and any flagged contradictions with the core called out).
4. **Promotion shortlist** — see triage below. **Hard cap: 5–10 items.**
5. **Open issues** — everything `status: open` in `.state/issues/` (ISSUES.md is the derived index); these drive rule changes. When the user settles one, close it: flip `status`, fill `resolved_by`, regenerate ISSUES.md.

## Promotion triage (leverage-ranked, hard-capped)

Score draft pages by:
- **Graph centrality** — hub pages many others link to or depend on; verifying a hub de-risks everything downstream.
- **Query traffic** — drafts recently relied on in answers (`.state/query-traffic.txt`); the most-used claims should verify fastest.
- **Dispute adjacency** — drafts that disputed pages depend on, or that sit near contested territory.

Take the top 5–10, never more. Everything below the cap **stays draft indefinitely — that is correct, not a backlog.** Verified is scarce by design; do not present the draft fraction as a problem or pad the list. <!-- constitution: principle 3, gate on status -->

## Review

For each shortlist item the user **explicitly confirms**: set `status: verified`, `verified_at`, add `"user confirmed in digest review, <date>"` to `sources:`, log in the day log (`wiki/log/<YYYY-MM-DD>.md`).

For each **staged addition** the user confirms: merge it into the page's core prose (integrated, not appended), delete the annex section, clear `pending_review` when no annex sections remain, log. If the user corrects it instead, route their statement through the correction flow; if they reject it, delete the annex section and log the rejection. Explicit assent only — a nod at the digest as a whole promotes nothing. Disputes: apply whatever the user adjudicates (which claim wins, what demotes), via the correction flow where their ruling is new speech (write it to `sources/inbox/` with provenance `"the user, <date>"`).

**When the user finishes reviewing** (says so, or has acted on the items): write the marker `.state/review-markers/<YYYY-MM-DD>` (second review same day: `-2`, then `-3`, …) — this review event is what connection-expiry and draft-lifecycle clocks count. Never write a marker for an unreviewed digest.

## The 15-minute tripwire

If review runs past ~15 minutes (or the user says it's too long): the cap or the scoring is wrong. Tighten via an `amend` proposal — **fix the digest, never the user's schedule.** Do not ask the user to review more often or longer.
