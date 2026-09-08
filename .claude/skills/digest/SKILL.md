---
name: digest
scope: "Compiling the review surface and closing its loop: triage scoring, the decision budget, annex-entry verdicts (the fold itself lives in ingest), interview verdicts, and review markers. The per-page brief and verdict mechanics live in audit-exocortex, and the adjudication items it compiles come from lint's queue, never its own detection."
description: "Compile the review surface: new connections, disputes, promotion shortlist, self-interview, friction log. Run on the deployment schedule or when the user asks \"what needs my review\" or wants the digest."
---

# Digest — the user's review surface

This is the system's one human loop. The user reads the digest, acts on it, and never audits the vault wholesale. Everything below is push. Insights and decisions reach the user unprompted. Read the README of any folder you write to.

**Unattended (scheduled) runs**: read CLAUDE.md at the vault root first if it isn't already in your context. Its rules bind the run. Compile only (never promote, never write a review marker) and acquire/release `.state/maintainer.lock` per the protocol in `.state/README.md` as the run's first and last action. End the run summary with: "Digest ready for review. Open it in any vault session and say 'review the digest'."

The last review marker in `.state/review-markers/` defines "since last review" for everything below.

## Compile

0. **Lint recency gate.** Section 3 is only as fresh as `.state/lint/queue.md`. Before compiling, compare the newest report in `.state/lint/` against the last review marker and against lint's weekly cadence. If lint has not run since the last review, or its newest report is more than seven days old, either run `lint` inline first (interactive runs) or open the digest with one line stating the queue's age so the reader weights section 3 accordingly (unattended runs, which never invoke lint). Same shape as chronicle's step 0 inbox gate (amendment 2026-09-06).

- **Decision budget: ~10–15 items total per digest**, leverage-ranked across sections 3–4 using the triage scoring below. Section 2 is a complete listing, never budgeted or carried, because connection expiry presumes the user saw the page.
- Everything past the budget carries over, ranked, to the next digest, with a one-line count of what carried. Carried items are not a backlog.
- The review's value is depth per item, not coverage (the user, 2026-07-20: it's "basically akin to journaling", and doing it well "takes time for each file"). Size every digest for unhurried engagement.

Write to `.state/digests/<YYYY-MM-DD>.md` and present it in full to the user:

1. **Recap**: a few lines: what entered the wiki since last review (ingests, syntheses, notable log entries).
2. **New connection pages**: every `wiki/connections/` page created since last review, with its one-line description. Also note connections one review short of lint check 7's expiry bar (last call).
2b. **Quarantined captures**: every item in `sources/inbox/quarantine/`, one line each with its age. Not budgeted or carried, same as section 2. An item can otherwise sit there indefinitely with no other surface raising it. Keep or discard is your call. Grooming does not touch this folder.
3. **Disputes and withdrawals**: everything in `.state/lint/queue.md`: contradiction pairs, deleted-note demotions, judgment calls, and compactions the guards refused since the last review, with their guard reports. These need adjudication.
3b. **Verified pages with unreviewed additions**: one item per `pending_review: true` page: the page, and its annex entries as a numbered claim list with citations (any flagged contradictions with the core called out). Verdicts are per claim (confirm, correct, reject) or per page ("all confirmed"). The user reviews claims, never prose.
4. **Promotion shortlist**: see triage below. **Hard cap: 5–10 items.**
4b. **Self-interview**: 1–3 question-shaped items about the user as a person, counted inside the decision budget. Three flavors:
   - **blind-spot**: an unconfirmed pattern-claim with cited receipts. Behavioral traces license behavior-only phrasing: state the pattern, leave the interpretation to the user.
   - **disclosure**: something the system genuinely doesn't know and needs to ask.
   - **negative-space**: a structural absence neither party has articulated.

   Do not soften. Confronting material (contradictions, shadow-self candidates, patterns the user may not welcome) is explicitly in scope and explicitly valued (the user, 2026-07-24). The Off limits section on `wiki/life/self-model.md` is the only topic restriction. Zero items is fine. Never pad, never manufacture a candidate from thin evidence. Page law: `wiki/life/README.md`.
