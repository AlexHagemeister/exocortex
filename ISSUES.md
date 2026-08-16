---
updated: 2026-08-16
---
# ISSUES — friction log (open-issue index)

- One file per issue in `.state/issues/` (`<YYYY-MM-DD>-<slug>.md`), frontmatter `title` / `status: open|resolved|wontfix` / `opened` / `rule` (what it implicates) / `resolved_by` (filled on close). Body freeform, no ceremony. A flag that takes effort won't get filed.
- To file: create the file, regenerate both indexes. To close: flip `status`, fill `resolved_by`, regenerate.
- Resolved files stay on disk as greppable history. Both indexes are derived, never hand-maintained: this one (**open issues only**) by `python3 .claude/scripts/regen-issues.py`, and `.state/issues/index.md` (every issue, open and resolved) by `python3 .claude/scripts/regen-index.py .state/issues`. Never transcribe rows by hand, and never copy them from the other index.
- The weekly digest surfaces open issues. The amend skill's cluster threshold triggers an amend proposal.

**Program defects go upstream too.** If the friction is in the shipped program itself (a skill, rule, or tooling bug any deployment would hit, not your local amendments or your data), file it on the program repo's public issue tracker as well (upstream URL per meta/DEPLOYMENT.md; `gh issue create`, or draft the text for the user to post). Write it in the detail you'd want on the receiving end: what happened, what you expected, the file and line, your environment. It is a public post: no vault content, no personal data. The user approves before it goes up. Unattended runs leave the draft in the local issue file for the digest to surface.

## Open

*(none — the list above is regenerated from .state/issues/ in a live vault)*
