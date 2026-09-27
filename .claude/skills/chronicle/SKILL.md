---
name: chronicle
scope: "Compiling daily and weekly chronicle entries in wiki/chronicle/ from vault-internal witnesses and the deployment's registered surfaces. Does not own capture (the pipeline's), correction reconciliation (ingest's), or promotion (nothing here promotes); answering questions from chronicle pages is query's job. Future witness kinds join as collector briefs, not a redesign."
description: Compile the chronicle — the agent-written record of the user's day. Run as a step of the deployment's scheduled maintenance chain (daily, retrospective for yesterday; the weekly roll-up on Mondays), or when the user asks to chronicle or backfill a day.
---

# Chronicle — compile the record of the user's day

You are writing `wiki/chronicle/` pages: the account of what the **user** did, distinct in register from the maintainer day log (`wiki/log/`), which records what the pipeline did. Read `wiki/chronicle/README.md` before writing — the folder law (five sections, naming, 04:00 day boundary, append-only, frontmatter template) lives there and is not restated here.

## Daily procedure (retrospective: compile yesterday)

**Step 0 — intake gate (state, not clock).** Scheduled runs pile up while the machine sleeps, so never assume process-inbox ran first. Yesterday's intake is done when no item in `sources/inbox/` predates today's 04:00 boundary (README and quarantine/ don't count). If stale items remain and no drain is in flight, invoke the `process-inbox` skill now and continue when it completes. If a drain appears mid-run (maintainer lock or fresh in-progress bookkeeping in `.state/`), wait and re-check. If intake still can't complete, proceed anyway and say so in the entry's Coverage section — a gapped entry beats a missing one.

**Step 0b — idempotency.** If the target day's entry already exists in `wiki/chronicle/`, a scheduled run stops and reports that; a second compile never overwrites or duplicates an entry. Enrichment of an existing entry is a different operation (below), never a recompile.

**Step 1 — orchestrate collection. Do not walk the surfaces yourself.** First compute the capture window as explicit local timestamps — `<target-day>T04:00` to `<day-after>T04:00` — and state it verbatim in every collector brief. Delegate each witness group to a subagent and write from their reports. **Launch every collector in the foreground** (`run_in_background: false`), all in one message so they run in parallel, and do not end your turn until the call returns. A collector launched in the background reports to whichever session is live when it finishes, and when this skill runs as a subagent that is the orchestrator, not you (three misrouted runs, Aug 17 to Sep 2, 2026). Every collector brief has two halves:

1. *Collect* from the assigned surfaces, **bounded to the stated window**. Use the tool's own time filters where they exist (calendar ranges, email date queries, git `--since/--until`); where a surface can't filter by time, fetch then discard out-of-window items, saying so. Every reported item carries its timestamp (or explicit "undated" with the best available anchor, e.g. file date); an item whose time can't be established is reported as such, never silently placed inside the window. Collectors report timestamps exactly as the source rendered them, with the timezone named, and never convert. Conversion to the compiler's reference zone happens once, at compile time, by the compiler. Credentials found in evidence (tokens, keys, passwords) are reported as existing and never reproduced, by collectors or in the entry.
2. *Disambiguate before reporting*: full read access to the vault — wiki, sources, top-of-mind, project hubs — with instruction to follow breadcrumbs until the data makes sense. A calendar block titled with a bare name should come back naming the project and context, cited. Never a raw dump, never a naive relay.

You verify on receipt: reports must name the window they searched, and any evidence dated outside it gets dropped or explicitly marked as boundary context before it enters the entry. A capture's filename and filing date are not its timestamp: the window applies to when something was said or done.

Collectors return distilled, cited evidence plus ambiguity notes ("could not determine what the 90-minute gap after 1pm was"). Triangulation and judgment stay with you, the orchestrator — the only context that sees all reports. A collector returning "nothing observed" is itself Coverage data. A collector whose tool fails retries once, then reports the surface as unreached, never as empty. A partial fallback (a second path that covers less) reports what it could not see. Coverage keeps the two apart: "returned nothing" and "unreached" are different lines.

The roster has two halves:

**Vault-internal witnesses** (universal, fixed here — one or two collectors as volume warrants):

| Witness | What to capture |
|---|---|
| Maintainer day log | `wiki/log/<day>.md` — what the pipeline did, what the user directed |
| Filed sources | sources/ files dated in the window — captures, clips, life-data |
| Git | the vault repo's commits in the window; activity shape, not diffs |
| Notes | the user's daily note and `notes/` changes (read-only) |
| Intentions | `artifacts/top-of-mind.md` as it stood; next-actions pages of projects the day touched |

**External surfaces** (deployment-specific): read the registry at `meta/chronicle-surfaces.md` and spawn **one collector per `active` surface**, handing it that surface's capture brief verbatim (batching two trivial surfaces into one collector is fine; skipping a registered surface is not). Surface-specific boundaries in the registry (e.g. Granola report-only) are law for the collector.

Registering a new surface: when the user asks to add one (or accepts an offer after connecting a new tool), append the entry to the registry per its format — a user-approved edit, one line in the day log. Never activate a surface without the user's explicit yes.

**Step 2 — write the entry** per the folder law's five sections and frontmatter. Rules that bind the writing:

- Evidence lines cite their witness. Times come from records only — never invent a timestamp.
- Every inference names the evidence it extends. An inference resting on a prior entry's *inference* (not its evidence) says so inline. This is the circularity guard; it is what keeps unverified-inference chains visible as entries compound.
- Subject attribution is itself an inference. A witness attests that something was said or recorded, never by itself whose fact it is. When a record holds a conversation whose speakers it does not identify, never default a first-person claim to the user: write the subject as unresolved, name whose it might be, and flag it in Coverage. A material fact whose sole witness is a report-only surface is escalated as an issue or digest line, never a capture.
- **The agent's read is yours.** Synthesis, judgment, alignment with stated intentions, patterns worth naming. It is explicitly attributed agent judgment, so write it freely and plainly — the user corrects it in conversation, and those corrections are themselves data that arrive through the normal corrections path.
- Style: plain prose the user can skim, under the deployment's style bindings (`meta/DEPLOYMENT.md` Style banlist row).

**Step 3 — close out.** Regenerate `wiki/chronicle/index.md` (oldest first, one line per entry from its `description`). One line in the maintainer day log, via `.claude/scripts/day-log.sh`. Nothing else: no wiki-page updates, no captures, with one exception (the user, 2026-09-09): a collector on an email surface that finds a fact new to the vault and worth keeping writes one inbox capture shaped "the user got an email about X, noteworthy and not yet in the vault," attributed as an observed email, never as the user's words. Meeting transcripts (Granola) are never read by this skill; they enter the vault only when the user brings one in with context. Anything that looks like it should enter the wiki goes through the normal pipeline, not this skill.

## Weekly procedure (Mondays, after the daily has covered Sunday)

Gate: all seven dailies Mon–Sun exist; compile any missing one first via the daily procedure. Read the seven entries, drilling into their cited evidence only where they are ambiguous. Write `<closing-Sunday>-week.md`: the same five sections at week granularity — what the week's record shows, the inferred arc, coverage (thin days), and the agent's read of the week. The cross-level circularity guard applies: building on a daily's inference rather than its evidence sections is marked as such.

## Backfill

On user request the daily procedure runs for any past date. Set `compiled:` honestly and expect Coverage to be thinner — transcript search and git survive time; ephemeral surfaces may not.

## Enrichment (entries are living pages)

When new evidence arrives for an already-chronicled day — a newly activated surface, a late-arriving source, the user's own addition — add it to that day's entry rather than leaving the entry stale. Collect for that day's window with the same discipline (window stated, items timestamped), then write a dated addition ("Added <date>:") into the affected sections and update Coverage (and the description, if the day's shape changed). Small factual fixes may edit in place. Never recompile the whole entry, and never let enrichment rewrite the agent's original read silently — a changed judgment is a dated addition to it.
