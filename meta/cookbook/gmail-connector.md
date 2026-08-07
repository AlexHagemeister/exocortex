---
name: gmail-connector
what: Agent access to Gmail for search, triage, labels, filters, and drafts, starting with zero deployment
type: connector
requires: a Google account; claude.ai's built-in Gmail connector (a self-hosted email MCP is the optional growth path)
effort: ~5 minutes to connect; a triage system like the source vault's takes an afternoon to design
suggest_when: the user pastes or retells email content, mentions inbox overwhelm or a buried thread, or asks what someone said in an email
status: recommended
---

# Gmail connector: your inbox as agent territory

claude.ai ships a first-party Gmail connector (Settings → Connectors, a normal Google sign-in): no server, no keys to manage, nothing to deploy. Once connected, the agent can search and read mail, work with labels, and draft replies. That zero-cost start is the point of this recipe; a self-hosted email MCP server is the growth path if you later want finer-grained tools or the same access from other surfaces, but nobody should have to deploy infrastructure to stop copy-pasting emails into a chat window.

## Why this is here

Email is where commitments, receipts, and context go to be forgotten. Connected, it becomes two things at once. First, a queryable corpus: "what did the landlord actually say about the deposit?" gets answered from the thread itself, not your memory of it. Second, and bigger: triage becomes delegable. In the source vault's use, this grew into a full system that has run since mid-2026: a minimal sender-based scheme across two accounts, where automatic filters handle known senders and the agent runs interactive triage over what's left, proposing verdicts sender by sender while the user just approves. The inbox went from backlog to maintained, and the labels went from a sprawling taxonomy to a handful that mean something.

The unlock generalizes past triage: you stop being the API between your inbox and everything else. Travel plans flow to the calendar, commitments flow to your task system, and knowledge worth keeping flows to the vault, with the agent doing the ferrying.

## What you'll end up with

- The agent searching and reading your mail on request, so email content enters conversations without copy-paste.
- Labels and filters managed through conversation ("archive everything from this sender and label future ones").
- Drafts written for your review. Sending stays your act: the agent prepares, you fire.
- Optionally, a triage routine: the agent sweeps the inbox, proposes an action per sender or thread, and executes only the ones you approve.

## Setup

User-only step:
1. On claude.ai: Settings → Connectors → connect Gmail and complete the Google sign-in.

Agent-driven steps (walk the user through these; don't wait to be asked):
2. Agree on the ground rules and state them plainly: the agent drafts but never sends; archiving or deleting happens only on explicit per-run approval. These defaults protect the user; relaxing them is the user's move, later, if trust is earned.
3. If the user wants triage, start small and sender-based: one pass over the current inbox, propose a verdict per sender (filter, label, archive, keep), execute the approved ones, and let filters accumulate run over run. Resist inventing a label taxonomy up front; labels earn their existence.
4. Growth path, only if the user asks for more: a self-hosted email MCP server gives finer-grained tools and works from any MCP surface. That is a separate project with its own credential handling; the built-in connector is the right start.

## Verify it works

Ask the agent to summarize today's unread mail. Then have it find a specific older thread by description ("the one about the security deposit"). If both land, connected. The first triage pass will tell you the rest.