4c. **Judgment calls**: every day-log line beginning `Judgment:` since last review, counted inside the decision budget. **Cap: 5.** Calls may be presented grouped by pattern (same call, same reasoning, N instances) with one verdict per group. Individual presentation is reserved for novel, consequential, or built-on calls. The cap applies to presented items, not raw lines (amendment 2026-08-27). Prefer interactive-session calls and calls later work built on. Overflow carries over ranked, like sections 3–4. The user confirms or corrects each line. A correction is the user's new speech, route it through the correction flow.
5. **Issues needing the user**: open issues explicitly queued for his decision or at the amend skill's cluster threshold. The rest of the open set is a one-line count (routine evidence-based closures belong to issue grooming, not this surface). When the user settles one, close it per ISSUES.md.
6. **Program update, if one exists**: if this vault is the program's *source* (a check both this skill and update-exocortex make, based on the deployment's publishing configuration), skip this item. Otherwise `git fetch` the program clone (path in meta/DEPLOYMENT.md, skip silently if UNSET) and compare the latest release to the installed version (DEPLOYMENT § Program version; row absent → derive from the clone's current HEAD, as update-exocortex does). Newer release → one line: the version, and "say 'update my exocortex' to see what changed." Outside the decision budget. This item never applies anything.

**Decision item shape.** Every item that asks for a verdict is one bullet: the thing (linked), the problem, the proposed fix, the question stated plainly, a default with one line of reasoning, and what happens if the user does nothing. Mark which items want a verdict now and which are parked and will resurface on their own. Where an item offers options, number them and name the one to take. A menu with no recommendation is not a decision item. (Promoted from the user's house style, amendment 2026-09-01.)

## Promotion triage (leverage-ranked, hard-capped)

Score draft pages by:
- **Graph centrality**: hub pages many others link to or depend on. Verifying a hub de-risks everything downstream.
- **Query traffic**: drafts recently relied on in answers (`.state/query-traffic.txt`). The most-used claims should verify fastest.
- **Dispute adjacency**: drafts that disputed pages depend on, or that sit near contested territory.

Take the top 5–10, never more. Everything below the cap **stays draft indefinitely. That is correct, not a backlog.** Verified is scarce by design, so do not present the draft fraction as a problem or pad the list. <!-- constitution: principle 3, gate on status -->

## Review

Run the shortlist through the `audit-exocortex` skill's loop: one page per turn, its brief format and verdict mechanics. Promotions in digest context write the receipt sentence at the top of the page body: "Verified by Alex in the digest review of <date> ([[wiki/log/<date>|day log]])."

For each **annex entry** the user confirms: run the fold (ingest step 5, Compaction): the confirmed claims are integrated into the core by a guarded whole-body rewrite, the entries deleted from the section, `pending_review` cleared when the section is empty, and the fold logged. Retitling an annex heading is not a merge. If the user corrects it instead, route their statement through the correction flow. If they reject it, delete the entry and log the rejection. Explicit assent only. A nod at the digest as a whole promotes nothing. Disputes: apply whatever the user adjudicates (which claim wins, what demotes), via the correction flow where their ruling is new speech (write it to `sources/inbox/` with provenance `"the user, <date>"`).

**Interview verdicts** (items from 4b): confirm → the claim enters `wiki/life/self-model.md` cited inline as "(Alex, digest review, <date>)"; correct → route through the correction flow; reject → record the rejection on the page (the verdict is itself self-knowledge); "not that topic" → add the topic to the page's Off limits section and never re-ask it. The verdict completes all bookkeeping. An interview item never produces a follow-up reading surface.

**When the user finishes reviewing** (says so, or has acted on the items): write the marker `.state/review-markers/<YYYY-MM-DD>` (second review same day: `-2`, then `-3`, …). This review event is what connection-expiry and draft-lifecycle clocks count. Never write a marker for an unreviewed digest. If act-evidence shows a review that never got its marker (`verified_at` stamps or day-log review entries since the last marker), write it retroactively, dated to the acts and noted as reconstructed. Unattended runs surface the evidence in the digest instead of writing the marker. Review markers count digest review events only: in-session promotions and audits stamp `verified_at` but never write markers, and opportunistic in-session promotion is encouraged (amendment 2026-08-27).

## The 15-minute tripwire

If review runs past ~15 minutes (or the user says it's too long), the cap or the scoring is wrong. Tighten via an `amend` proposal. **Fix the digest, never the user's schedule.** Do not ask the user to review more often or longer. (The user choosing to review in smaller, more frequent sittings is a different thing, expected and healthy. The weekly schedule is an anchor, not a batch size, and each sitting writes a marker and advances the clocks.)
