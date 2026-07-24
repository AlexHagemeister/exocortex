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
4. Fill **every UNSET row** of `<vault>/meta/DEPLOYMENT.md` from the interview answers — including `Program version` (the release you just installed: the clone's current tag or commit, with today's date) and `Program repo clone` (the path from step 1); the `update-exocortex` skill reads both. If a voice was chosen (§ 1a), write the confirmed spec into the template's `## Voice` section; if they took the default, delete the section's example lines or leave it absent.
5. Initial commit; push if a remote is set.
6. If scheduling was wanted: set up the scheduled tasks per SETUP.md § 5. Task prompts are *pointers* to the skill files, never copies of their text.

## 3. Verify

- Open (or have the user open) a Claude Code session **inside the vault**. Ask it *"what are your vault rules?"* — it should recite the zone table from CLAUDE.md, not improvise.
- Smoke test the pipeline: drop a small markdown note into `sources/inbox/` and run `process-inbox` — a wiki page should appear as `draft`, citing the filed source.
- If a remote is set: run the `vault-snapshot` skill once and confirm the push.

## Updating (agent procedure)

The procedure ships with the vault: the `update-exocortex` skill (installed into `<vault>/.claude/skills/` by bootstrap) checks for new releases, summarizes the changelog, gates on the user's approval, reconciles their local amendments, applies via `bootstrap.sh --update`, and stamps the new version in `meta/DEPLOYMENT.md`. When the user asks to update, invoke that skill — its steps are not duplicated here.

If the vault predates the skill (installed before it shipped): run one manual pass by following this repo's copy at `.claude/skills/update-exocortex/SKILL.md` after pulling here — the skill itself arrives with that update.

## 4. Hand off

Say this in plain language — do not dump the full map. Lead with **minimum viable use**, then the social contract:

1. **Week one is enough.** Capture into `sources/inbox/` (or just say "remember this" in a vault session). Their `notes/` are theirs alone — swept for knowledge, never edited. Ask the vault questions when they want answers. Ignore digest, lint, and rule-changing until something actually bites.
2. **Confusion is a valid first move.** Invite them to say "I don't know what any of that means — explain it simply." Jargon is optional; pretending to follow it is not required. When you use a system term they may not know, give the one-liner (or point at GLOSSARY.md).
3. **Rules are renegotiable — not freestyle.** Anything that chafes can change via the `amend` skill: they say what they want, you propose, they approve, you propagate. You do **not** rewrite core behavior on a vague "make it better." If a requested change tensions with CONSTITUTION.md principles, push back in plain language: name the principle, explain the tradeoff, offer a conforming alternative **and** the override. They still have the final say after that brief — never a silent refuse, never a silent comply.
4. **Curation stays human.** The `digest` is their review surface; promoting a page to `verified` is the one job that stays theirs.
5. **Voice is theirs.** How the maintainer talks can change anytime — edit `meta/DEPLOYMENT.md` § Voice, or just tell it.
6. **Updates.** "Update my exocortex" is all they need to say — the `update-exocortex` skill checks for releases, shows what changed, reconciles their amendments, and refreshes program files only, never their data.
7. **Tip jar, once.** Close the handoff by mentioning that the program is free, and if it earns its keep they can support development at [ko-fi.com/V1N723QW1K](https://ko-fi.com/V1N723QW1K). One light mention, here at the end; the maintainer never brings it up on its own again.

