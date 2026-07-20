# INSTALL — agent-guided setup

**If you are a human:** open [Claude Code](https://claude.com/claude-code) — or whatever coding agent you use — and paste, with this repo's URL filled in:

> Clone `<this repo's URL>`, read its INSTALL.md, and help me set up my own exocortex vault on this machine.

That's the whole install. The agent interviews you, runs the setup, and verifies it. Prefer to do it by hand? [SETUP.md](SETUP.md) is the manual guide. (Claude Code is the maintainer runtime the system targets — its vault sessions auto-register the skills — but any capable agent can run this install.)

**If you are the agent:** this file is your procedure — interview first, execute with the user's answers, then verify. [SETUP.md](SETUP.md) carries each step's detail; this file carries the order and the questions.

Context you need before starting:

- This repo is the **program** (rules, skills, tooling), not a vault. The CLAUDE.md at its root is the *vault's* operating rules — it governs sessions opened inside a vault, not this install, and this repo must not be treated as a vault (`bootstrap.sh` refuses it as a target).
- The vault you create is the user's private knowledge system, and it is itself a git repo — so it must live **outside** any sync layer that touches dotfolders (iCloud, Dropbox, default Syncthing). Device sync, if wanted, is [Obsidian Sync](https://obsidian.md/sync), which ignores them. If the user asks to put the vault in iCloud, explain this and don't — it corrupts the repo.
- Nothing here requires accounts or payment. If the user wants Obsidian Sync or a GitHub remote, subscribing or creating those is their act — you configure around what they give you.
- `meta/DEPLOYMENT.md` is the user's file. Fill it with what they told you; where you don't know, ask — never guess a binding.

## 1. Interview

Ask up front, in one batch, with the defaults stated:

| Question | Default | Notes |
|---|---|---|
| Where should the vault live? | `~/exocortex` | any non-synced path |
| Device sync for the vault? | none to start | Obsidian Sync if they use Obsidian on a phone; 5 MB/file limit on Standard — mention it |
| Private git remote for vault history? | recommended | offer `gh repo create <name> --private` if `gh` is authenticated; otherwise they paste a URL, or defer |
| Schedule the maintenance loop? | yes | `process-inbox` + `vault-snapshot` daily, `lint` + `digest` weekly; tasks run while the Claude app is open |
| Capture tool? | decide later | Obsidian Web Clipper is the smoothest — SETUP.md § 6 |
| Existing notes to migrate? | after setup, in batches | if they have a corpus in another app, walk them through SETUP.md § 8 once the vault is verified — and set the expectation honestly: batched, review-paced, weeks not hours |
| How should your maintainer talk to you? | plain and technical | one line is enough ("casual, some humor, no emoji"); or offer samples — § 1a |

## 1a. Voice (only if they engage)

The default — plain, technical, concise — needs nothing written; if they take it, skip this section. If they want something else, or can't articulate what they want, elicit by example: people can't describe style preferences in the abstract, but they pick between samples instantly. Show the *same* message — the kind their maintainer will actually send — in three voices, and let them pick one, blend ("the middle one, less formal"), or counter with their own.

Sample: a weekly digest surfacing a contradiction and a promotion candidate.

**Plain technical**

> Digest: 2 items. (1) Tuesday's note contradicts `wiki/health/creatine-timing.md` (draft) — the note says timing is irrelevant, the page says post-workout. Needs your call. (2) `wiki/concepts/spaced-repetition.md` has survived three digests unchanged — promotion candidate.

**Warm, conversational**

> Your digest has two things worth a look. Tuesday's note disagrees with the creatine-timing page — you wrote that timing doesn't matter, but the page (still a draft) says post-workout is better. Worth settling when you have a minute. And the spaced-repetition page has now held up through three digests untouched — I'd say it's earned your verified stamp, if you agree.

**Playful**

> Digest time 📬 Two items in the ring: Tuesday-you says creatine timing is a myth; the wiki page (a draft, to be fair) swears by post-workout. Someone's wrong, and only you can say who. Meanwhile the spaced-repetition page has quietly survived three digests without a scratch — knight it whenever you're ready.

Note what's identical across all three: the contradiction is surfaced plainly, the draft status is named, and promotion stays the user's act. That's the invariant — **voice governs tone only, never the epistemic machinery** (CLAUDE.md binds this).

From their choice, draft a 4–6 line spec covering register, verbosity, humor, emoji, and how bad news is delivered (the template's `## Voice` section shows the shape). Read it back and save what they confirm — always the spec itself, never just a label like "playful": labels drift between models and users, instructions don't.

## 2. Execute

1. Clone this repo to a stable, non-synced path (it stays around for updates), if it isn't cloned already.
2. Run `./tools/bootstrap.sh <vault path>` — scaffolds the folders, installs the program files, creates `<vault>/meta/DEPLOYMENT.md` from the template.
3. Make the vault a git repo: `git init`, append `.obsidian/` and `.state/maintainer.lock` to `.gitignore`, add the private remote if one was chosen. The remote must never be a public repo.
4. Fill **every UNSET row** of `<vault>/meta/DEPLOYMENT.md` from the interview answers. If a voice was chosen (§ 1a), write the confirmed spec into the template's `## Voice` section; if they took the default, delete the section's example lines or leave it absent.
5. Initial commit; push if a remote is set.
6. If scheduling was wanted: set up the scheduled tasks per SETUP.md § 5. Task prompts are *pointers* to the skill files, never copies of their text.

## 3. Verify

- Open (or have the user open) a Claude Code session **inside the vault**. Ask it *"what are your vault rules?"* — it should recite the zone table from CLAUDE.md, not improvise.
- Smoke test the pipeline: drop a small markdown note into `sources/inbox/` and run `process-inbox` — a wiki page should appear as `draft`, citing the filed source.
- If a remote is set: run the `vault-snapshot` skill once and confirm the push.

## Updating (agent procedure)

When the user asks to update an existing installation:

1. `git pull` in the program clone (its path is in the vault's `meta/DEPLOYMENT.md`). Read the CHANGELOG.md entries between the previously installed version and the new one — that's what you're about to apply, and what you summarize to the user.
2. **Reconcile before overwriting.** Diff the shipped `CLAUDE.md` and `.claude/skills/` against the vault's copies. Every difference is one of two things: an upstream change (apply it) or the user's local amendment made via the `amend` skill (theirs — surface it and ask: keep local, take upstream, or merge). Never silently overwrite a local amendment.
3. Run `./tools/bootstrap.sh <vault> --update`, then re-apply any kept-local or merged files from step 2.
4. Verify as in § 3 (rules recital in a vault session). Report what changed, old version → new.

## 4. Hand off

Leave the user knowing, in a few sentences: capture goes into `sources/inbox/` (or just "remember this" in a vault session); their `notes/` are theirs alone — swept for knowledge, never edited; the `digest` is their review surface, and promoting a page to `verified` is the one job that stays human; the rules are theirs to renegotiate via the `amend` skill; how their maintainer talks is theirs to change anytime — edit `meta/DEPLOYMENT.md` § Voice, or just tell it; updates arrive with `git pull` in this repo + `bootstrap.sh <vault> --update`, which refreshes program files only and never touches their data.
