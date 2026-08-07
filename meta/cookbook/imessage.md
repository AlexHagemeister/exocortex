---
name: imessage
what: Agent access to Messages on a Mac: find, read, and draft texts in conversation
type: connector
requires: a Mac with Messages signed in; the Claude desktop app's iMessage extension (or an equivalent local MCP)
effort: ~5 minutes; grant the macOS permissions it requests
suggest_when: the user retells a text exchange from memory, or asks the agent to check or send a message
status: experimental
---

# iMessage: texts in the conversation

Messages is where a lot of real coordination happens, and it is invisible to every agent by default. On a Mac, the Claude desktop app's iMessage extension (or an equivalent local MCP server) gives the agent access to it: search conversations, read threads, check unread, and draft or send messages. Setup is enabling the extension and granting the macOS permissions it requests; the messages never leave your machine except as part of your conversation with the agent.

Like the Reminders recipe, this one is experimental by honest labeling: the connection works and sees real use in the source vault, but the workflow patterns around it are still settling. Connect it, use it conversationally, and let your own patterns emerge.

## Why this is here

The immediate payoff is small and constant: "what was the address she texted me?" gets answered from the thread instead of a phone-scrolling session, and "text him I'm running ten minutes late" happens without leaving the conversation. The larger one is that texts are context: plans, commitments, and logistics live in Messages, and an agent that can see them stops asking you to retype your own life.

Two cautions belong in the recipe, not the fine print. Messages are other people's words: anything from a thread that enters the vault must carry its speaker, same as any source. And sending is outward-facing: the agent drafts and shows you the exact text and recipient, and your explicit yes sends it. That default is not negotiable at setup time; loosen it later if you ever want to, deliberately.

## What you'll end up with

- The agent searching and reading your Messages threads on request.
- Outbound texts drafted in conversation and sent only on your confirmation of the exact text and recipient.
- One less silo: the coordination layer of your life becomes visible to the agent that helps you plan around it.

## Setup

User-only steps:
1. In the Claude desktop app on your Mac, enable the iMessage extension (or install an equivalent local MCP server for your agent surface).
2. Grant the macOS permissions it requests; reading Messages requires deeper disk access than most apps, which is also why a local-only connection is the right shape for this data.

Agent-driven step:
3. Verify by searching for a recent conversation, and state the sending rule out loud so it's on the record: draft, show, send only on explicit confirmation.

## Verify it works

Ask the agent what your most recent unread text says. Then have it draft (not send) a reply. If both work, connected. The first time it saves you a phone-scroll, you'll know why it's here.
