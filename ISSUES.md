---
updated: 2026-09-26 9:58 pm
---
# ISSUES: friction log (open-issue index)

- One file per issue in `.state/issues/` (`<YYYY-MM-DD>-<slug>.md`), frontmatter `title` / `status: open|resolved|wontfix` / `opened` / `rule` (what it implicates) / `kind` / `resolved_by` (filled on close). Body freeform, no ceremony. A flag that takes effort won't get filed.
- Mark observation and read apart in the body: what was seen stands plain, while any causal story, close condition, or fix sketch carries a hypothesis marker ("My read:", "likely") until someone re-derives it from evidence. An unmarked diagnosis gets read downstream as a finding (added 2026-08-25).
- `kind` says what species of item it is, so the open list reads as three queues instead of one pile: `watch` (observing a change for evidence, closes on review cycles), `decision` (closure needs the user's ruling), `defect` (something broken or missing, fixable by agent work once approved). The Open section below is grouped by kind, decisions first.
- To file: create the file, regenerate both indexes. To close: flip `status`, fill `resolved_by`, regenerate.
- To record a recurrence: append to the end of the open issue's body, under a heading `## Recurrence <YYYY-MM-DD>`, one to three lines naming what was observed and where the evidence sits (day log, step report, entry). Never edit what is above it. Recurrence entries are how "N recurrences" close conditions mature (added 2026-09-04).
- Resolved files stay on disk as greppable history. Both indexes are derived, never hand-maintained: this one (**open issues only**) by `python3 .claude/scripts/regen-issues.py`, and `.state/issues/index.md` (every issue, open and resolved) by `python3 .claude/scripts/regen-index.py .state/issues`. Never transcribe rows by hand, and never copy them from the other index.
- The weekly digest surfaces open issues. The amend skill's cluster threshold triggers an amend proposal.
- **Friction metacognition** (adopted 2026-07-24 at the user's request): when an operation ends after a recurring serial chain of ~5+ trivial tool calls (hash bookkeeping, index regeneration, git choreography: mechanical steps, not judgment-laden ones), file a friction issue naming the pattern, the call count, and a proposed deterministic fix (a script runnable in one call, or subagent delegation). No batch optimization pass unless accumulated evidence argues for one.

**Program defects go upstream too.** If the friction is in the shipped program itself (a skill, rule, or tooling bug any deployment would hit, not your local amendments or your data), file it on the program repo's public issue tracker as well (upstream URL per meta/DEPLOYMENT.md; `gh issue create`, or draft the text for the user to post). Write it in the detail you'd want on the receiving end: what happened, what you expected, the file and line, your environment. It is a public post: no vault content, no personal data. The user approves before it goes up. Unattended runs leave the draft in the local issue file for the digest to surface.

## Open

*(none — the list above is regenerated from .state/issues/ in a live vault)*
