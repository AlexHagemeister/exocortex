# Vault Doctrine v0.3

> **SUPERSEDED — construction artifact (banner added 2026-07-16, user-approved).** This document guided the vault's construction and is preserved as historical reference. Its operational rules are superseded by the live surfaces — CLAUDE.md, .claude/skills/, and folder READMEs — which have since been amended beyond what this document describes (link conventions, lifecycle keying, staged sections, concurrency, and more). Do not compile, quote, or restore rules from this document. Principles live in CONSTITUTION.md at the vault root; the rules live where they bind.

Personal AI knowledge system: OKF core + local doctrine. This document is the schema-of-schemas — it governs the vault's CLAUDE.md, which governs the agents. Audience: the Curator (the human running the system) and any agent maintaining or consuming the vault.

**Roles.** *Curator* — the human: curates inputs, promotes drafts, adjudicates disputes, owns notes/, holds final say on schema. Curation is the one job that cannot be delegated. *Maintainer* — the agent role: the skill set (§8) any capable agent instance can invoke, governed by CLAUDE.md. Roles are hats, not identities — many instances may wear the maintainer hat; only one human wears the Curator's. **Terminology rule:** role names are design-time vocabulary for this document and the constitution only. Runtime surfaces (CLAUDE.md, skills, READMEs) address the reading agent as "you" and the human as "the user" — rules agents follow mid-task must be legible with zero glossary. "Consumer" is reserved for its OKF sense: external tooling reading a bundle.

**Portability.** This doctrine, the OKF spec, and the skill files constitute the entire program — code as markdown. Everything else in a vault is Curator data. Anyone can replicate the system by adopting the program against their own vault.

**Lineage:** Karpathy's LLM-wiki pattern (Apr 2026) → Google Open Knowledge Format v0.1 (Jun 2026) → this doctrine. Where OKF is silent (workflow, guardrails, topology), this document decides. Where this document is silent, OKF SPEC.md decides.

---

## 1. Purpose

One vault serving three roles simultaneously:

1. **Research brain** — compiled knowledge about the world (external sources)
2. **Memory brain** — compiled knowledge about the Curator's work and life (sessions, life data)
3. **Agent substrate** — the context layer any agent instance reads to act on the Curator's behalf

Design consequence: the wiki is optimized for *agent consumption first*, human browsing second. The files are the interface; the vault app is only the viewer.

## 2. Vault Topology & Ownership

```
vault/                      (iCloud-synced Obsidian vault)
├── CLAUDE.md               # operating schema — co-evolved, Curator has final say
├── .claude/skills/         # PROGRAM ZONE: the maintainer skill set. Flat structure
│                           #   (one folder per skill, no grouping subfolders). At
│                           #   vault root so Claude Code sessions in the vault
│                           #   auto-register them; outside wiki/ so OKF consumers
│                           #   don't parse SKILL.md files as concepts.
├── sources/                # IMMUTABLE inputs. Agents never edit. Ever.
│   ├── inbox/              # transient queue: clipper drops, session notes, captures
│   │   └── quarantine/     #   rejected captures (validation failures) await Curator
│   ├── articles/           # external sources, filed here by ingest (permanent home)
│   │   ├── index.md        #   pipeline-maintained listing
│   │   └── README.md       #   stream semantics incl. evidential modality (§4)
│   ├── sessions/           # session captures (index.md + README.md, as above)
│   └── life/               # exports: health, calendar (index.md + README.md)
├── wiki/                   # AGENT-OWNED. ═══ THE OKF BUNDLE (boundary) ═══
│   ├── index.md            # root index (progressive disclosure)
│   ├── log.md              # chronological change history
│   ├── connections/        # Connection pages (§2.4) + index.md + README.md
│   ├── <topic>/            # small, stable top-level folders — see §3
│   │   ├── index.md        #   derived listing (regenerated freely)
│   │   ├── README.md       #   authored folder semantics (type: Meta)
│   │   └── <concept>.md
│   └── ...
├── notes/                  # CURATOR-OWNED, LIVE. Thought-dump zone: fleeting
│                           #   notes, ideas, drafts, daily notes. Agents read,
│                           #   link, and ingest from it — never write to it.
└── .state/                 # PIPELINE-OWNED bookkeeping: sweep cursors, digest
                            #   review markers. Excluded from ingestion, sync
                            #   conflict checks aside, and from the bundle.
```

