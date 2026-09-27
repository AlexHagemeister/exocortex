---
updated: 2026-09-09 Wed, Sep 9 — 4:46 PM
---
# GLOSSARY: system vocabulary

This file owns **term meaning**. Procedures live in skills, invariants in CLAUDE.md, folder law in READMEs, and principles in CONSTITUTION.md. When a definition and a rule disagree, fix the glossary or amend the rule. Do not paper over with a second definition elsewhere.

Runtime surfaces say **you** and **the user**. Role nouns (Curator, Maintainer) appear only in CONSTITUTION.md and design docs.

## Zones and sharing

**program**: shippable system files per MANIFEST (rules, skills, substrate scripts, glossary, and supporting conventions), with no personal data.
_Avoid:_ the vault, the wiki, the repo (ambiguous, name which surface)
_Home:_ CONSTITUTION.md § Sharing and boundaries; public repo MANIFEST

**bundle**: a contained folder of related knowledge. Bundles nest freely (e.g. a project's bundle inside projects/). Unqualified, "the bundle" still means the outermost one: wiki/ alone, the OKF-conformant export surface (not the vault and not the program). (Sense widened per the user, 2026-07-20.)
_Avoid:_ the vault, the program, "my exocortex" (ambiguous)
_Home:_ CONSTITUTION.md § Sharing and boundaries (export sense); GLOSSARY only for the nested sense

**hub**: a project's central page with goals, current state, key decisions, and links to satellites. In a bundle, the hub is the folder's authored `index.md`, a page, not a derived listing.
_Avoid:_ index (indexes are derived and regenerated; hubs are authored)
_Home:_ wiki/projects/README.md

**satellite**: a page holding one substantial sub-topic of a project, linked from its hub.
_Avoid:_ section (a satellite is a page, not a heading), sub-page
_Home:_ wiki/projects/README.md

**vault**: the whole personal knowledge installation (sources, notes, wiki, attachments, and pipeline bookkeeping).
_Avoid:_ the wiki, the program, the bundle
_Home:_ CLAUDE.md § Zones

**wiki**: agent-maintained compiled knowledge layer in wiki/. Claims carry status and provenance.
_Avoid:_ the vault, notes, sources
_Home:_ wiki/README.md

**source**: frozen record of what was said, filed under sources/ after ingest moves it from inbox/.
_Avoid:_ truth claim, "the wiki says"
_Home:_ CLAUDE.md § Zones; sources/inbox/README.md (freeze-at-filing)

**attachment set**: several inbox items that are one source, a primary item plus the attachments it explicitly cites at capture. Each member files separately; together they feed the page that owns their subject (since 2026-09-06 that is the general rule for any sources sharing a subject, so the term names a filing shape, not an exception).
_Avoid:_ bundle (a folder of wiki knowledge), "related captures" (topical similarity is not membership)
_Home:_ `.claude/skills/ingest/` step 4

**note**: the user's own writing in notes/. The maintainer never edits note bodies.
_Avoid:_ source, wiki page
_Home:_ CLAUDE.md § Zones

**inbox**: pre-pipeline capture queue at sources/inbox/, freely editable until ingest files an item.
_Avoid:_ the wiki, "pending pages"
_Home:_ sources/inbox/README.md

**staging**: import holding area at staging/, invisible to the pipeline until items move into notes/ or sources/inbox/.
_Avoid:_ inbox (that's sources/inbox/, the capture queue)
_Home:_ staging/README.md

**drawings**: shared sketch space at drawings/ for the user's canvases and sketches plus agent-drawn diagrams, never swept or ingested by the pipeline. Location is the rule, not file type.
_Avoid:_ attachments (media embedded in pages), staging (import holding area)
_Home:_ drawings/README.md

**artifacts**: shared workspace at artifacts/ for work products the user and agent build together (decks, HTML pages, documents), any file type, never swept or ingested by the pipeline. Linkable without an authorship claim. Citing a claim from one requires a speaker, via sources/inbox/.
_Avoid:_ attachments (media embedded in pages), drawings (sketch space)
_Home:_ artifacts/README.md

**cookbook**: opt-in recipe library at meta/cookbook/. Ships with the program, inert until the user opts in; never swept, ingested, or cited as evidence.
_Avoid:_ tips, extras (name the folder), wiki (recipes are program content, not vault knowledge)
_Home:_ meta/cookbook/README.md

**recipe**: one cookbook entry: an optional connector, prompt, workflow, or automation, with setup detail sufficient for the agent to install it on the user's explicit yes.
_Avoid:_ skill (skills are the pipeline's own procedures; recipes are optional add-ons)
_Home:_ meta/cookbook/README.md

**feature staging**: trial tier for session directives: unverified imports and rules live in CLAUDE.local.md (deployment-local, never ships) until the user promotes them into the shipped surfaces via amend.
_Avoid:_ staging (the import holding area at staging/ is unrelated)
_Home:_ CLAUDE.local.md (header note)

## Pipeline skills

**ingest**: skill that files a source and compiles it into wiki pages.
_Avoid:_ import, add to the wiki, sync in
_Home:_ `.claude/skills/ingest/`

**process-inbox**: skill that drains sources/inbox/ and sweeps notes/ for deltas.
_Avoid:_ ingest (ingest handles one item; process-inbox orchestrates the queue and sweep)
_Home:_ `.claude/skills/process-inbox/`

**session-capture**: skill that preserves a conversation's durable knowledge as an inbox source.
_Avoid:_ ingest, remember this (name the skill)
_Home:_ `.claude/skills/session-capture/`

**query**: skill that answers from the vault with status-weighted citations.
_Avoid:_ search, chat about the vault
_Home:_ `.claude/skills/query/`

**lint**: skill that runs vault health checks and queues fixes.
_Avoid:_ spellcheck, cleanup, audit (that's the review-loop skill)
_Home:_ `.claude/skills/lint/`

**digest**: skill that compiles the user-facing review surface from pipeline output.
_Avoid:_ summary email, newsletter
_Home:_ `.claude/skills/digest/`

**audit-exocortex**: skill that runs the user's page review as an interactive loop. One page per turn, a reading brief with addressed items, explicit verdicts (correct / add / promote / skip). Suffixed to avoid collision with non-vault audit skills. Unqualified "audit" in vault surfaces means this one.
_Avoid:_ lint (health checks), digest (compiles the review surface; audit is the loop that walks it)
_Home:_ `.claude/skills/audit-exocortex/`

**review-system**: creator-side skill (source vault only, not yet shipped) that reviews the system itself (rules vs disk, skill-layer drift, automation, human-loop health) on a fixed rubric. It reports to .state/reviews/.
_Avoid:_ lint (page health), audit (content review loop)
_Home:_ `.claude/skills/review-system/`

**amend**: skill that changes rules, skills, or wiki folder structure with user approval.
_Avoid:_ fix the rules, edit CLAUDE.md (name the skill)
_Home:_ `.claude/skills/amend/`

**publish-program**: creator-side skill (source vault only, not shipped) that syncs vault program files to the public repo after user-reviewed diff.
_Avoid:_ push, backup, mirror
_Home:_ `.claude/skills/publish-program/`

**vault-snapshot**: skill that commits and pushes the vault git history for recovery and remote capture.
_Avoid:_ backup (ambiguous), publish (that's publish-program)
_Home:_ `.claude/skills/vault-snapshot/`

**update-exocortex**: skill that pulls the latest program release into this vault, reconciling local amendments.
_Avoid:_ upgrade, pull updates (name the skill)
_Home:_ `.claude/skills/update-exocortex/`

## Epistemics

**draft**: wiki status for hypothesis-grade pages. Usable, but say so when it matters.
_Avoid:_ unverified (use status labels), guess (use observation/inference sections)
_Home:_ CLAUDE.md § Reading wiki pages: status weighting

**verified**: wiki status for human-promoted ground truth. Scarce by design.
_Avoid:_ true, confirmed (unless quoting a source), approved (politeness ≠ assent)
_Home:_ CLAUDE.md § Reading wiki pages: status weighting

**review receipt**: the sentence at the top of a verified page's body recording who promoted it, in which review, on what date, linking the day log that records the promotion.
_Avoid:_ sources: (retired 2026-08-17), provenance (provenance is a claim's origin; a review receipt records who promoted the page)

**compaction**: the guarded, unattended re-expression of a verified page for cohesion without changing any claim (ingest step 5). Status untouched. The **fold** is compaction run at the user's confirmation of annex entries, which integrates them into the core.
_Avoid:_ consolidation (the neuroscience analogy, and the ordinary word; the vault operation is compaction), merge (a fold integrates; retitling a heading is not a merge)
_Home:_ `.claude/skills/ingest/SKILL.md` step 5

**compaction receipt**: the sentence beside a page's review receipt recording a compaction: date, what the guards checked, and the last curator review it rests on.
_Home:_ `.claude/skills/ingest/SKILL.md` step 5

**stale**: wiki status for a page past its review half-life. Re-verify before relying on it.
_Avoid:_ old, outdated (use status)
_Home:_ CLAUDE.md § Reading wiki pages: status weighting; `.claude/skills/lint/` check 2

**disputed**: wiki status for a page with contradictory evidence. Do not build on it.
_Avoid:_ wrong, deprecated
_Home:_ CLAUDE.md § Reading wiki pages: status weighting

**pending_review**: frontmatter flag for a page with a verified core plus one draft-grade "Unreviewed additions" section of dated entries awaiting the fold.
_Avoid:_ draft (the core may still be verified)
_Home:_ CLAUDE.md § Reading wiki pages: status weighting

**scope**: a page's boundary contract, carried in its `scope:` frontmatter field: what belongs, what is excluded, and where each exclusion lives instead. Serves filing (where a new fact goes), retrieval (an agent can skip and reroute without loading the body), and audit (the fixed standard that body drift is measured against). Mandatory on every wiki page and every skill (for skills it is maintainer-facing: a calibration and split signal, not router input). Distinct from `description`, the one-line retrieval attractor. Sources and notes never carry it.
_Avoid:_ packing exclusions into `description`
_Home:_ `.claude/skills/ingest/` step 4 (field law); amend skill (skill frontmatter law); CLAUDE.md § Page scoping (tests)

**provenance**: traceable origin of a claim (source path, URL, or the user's dated words).
_Avoid:_ citation (provenance is origin; citation is how you point at it)
_Home:_ CONSTITUTION.md principle 1

**modality**: how much evidential weight a stream grants its contents (declared in that stream's README). A filed item may carry its own `modality:` frontmatter line when the stream default would mislabel it, and the item's line wins.
_Avoid:_ tone, format
_Home:_ stream README (e.g. sources/meetings/README.md); `.claude/skills/ingest/` step 2 (per-item override)

**freeze**: the moment ingest files a source. Path and content become immutable records of what was said.
_Avoid:_ lock, archive
_Home:_ sources/inbox/README.md; `.claude/skills/ingest/`

**load-bearing claim**: a wiki claim of one of CLAIM-SPEC's types (v1: quote, fluent, supersession), and therefore machine-checkable. Everything else is free prose with no parse expectation. The definition is operational: the types list, not judgment, decides membership.
_Avoid:_ important claim, key fact (importance is not the test; type is)
_Home:_ meta/CLAIM-SPEC.md (deployment-local trial 2026-09-01, ships only if it graduates)

**fluent**: a current-state claim that can stop being true, expected to be anchored to a literal date it was true as of (an undated fluent is still a fluent, warn-grade). Contrast with an event, whose happening never becomes false.
_Avoid:_ fact (unanchored), status (that word is taken by the page lattice)
_Home:_ meta/CLAIM-SPEC.md (deployment-local trial 2026-09-01, ships only if it graduates)

- **laundered inference**: a guess written with the typography of a fact, so it propagates as if verified. The constitution's named deadliest anti-pattern (CONSTITUTION.md § Anti-patterns). The instances the vault has recorded live on wiki/concepts/laundered-inference.md. Status fields and observation/inference separation exist to prevent it. (Entry added 2026-09-09.)

## Operations

**stream**: a permanent sources/ subfolder with its own modality README (articles/, sessions/, meetings/, life/, …).
_Avoid:_ folder, category (streams carry evidential semantics, not just taxonomy)
_Home:_ sources/inbox/README.md; `.claude/skills/ingest/` step 2

**issue**: friction-log entry in .state/issues/. ISSUES.md lists open issues only.
_Avoid:_ ticket, bug (unless quoting an external tracker)
_Home:_ ISSUES.md; `.state/README.md`

**kind**: an issue's species, frontmatter `kind: watch|decision|defect`, so the open list reads as three queues (watches accruing evidence, decisions on the user's desk, defects fixable by agent work).
_Avoid:_ type (already means a wiki page's frontmatter `type:`), category
_Home:_ ISSUES.md conventions

**day log**: dated pipeline history at wiki/log/<YYYY-MM-DD>.md.
_Avoid:_ journal, changelog (program changes use public CHANGELOG.md)
_Home:_ wiki/log/

**claim-neutral edit**: a user-directed wiki edit that changes no claim (style, structure, formatting, link fixes). Applied directly on in-chat approval and day-logged. No knowledge enters, so no pipeline is bypassed.
_Avoid:_ correction (that flow is for wrong claims), override (this is rule-following, not an exception)
_Home:_ CLAUDE.md, single-pipeline rule

**wikilink**: the vault's link form since 2026-08-17: `[[name]]`, resolved by file basename across the whole vault, or path-qualified `[[folder/name]]` when the name is not unique (index, README, collisions). Alias with `|`. Obsidian sees, follows, and repairs these; a page's name is its identity.
_Avoid:_ markdown link, relative link, path link (the pre-2026-08-17 form; still correct for links into dot-folders, which Obsidian cannot wikilink)
_Home:_ `.claude/skills/ingest/` link rule; lint check 1 enforces

**chronicle**: the agent-compiled record of the user's days in `wiki/chronicle/`: one page per day (04:00-to-04:00), five fixed sections (reported, observed, inferred, coverage, the agent's read), weekly roll-ups after each Sunday. Distinct from the day log, which records what the pipeline did. Never a citation target: wiki claims cite the underlying sources, not chronicle entries. Opt-in via the cookbook recipe.
_Avoid:_ diary, journal (those imply the user wrote it), day log (that is the pipeline's book)
_Home:_ `wiki/chronicle/README.md` folder law; `.claude/skills/chronicle/` procedure; `meta/cookbook/chronicle.md` adoption

**self-interview**: the digest's 1–3 question-shaped items about the user per cycle. The kinds are blind-spot (receipted hypothesis awaiting verdict), disclosure (the system doesn't know, asks), and negative-space (neither knows). The user's verdict completes all bookkeeping.
_Avoid:_ survey, personality quiz, blind-spot report
_Home:_ `.claude/skills/digest/` compile 4b + Review interview-verdicts

**self-model page**: the joint self-knowledge ledger at wiki/life/self-model.md. It holds trait- and pattern-level claims about the user, each claim's provenance naming whose knowledge it is (self-report / confirmed agent inference / a named person's feedback). Only explicit user verdicts admit content.
_Avoid:_ user-model, profile (the self modeled is the user; the modelers are both parties)
_Home:_ wiki/life/README.md (page law)

**deployment profile**: environment bindings in meta/DEPLOYMENT.md. Skills reference it and never hardcode paths.
_Avoid:_ config, settings (too generic)
_Home:_ meta/DEPLOYMENT.md

**MANIFEST**: allowlist in the public program repo naming vault paths that ship. Adding a line is a publishing decision.
_Avoid:_ package.json, file list
_Home:_ public repo MANIFEST; `.claude/skills/publish-program/`

## Flagged ambiguities

- **repo**: three distinct repos are in play (the private vault, the public program, and optionally remote capture branches). Name which one.
- **maintainer**: design-time role noun only. Runtime surfaces say "you" (the agent) and "the user."
