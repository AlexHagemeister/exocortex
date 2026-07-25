---
name: audit-exocortex
description: Interactive one-page-at-a-time review of wiki pages — a reading brief per page, the user corrects and promotes, then the next page. Use when the user says "let's audit" or "audit now", wants to review pages a recent ingest or session created, or when a digest review begins.
---

# Audit — one page at a time

The user's attention is the scarce input; spend it deliberately. One page per turn, never batched. Read the README of any folder you write to.

## Queue

Precedence: pages the user names > the open digest's items > pages created or changed since the last review touchpoint. State the queue size up front.

## Per page — the reading brief

Not a summary — the user reads the page. The brief bounds where their judgment is needed:

**N of M — [link] (status, last touched)** — one line on what the page is.

Then the items, numbered continuously, **sorted into two classes by who the decision belongs to — needs-you items first**:

**Needs-you** — a real tradeoff, a fact only the user holds, or anything touching promotion:

> **k. § [heading] › block [j]**, opens "[first ~3 words]"
> - **Look at:** "[verbatim quote]"
> - **Why:** why this needs the user's eyes (inferred vs. stated, single-source, contradicts something, gap only the user can fill).
> - **Rec:** the recommendation with its reason, plus the live alternative in one clause. Never a bare "your call" with equal-weight options.

**Recommend-and-run** — the fix is mechanical or the evidence points one way. Compressed, often one line each:

> **k. § [heading] › block [j]** — **Fix:** what will be done, already decided. **Basis:** one line of evidence, enough to veto from the brief alone.

Recommend-and-run items execute unless the user objects by item number — **silence is consent for this class only**, and only within the writes the skill already authorizes (draft edits, annex staging, link maintenance). Misfiled items cost one word ("2: needs-me"); when unsure which class, use needs-you.

**Never recommend-and-run, regardless of confidence:** promotion to `verified` (explicit assent every time — silence promoting a page is politeness-as-promotion), and any change to a claim's meaning on a verified core (correction flow, named to the user). <!-- constitution: principle 3, gate on status -->

- Heading = deepest containing heading, exact text; give the path if the heading text is duplicated on the page; "(top of page)" if none. Block = j-th paragraph/list/table/quote under it, counted from 1, plus enough of its opening words (~3) to spot it without counting. Anchor = exact quote, searchable — never a paraphrase.
- The list must be exhaustive of your doubts. Close with the bounding line ("everything else traces to filed sources") only when you have checked.
- A clean page gets one line saying so — never pad items.

End with the available moves (correct / add / promote / skip), not a question.

## Verdicts

The user replies by item number; one reply may carry several verdicts ("2: date's wrong — day before. Update, then promote.").

- **Correction or addition**: first check whether the claim also lives on other pages (grep). If it does, route the user's statement through the correction flow (sources/inbox/) so reconciliation reaches all of them. If the page under audit is its only home, apply the edit directly and add provenance `"the user, audit review, <date>"` to `sources:`.
- **Promotion**: explicit assent only, per page — set `status: verified`, `verified_at`, add `"user confirmed in audit, <date>"` to `sources:` (in digest context, digest's wording), log in the day log. <!-- constitution: principle 3, gate on status -->
- **Skip**: leave as-is, move on.

## Exit

Queue empty or the user stops. Day-log what was audited (pages, verdicts). Review markers are digest-only: an audit running inside a digest review follows digest's marker rule; ad-hoc audits never write markers — they stamp `verified_at`, which digest's marker-reconstruction logic already counts.