**Bundle boundary:** the OKF bundle is wiki/ alone. sources/ and notes/ are external referenced resources — wiki provenance cites paths into them, which is spec-legal (consumers MUST tolerate broken links) but means an exported bundle carries dangling source references by design. When sharing: ship the program (constitution + CLAUDE.md + .claude/skills/), optionally the bundle, optionally sources/ alongside it; notes/ and .state/ never ship. Note the boundary is file-level, not knowledge-level — wiki pages built from notes contain distilled note content; sharing a bundle publicly is a redaction pass, not a folder exclusion.

### 2.1 Ownership matrix (the core contract)

| Zone       | Curator writes | Agent writes | Agent reads |
|------------|----------------|--------------|-------------|
| CLAUDE.md  | yes (final say) | proposes edits | yes |
| sources/   | yes (adds only) | adds to inbox; files inbox items during ingest | yes |
| wiki/      | **never** | yes (via pipeline only) | yes |
| notes/     | yes (freely, forever) | **never** | yes (reads, links, ingests from) |
| .claude/skills/ | yes (final say) | proposes edits via `amend` | yes |
| .state/    | no | pipeline only | pipeline only |

**Three input semantics:** sources/ is frozen speech (others', or the past Curator via session captures) — filed once, cited forever. notes/ is live speech (the Curator's ongoing thought) — perpetually editable, never frozen. Corrections-as-statements (§2.3) bridge them: Curator speech *about* frozen sources enters as new frozen sources.

### 2.2 Source immutability

Ingest performs a one-time filing move (inbox/ → permanent stream folder) *before* writing any wiki page that cites the item; provenance always references the final path. **The freeze happens at filing:** inbox items are pre-pipeline — freely editable or deletable. Once filed, path and content are frozen. A source is a record of what was said, not a truth claim; it is never edited to "fix" it.

### 2.3 Correcting sources (low-friction by design)

The Curator's action is always a statement, never a re-fetch:
- Broken capture → re-clip.
- Source factually wrong → no source action; the *wiki* layer marks the claim disputed or outweighs it with better sources.
- Agent-generated source (e.g., a session summary) misstated something → the Curator says so in any agent surface; the correction enters inbox as a new source (provenance: "Curator, <date>") and ingestion reconciles dependents. Superseded originals remain as historical record; lint may flag them.

### 2.4 notes/ ↔ wiki: watched stream and connections

