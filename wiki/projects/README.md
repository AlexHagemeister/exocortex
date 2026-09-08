---
type: Meta
title: "Projects: ongoing work"
description: One hub page per project plus its satellite pages; the memory brain's work half.
status: draft
---

One hub page per project (goals, current state, key decisions, links to satellites), with satellite pages for substantial sub-topics. Fed mostly by session captures and the notes sweep. Project state changes fast, so keep claims dated and cited inline; compaction (ingest step 5) restructures a page but never strips a claim's date or citation, and a confirmed later state claim supersedes an earlier one with both dates kept.

**Grow satellites, not sections.** A substantial new sub-topic becomes a satellite page linked from the hub — never a new hub section; edits to existing hub concerns stay on the hub. A flat hub gains its first satellite by becoming a bundle: move `<slug>.md` → `<slug>/index.md`, fix any path-qualified links on the moved page, regenerate the touched indexes and path-qualify any inbound links that named the old path (bare wikilinks keep resolving), log the move in the day log. The move is mechanical and pre-approved by this rule (amendment, 2026-07-30): nothing is reworded. A bundle's `index.md` is the authored hub page, never a derived listing — do not regenerate it; the folder needs no separate index. Each satellite link on the hub carries a one- or two-line summary of what that page holds — the hub keeps the whole project legible without opening satellites; a hub reduced to a bare link list has lost its job (amendment, 2026-07-31).

**Uniform satellite naming is a convention justified per-use, not a mandate.** The CS course bundles (cs160, cs170: index/logistics/next-actions/objectives) share a naming shape because it was useful there. The user's ruling when asked to generalize it (2026-08-27 digest review, verbatim): "uhm. yeah uniform to the extent that its actually useful, but not to the extent that it imposes some homogenous structure to the messiness of real knowledge... I humbly admit the limitations in my ability to judge and design this aspect of it with confidence." Reuse a satellite shape where it fits; never force a project's real structure to match a prior bundle's for consistency's own sake.
