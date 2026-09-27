---
type: Meta
title: Log — dated pipeline history
description: One file per day recording what the pipeline did; skim, don't read whole.
scope: "Day-log files only, one per date, written by skills as they act. What each skill logs lives in that skill, and how any entry is written lives here. Not claim-bearing pages: no sources, no status weighting, never a citation target for wiki claims (cite the underlying sources instead)."
status: draft
---

One file per day (`<YYYY-MM-DD>.md`), written by skills as they act. History, not knowledge: nothing here carries status or serves as provenance for a wiki claim.

Entries are appended in the order they are written, through `.claude/scripts/day-log.sh "<entry>"` (or a heredoc on stdin for long entries). The script finds the day's file itself (a day runs 04:00 to 04:00 local, as in the chronicle, so a write before 04:00 lands in the previous day's file) and adds to the end in one write, so concurrent lock-exempt writers never erase each other. Never rewrite a day log from an earlier read. Corrections are new entries, and small in-place fixes to an existing entry (a link, a typo) use Edit (amendment 2026-09-26, after a whole-file rewrite erased a run's entries on 2026-09-12).

Links here are frozen with the entry: they name where a page lived on the day the line was written, and a later page move does not rewrite them. A dead link in a day log is dated history, not rot, so migrations skip this folder and lint's dangling-link listing does not count it (amendment 2026-09-06, closing the page-moves question).