- **Watched stream:** process-inbox also diffs notes/ against its previous pass (cursor in .state/) and ingests new or changed content. Wiki pages cite a note *plus the read timestamp*; when a cited note changes later, lint flags the citation stale and the delta re-ingests. Mutability for the Curator, pinned provenance for the wiki.
- **Deletion is withdrawal:** lint detects citations to deleted notes; wiki claims resting *solely* on a deleted note demote to `disputed` and queue for the Curator.
- **The agent never writes links into notes/** — it doesn't need to: backlinks and graph view surface any wiki→note link on the note automatically. Routine associations (a note mentions a known entity): ingest links the relevant concept pages to the note. Substantive insights (the gold): a first-class `type: Connection` page in wiki/connections/ stating the relationship, linking both endpoints, `status: draft`. A connection is a claim; page-hood gives it the full lifecycle (promote, dispute, expire) an appended link never could.
- **Connection drafts expire:** unpromoted after ~3 *Curator-reviewed* digests → presumed noise; lint deletes the page and logs it (recoverable from the git mirror). The clock ticks on review events, never wall-clock: human-gated lifecycles count human acts.
- **Discovery is push:** the digest lists new Connection pages; insights reach the Curator unprompted.

### 2.5 Correction doctrine (wiki layer)

If a wiki page is wrong, the Curator does not hand-edit it. Root-cause the upstream cause — bad source → correct via §2.3 and re-ingest; bad inference → improve schema or skill — and let the agent reconcile. Hand-edits fork the agent's model of its own work.

## 3. Folder & Tag Doctrine

- **Folders are load-bearing.** A concept's file path IS its identity (OKF); moves break every inbound link. Top-level wiki/ folders: few, stable, human-chosen. Folder refactors are schema migrations — agent proposes, Curator approves, agent executes with a link-rewrite pass, logged in log.md.
- **Tags are free.** Agents create and apply tags without approval; emergent themes and experiments live in tags, not folders. Any tag applied consistently gets its own concept page defining it (tags are first-class concepts per OKF).

## 4. File Format (OKF-conformant superset)

All wiki/ pages use **standard markdown links** (not wikilinks) and OKF frontmatter plus local guardrail fields. notes/ may use wikilinks freely — it is outside the bundle.

```yaml
---
type: Concept            # REQUIRED (only OKF-required field). Local taxonomy, evolvable.
title: ...
description: ...
tags: [ ... ]
timestamp: 2026-07-15T10:00:00Z   # last substantive update
# --- local guardrail fields (conformant extensions) ---
status: draft            # draft | verified | stale | disputed
verified_at:             # set on promotion to verified
depends_on: []           # concept paths this page's claims rest on
sources: []              # provenance: paths into sources/ or notes/ (+ read timestamp), URLs, or "Curator, <date>"
---
```

Body and file conventions:
- **Separate observation from inference.** "What the source says" and "what we conclude" live under distinct headings. Never write a guess in the same breath as a fact.
- **No claim without provenance.** Every substantive claim traces to a `sources:` entry or is explicitly marked as agent inference.
- **Dangling links are legal and useful.** Red links are the backlog of known-missing knowledge.
- **index.md:** no frontmatter (per OKF); sections of linked entries with one-line descriptions. Fully derived — regenerated freely, never hand-maintained, carries no decisions.
- **README.md** per wiki/ folder and per sources/ stream: authored semantics — what the folder is for, what belongs in it, local conventions. Frontmatter `type: Meta`: a first-class, linkable, statused concept; agent proposes, Curator approves, like schema. Changes only when the folder's *meaning* changes. The index/readme split is derivation status — regenerable listing vs. durable meaning; never mix them.
- **Stream modality:** each sources/ stream README declares its *evidential semantics* — what kind of claim the stream can support. Calendar entries evidence intention, never occurrence ("did X" requires corroboration from a second stream). Session summaries are agent paraphrase of what was said, not what is true. Measurements carry error, not ground truth. Ingest must respect declared modality when writing claims.
- notes/ gets no agent-maintained index or readme; any map of the Curator's notes lives as a derived wiki page.

## 5. Epistemic Guardrails

**The status lifecycle (the load-bearing guardrail):**

```
[agent writes] → draft → [promotion, §8] → verified
                            ↓ (staleness decay)   ↓ (contradiction found)
                          stale                disputed
```

- Agent writes land as `draft` — sole exception: verbatim Curator quotes, born `verified` (§8 trust inheritance).
- Every agent reading wiki pages weights by status: `verified` = ground truth; `draft` = hypothesis; `stale` = re-verify before relying on; `disputed` = do not build on.
- Promotion to `verified` is a Curator act (§8: digest triage, flow-of-use confirmation) or a verification pass with cited evidence. **Gate on status, not on merge** — writes are never blocked; trust is graduated.
- Staleness decay: lint demotes `verified` → `stale` past a per-type half-life (fast for infrastructure/life facts, slow for conceptual pages).
- Contradictions: lint flags incompatible claim pairs; both go `disputed` and queue for the Curator. Detectable without ground truth — treat as gold.
- Retraction: when a page is invalidated, walk inbound links + `depends_on` dependents and re-examine each (cheap ATMS). Log retractions in log.md.

**Deferred to v2:** executable-claim tests (mechanical verification at write time); full dependency-graph truth maintenance.

## 6. Write Path (single-pipeline rule)

> No agent writes to wiki/ directly. All knowledge enters through sources/inbox/, the notes/ sweep, or maintainer skills.

Automation depth varies per stream; the pipeline is invariant:
- **External clips:** manual capture (clipper → inbox). Curation is the human quality gate. Clip deliberately.
- **Notes:** zero-friction by design — dump thoughts anywhere in notes/; the sweep ingests deltas (§2.4).
- **Sessions:** not hooks — a `session-capture` skill, invoked on demand from any surface, summarizes a session's durable knowledge (quoting pivotal exchanges verbatim, per §4 modality) into inbox/. The Curator decides which sessions are worth capturing.
- **Life data:** scheduled exports into sources/life/, ingested by pipeline under each stream's declared modality.
- **Query write-back:** good synthesized answers file into wiki/ as drafts, so explorations compound.

## 7. Agent Topology

One maintainer **role**, not one maintainer agent: a skill set any capable agent instance can invoke, governed by CLAUDE.md. All other agents are read-only toward wiki/ and contribute via inbox/ drops. Current deployment: Claude Code (interactive + scheduled) wears the maintainer hat; Desktop Commander chat and task agents are read-only; mobile capture via clipper; mobile query via remote session (untested, §12).

### 7.1 Instruction conflicts (Curator vs. doctrine)

The Curator is not expected to know the doctrine; the agent is. When an instruction conflicts with a rule:

1. **Translate first.** Most conflicts are phrasing, not intent — "fix that page" is §2.3, "remember this" is an inbox drop, "link my note to X" is a wiki-side link. Route the intent through the conforming path and disclose the mechanism in one line. Casual use should teach the doctrine, never require it.
2. **Surface true conflicts.** If the intent itself violates a rule, name the rule and its reason in one sentence; offer the conforming alternative and the override. No lecture, no refusal.
3. **Overrides are sovereign, explicit, and logged.** The Curator may override any rule; the agent complies and records a doctrine-exception entry in log.md (what, why). Silent exceptions are forbidden in both directions — no quiet compliance, no quiet reinterpretation.
4. **Repeated overrides indict the rule, not the Curator.** The same rule overridden ~3 times → the maintainer proposes a schema amendment. Exceptions are bugs; amendments are fixes; Curator–doctrine friction is data.

## 8. Workflows (the skill set)

| Skill | Trigger | Does |
|---|---|---|
| `ingest` | on command / by process-inbox | Validate (reject empty/truncated/junk → inbox/quarantine/; content-hash dedup) → file to stream folder → read → discuss takeaways if interactive → write source summary → update 5–15 related wiki pages (draft, provenance, links) → refresh indexes → append log.md |
| `process-inbox` | scheduled (daily-ish) | Sweep inbox (excluding quarantine/ and sync-conflict files, §9) → ingest per item; diff notes/ against .state/ cursor → ingest deltas. Empty inbox = fully ingested |
| `session-capture` | on command, any surface | Summarize session's durable knowledge → inbox/ with provenance |
| `query` | on demand | Read root index → drill via links → synthesize with status-weighted citations → file good answers back (draft) → on explicit Curator confirmation of a cited claim, promote it (flow-of-use, below) |
| `lint` | scheduled (weekly minimum) | Contradiction sweep, staleness decay, stale note-citations, deleted-note withdrawal (§2.4), orphans, missing cross-refs, red-link triage, connection expiry, frontmatter conformance, program-consistency sweep (derived surfaces vs. doctrine, §11) |
| `digest` | scheduled (weekly) | Synthesis recap + review surface: new Connection pages, triaged promotion candidates, disputes. Curator marks it reviewed (marker in .state/) — the review event other clocks count |
| `mirror-snapshot` | scheduled | Snapshot vault → external git repo (§9) |
| `amend` | Curator-approved schema change, or §7.1 override pattern | Edit doctrine → locate derived statements via anchors (§11) → recompile affected surfaces → run consistency sweep → log the amendment in log.md |

Lint weekly minimum — contradictions compound. The digest is the review loop: the Curator reads it, acts on it, and never audits the vault wholesale.

**Verified is scarce by design; promotion is engineered, not hoped for.** Ingestion produces drafts at machine speed; promotion happens at human speed; the verified fraction stays small and agents work from status-weighted drafts. Promotion capacity:
- *Digest triage:* a leverage-ranked shortlist, hard-capped (~5–10 items), scored by graph centrality (hub claims first), query traffic (drafts recently cited in answers), and dispute adjacency. Everything below the cap stays draft indefinitely — correct, not a backlog.
- *Flow-of-use promotion:* when an answer cites a draft and the Curator **explicitly** confirms the claim, that is a review event — promote with provenance "Curator confirmed in session, <date>". Politeness is not assent; when unsure, ask. Corrections route through §2.3. Verification becomes exhaust from normal use; the most-used claims verify fastest.
- *Trust inheritance:* claims quoting Curator speech **verbatim** are born `verified`. Paraphrases are not — paraphrase is where misstatement lives.

If digest review exceeds ~15 minutes/week, the triage cap or scoring is wrong — fix the digest, never the Curator's schedule.

## 9. Versioning & Sync (deployment profile)

- Vault is iCloud-synced (Obsidian iOS continuity).
- **Sync-conflict quarantine:** sync layers silently spawn duplicate files ("conflicted copy" variants). The sweep excludes conflict-pattern filenames from ingestion and flags them — otherwise the sync layer becomes an unaudited source of divergent claims.
- **Git and iCloud must not cohabit.** No .git inside the iCloud vault — eviction/conflict behavior corrupts repos; this rules out the Obsidian Git plugin at the current vault location.
- `mirror-snapshot` copies the vault to a separate, non-iCloud git repo on schedule. The mirror is observational — diffs, history, rollback, recovery of expired pages — never a write gate (the status field is the gate, §5).
- If the vault moves off iCloud, revisit: direct git versioning becomes viable and the mirror retires.

## 10. Anti-patterns (named failure modes)

- **Laundered inference:** writing a guess with the typography of a fact. Status + observation/inference separation exist to prevent this.
- **Hand-healing:** the Curator editing wiki/ to fix an error. RCA upstream instead (§2.5).
- **Promiscuous capture:** auto-ingesting *external* content without a curation gate. (The notes/ and life-data streams are exempt: the Curator's own speech and scheduled personal exports are pre-curated by definition.)
- **Folder churn:** reorganizing wiki/ casually. Identity-is-path makes this a breaking migration (§3).
- **Silent retraction:** correcting a page without walking its dependents. Local healing, global poisoning (§5).
- **Politeness-as-promotion:** inferring verification from friendly acknowledgment (§8). The trust ledger only records explicit assent.
- **Silent exception:** an agent quietly complying with a doctrine-breaking instruction, or quietly reinterpreting it, without disclosure (§7.1). Both diverge the Curator's mental model from the system's reality — the translation must be spoken, the override must be logged.

## 11. Context Architecture (progressive disclosure)

No agent reads the whole program. Attention is the scarce resource; adherence degrades with rule-set size, so every context contains only the rules binding *now*. The doctrine is normative source; CLAUDE.md, skills, and READMEs are **derived surfaces compiled from it**.

| Level | Surface | Loaded when | Contains |
|---|---|---|---|
| L0 | CLAUDE.md core | always (any vault-touching agent) | ownership matrix, single-pipeline rule, status semantics, §7.1 behavior. **Hard budget: one page** — growth past it means something belongs in a skill or README |
| L1 | skill body | on invocation | the procedure plus every doctrine rule governing it (ingest embeds validation + modality + draft status; digest embeds the triage cap) |
| L2 | folder README | when writing to that folder | folder-local rules (connection expiry in connections/, calendar modality in life/) |
| L3 | this doctrine | constitutional cases only | amendment proposals, true §7.1 conflicts, RCA of system misbehavior |
| — | OKF SPEC.md | never at runtime | already compiled into §4 conventions and skill templates; the spec is for humans and tooling authors |

**Compilation drift** (derived surface contradicts doctrine) is this architecture's failure mode. Mitigations: precedence is explicit — doctrine wins, the derived file is the bug; amendments land in the doctrine first, then recompile outward, never the reverse; and lint runs a program-consistency sweep checking derived surfaces against doctrine (§8).

**Traceability anchors:** every compiled rule in a derived surface carries a comment pointing to its doctrine section (e.g., `<!-- doctrine §4: stream modality -->`). Locating all surfaces a rule compiled to is then mechanical (grep), for both the `amend` skill and the consistency sweep. Amendment is a single Curator conversation; multi-file propagation is machine work.

## 12. Open Items

- Physical home for the git mirror and scheduled agents (machine/runner).
- Deployment gaps: read-only enforcement for non-maintainer agents (honor-system; mirror diffs detect, OS permissions escalate), mirror window-of-loss between snapshots, session capture from mobile chat, mobile query via remote session (test).
- Per-type staleness half-lives (tune after first month of lint output).
- Bootstrap: annex, don't migrate — declare existing material sources/ (finished, frozen) or notes/ (live), stand up empty wiki/, let ingestion pull from old material opportunistically.
- Doctrine/deployment-profile split when stabilizing for share (§9 is the seam).
- v2 guardrails: executable-claim tests, full dependency tracking.

---
*Changelog: v0.3 — added §7.1 instruction-conflict protocol (translate/disclose/override/amend), silent-exception anti-pattern, §11 context architecture (progressive disclosure ladder, compilation model, drift mitigations); lint gains program-consistency sweep.*
*Changelog: v0.2 — full-consistency pass. Reassembled ownership matrix; resolved draft-exception conflict (§5↔§8); scoped promiscuous-capture anti-pattern; added .state/ (pipeline bookkeeping), inbox/quarantine/, digest review marker, connection-expiry recovery via mirror; genericized remaining role references; fixed cross-references; trimmed redundancy.*
