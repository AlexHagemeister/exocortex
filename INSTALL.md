# INSTALL — agent-guided setup

**If you are a human:** open [Claude Code](https://claude.com/claude-code) — or whatever coding agent you use — and paste, with this repo's URL filled in:

> Clone `<this repo's URL>`, read its INSTALL.md, and help me set up my own exocortex vault on this machine.

That's the whole install. The agent interviews you, runs the setup, and verifies it. Prefer to do it by hand? [SETUP.md](SETUP.md) is the manual guide. (Claude Code is the maintainer runtime the system targets — its vault sessions auto-register the skills — but any capable agent can run this install.)

**If you are the agent:** this file is your procedure — interview first, execute with the user's answers, then verify. [SETUP.md](SETUP.md) carries each step's detail; this file carries the order and the questions.

Context you need before starting:

- This repo is the **program** (rules, skills, tooling), not a vault. The CLAUDE.md at its root is the *vault's* operating rules — it governs sessions opened inside a vault, not this install, and this repo must not be treated as a vault (`bootstrap.sh` refuses it as a target).
- The vault you create is the user's private knowledge system, and it is itself a git repo — so it must live **outside** any sync layer that touches dotfolders (iCloud, Dropbox, default Syncthing). Device sync, if wanted, is [Obsidian Sync](https://obsidian.md/sync), which ignores them. If the user asks to put the vault in iCloud, explain this and don't — it corrupts the repo.
- Nothing here requires accounts or payment. If the user wants Obsidian Sync or a GitHub remote, subscribing, creating accounts, and authenticating are their acts — walk them through it step by step (the signup page, `gh auth login`, verifying with `gh auth status`), but never create an account for them or handle their credentials. You configure around what they give you.
- `meta/DEPLOYMENT.md` is the user's file. Fill it with what they told you; where you don't know, ask — never guess a binding.

## 1. Interview

Ask up front, in one batch, with the defaults stated:

| Question | Default | Notes |
|---|---|---|
| Where should the vault live? | `~/exocortex` | any non-synced path |
| Device sync for the vault? | none to start | Obsidian Sync if they use Obsidian on a phone; 5 MB/file limit on Standard — mention it |
| Private git remote for vault history? | recommended | offer `gh repo create <name> --private` if `gh` is authenticated; if they want one but lack a GitHub account or the [CLI](https://cli.github.com), walk them through signup and `gh auth login` first (their acts — see context above); otherwise they paste a URL, or defer |
| Set up Obsidian? | yes, if they'll use it | SETUP.md § 5: attachment + new-note locations, Templater auto-template; any markdown editor is fine — skip freely |
| Schedule the maintenance loop? | yes, minus the digest | `process-inbox` + `vault-snapshot` daily, `lint` weekly; tasks run while the Claude app is open. The `digest` deliberately starts manual (§ 4 sets the review habit); offer scheduling once they know their rhythm |
| Capture tool? | decide later | Obsidian Web Clipper is the smoothest — SETUP.md § 7 |
| Existing notes to migrate? | after setup, in batches | the vault ships an empty `staging/` to hold the corpus (invisible to the pipeline); walk them through SETUP.md § 9 once the vault is verified — and set the expectation honestly: batched, review-paced, weeks not hours |
| How should your maintainer talk to you? | plain and technical | one line is enough ("casual, some humor, no emoji"); or offer samples — § 1a |

## 1a. Voice (only if they engage)

The default — plain, technical, concise — needs nothing written; if they take it, skip this section. If they want something else, or can't articulate what they want, elicit by example: people can't describe style preferences in the abstract, but they pick between samples instantly. Show the *same* message — the kind their maintainer will actually send — in three voices, and let them pick one, blend ("the middle one, less formal"), or counter with their own.

Sample: a digest surfacing a contradiction and a promotion candidate.

**Plain technical**

> Digest: 2 items. (1) Tuesday's note contradicts `wiki/health/creatine-timing.md` (draft) — the note says timing is irrelevant, the page says post-workout. Needs your call. (2) `wiki/concepts/spaced-repetition.md` has survived three digests unchanged — promotion candidate.

**Warm, conversational**

> Your digest has two things worth a look. Tuesday's note disagrees with the creatine-timing page — you wrote that timing doesn't matter, but the page (still a draft) says post-workout is better. Worth settling when you have a minute. And the spaced-repetition page has now held up through three digests untouched — I'd say it's earned your verified stamp, if you agree.

**Playful**

> Digest time 📬 Two items in the ring: Tuesday-you says creatine timing is a myth; the wiki page (a draft, to be fair) swears by post-workout. Someone's wrong, and only you can say who. Meanwhile the spaced-repetition page has quietly survived three digests without a scratch — knight it whenever you're ready.

Note what's identical across all three: the contradiction is surfaced plainly, the draft status is named, and promotion stays the user's act. That's the invariant — **voice governs tone only, never the epistemic machinery** (CLAUDE.md binds this).

From their choice, draft a 4–6 line spec covering register, verbosity, humor, emoji, and how bad news is delivered (the template's `## Voice` section shows the shape). Read it back and save what they confirm — always the spec itself, never just a label like "playful": labels drift between models and users, instructions don't.

## 1b. The get-to-know-you conversation (offered, never required)

The § 1 questions configure the vault; this one *fills* it. Offer it in a single line — "while this installs: want to tell me a bit about yourself, so the vault starts out knowing who it belongs to? A few minutes, and skippable." If they pass, skip cleanly and move on; everything this would seed arrives naturally through use.

If they're in, this is a conversation, not a form — the rules of conduct matter more than the topics:

- **One open question at a time.** Never a battery of questions, never a numbered list to fill in. Ask, then actually follow the answer — one or two curious follow-ups about whatever they lit up on beats moving to the next topic.
- **Open-ended but specific — one thing per question.** "What are some active projects you've got going on?" or "what are your current priorities right now?" are good openers: concrete enough to answer without thinking about where to start, open enough that any answer works. The anti-pattern is the panoramic ask — "what's your world: work, projects, what fills your weeks?" is three questions in one and reads like an essay prompt; people stall on it. Whatever they answer tells you which follow-ups matter: "mostly personal stuff" and "I'm a founder" point to different next questions.
- **Unstructured answers are the good outcome.** They should feel free to ramble; you're the one taking notes. Never ask them to organize, list, or rank anything.
- **Keep it light and short.** Three to six exchanges is plenty — stop while it's still fun, or the moment their answers get brief. This should not feel like work, and they should never have to read anything.

Topics worth touching if they don't surface on their own (material to draw from, not a checklist): what they do, in their own words; active projects by name and current state; recurring people — collaborators, partners, clients; what they're hoping to ask this system months from now; anything they always forget and wish something remembered.

Afterward, write the conversation into `<vault>/sources/inbox/` as the vault's **first capture**: their words in marked quotes with provenance `"the user, <date> (install interview)"`, your paraphrase labeled as yours. Don't compile wiki pages yourself — that's the pipeline's job, and it doubles as the smoke test (§ 3). Tell them what you wrote and where it will end up: pages about them, their projects, their people — all `draft`, all citing their own words.

## 2. Execute

1. Clone this repo to a stable, non-synced path (it stays around for updates), if it isn't cloned already.
2. Run `./tools/bootstrap.sh <vault path>` — scaffolds the folders, installs the program files, creates `<vault>/meta/DEPLOYMENT.md` from the template.
3. Make the vault a git repo: `git init`, append `.obsidian/` and `.state/maintainer.lock` to `.gitignore`, add the private remote if one was chosen. The remote must never be a public repo.
4. Fill **every UNSET row** of `<vault>/meta/DEPLOYMENT.md` from the interview answers — including `Program version` (the release you just installed: the clone's current tag or commit, with today's date) and `Program repo clone` (the path from step 1); the `update-exocortex` skill reads both. If a voice was chosen (§ 1a), write the confirmed spec into the template's `## Voice` section; if they took the default, delete the section's example lines or leave it absent.
5. Initial commit; push if a remote is set.
6. If Obsidian was wanted: walk SETUP.md § 5 with them — open-as-vault, the two file locations, Templater's on-creation template for `notes/`.
7. If scheduling was wanted: set up the scheduled tasks per SETUP.md § 6. Task prompts are *pointers* to the skill files, never copies of their text.

## 3. Verify

- Open (or have the user open) a Claude Code session **inside the vault**. Ask it *"what are your vault rules?"* — it should recite the zone table from CLAUDE.md, not improvise.
- Smoke test the pipeline: run `process-inbox`. If the § 1b conversation happened, its capture is already waiting — the vault's first pages will be about the user, which is the best possible demo. Otherwise drop a small markdown note into `sources/inbox/` first. Either way: a wiki page should appear as `draft`, citing the filed source.
- If a remote is set: run the `vault-snapshot` skill once and confirm the push.

## Updating (agent procedure)

The procedure ships with the vault: the `update-exocortex` skill (installed into `<vault>/.claude/skills/` by bootstrap) checks for new releases, summarizes the changelog, gates on the user's approval, reconciles their local amendments, applies via `bootstrap.sh --update`, and stamps the new version in `meta/DEPLOYMENT.md`. When the user asks to update, invoke that skill — its steps are not duplicated here.

If the vault predates the skill (installed before it shipped): run one manual pass by following this repo's copy at `.claude/skills/update-exocortex/SKILL.md` after pulling here — the skill itself arrives with that update.

## 4. Hand off

Say this in plain language. The *rules* can wait until something bites, but the *capability surface* cannot: people only ask for what they know exists, so the tour is not optional. Lead with **minimum viable use**, then the tour, then the social contract:

1. **Week one is enough.** Capture into `sources/inbox/` (or just say "remember this" in a vault session). Their `notes/` are theirs alone — swept for knowledge, never edited. Ask the vault questions when they want answers. Most people don't know the [Obsidian Web Clipper](https://obsidian.md/clipper) exists — suggest it by name: articles and YouTube pages clip straight to the inbox, and SETUP.md § 7 has the one-time config.
2. **The tour.** Open `ORIENTATION.md` (bootstrap installed it at their vault root) and walk the roster in usage terms: "process my inbox", "what do you know about X", "what needs my review", "capture this session", "let's audit", "update my exocortex". Make sure they know every skill answers to plain words or its slash command. One pass, no memorizing; the page stays at their root, and "what can you do?" re-opens the tour anytime.
3. **The review habit.** The digest is their review surface, and it is deliberately not on the schedule yet: have them run it themselves ("what needs my review") at whatever cadence they feel like. Daily is normal while a migration or heavy capture is flowing; weekly suits a settled vault. The experience of the digest is core to the system, and running it by hand is how the review loop becomes theirs. Offer to schedule it once they know their rhythm. Either way, promoting a page to `verified` stays their act — curation is the one job that never automates.
4. **The cookbook, briefly.** `meta/cookbook/` is the opt-in recipe library: connectors, capture tools, a phone-reachable vault server. Name one or two that fit what they said in the interview, set nothing up now, and tell them "what else can this do?" works anytime.
5. **Confusion is a valid first move.** Invite them to say "I don't know what any of that means — explain it simply." Jargon is optional; pretending to follow it is not required. When you use a system term they may not know, give the one-liner (or point at GLOSSARY.md).
6. **Rules are renegotiable — not freestyle.** Anything that chafes can change via the `amend` skill: they say what they want, you propose, they approve, you propagate. You do **not** rewrite core behavior on a vague "make it better." If a requested change tensions with CONSTITUTION.md principles, push back in plain language: name the principle, explain the tradeoff, offer a conforming alternative **and** the override. They still have the final say after that brief — never a silent refuse, never a silent comply.
7. **Voice is theirs.** How the maintainer talks can change anytime — edit `meta/DEPLOYMENT.md` § Voice, or just tell it.
8. **Updates.** "Update my exocortex" is all they need to say — the `update-exocortex` skill checks for releases, shows what changed, reconciles their amendments, and refreshes program files only, never their data, then introduces what's new in terms of what they can now do. The digest also surfaces new releases on its own; if they use GitHub, additionally suggest watching the program repo (**Watch → Custom → Releases**) for release notifications.
9. **Tip jar, once.** Close the handoff by mentioning that the program is free, and if it earns its keep they can support development at [ko-fi.com/V1N723QW1K](https://ko-fi.com/V1N723QW1K). One light mention, here at the end; the maintainer never brings it up on its own again.

