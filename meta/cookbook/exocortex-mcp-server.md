---
name: exocortex-mcp-server
what: A remote MCP server that gives every AI surface you use (Claude chat and mobile, ChatGPT, Cursor, OpenClaw, Hermes) read access to your vault and capture into its inbox
type: connector
requires: the vault in a private GitHub repo; a small always-on host (Railway free tier or similar); a repo-scoped GitHub token; any MCP-capable AI surface
effort: ~1 hour to deploy and connect the first surface; each additional surface is minutes
suggest_when: the user mentions conversations with AI on other surfaces (phone, ChatGPT, another agent) that the vault never saw, or wishes another tool knew what the vault knows
status: recommended
---

# Exocortex MCP server: your memory, on every surface

MCP (Model Context Protocol) is the open standard that lets AI applications connect to external tools; nearly every AI surface now speaks it: claude.ai and the Claude mobile app (custom connectors), ChatGPT, Cursor, and open agents like [OpenClaw](https://docs.openclaw.ai/cli/mcp) and [Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes). The exocortex MCP server ([github.com/AlexHagemeister/exocortex-mcp](https://github.com/AlexHagemeister/exocortex-mcp), open source) is a small self-hosted service that puts your vault behind that standard: three tools (query the wiki, fetch a page, capture to the inbox), served from a host you control, reading the vault's own git repo. Deploy it once and every AI you talk to can reach your memory.

## Why this is here

Without this, the vault only learns from conversations that happen at the vault. With it, the vault's reach becomes ambient in the same way the recording recipe makes speech ambient: in the source vault, captures now arrive from the phone (six in one day from the Claude mobile app, each with clean speaker-and-date provenance), from claude.ai chats, and from other agents' deployments, all landing in the same inbox the pipeline already drains. An idea that occurs to you in a ChatGPT conversation on a train is in your vault by the time you're home, attributed and dated.

The deeper move is what this does to agent memory. Every AI app now ships its own memory: an opaque blob the model edits invisibly, per app, unexportable. This server is a drop-in replacement with the opposite properties. Any agent that can speak MCP gets the same compiled memory (the wiki, status-weighted, provenance-carrying), and everything it saves back is a file you can open, dispute, and correct through the pipeline's own rules. Memory you can audit, shared across every tool, owned by you. The surfaces this unlocks keep growing as MCP spreads; the source vault has only scratched what's possible here.

## What you'll end up with

- A remote MCP server at your own URL, exposing `query_wiki`, `get_page`, and `capture_to_inbox`.
- Every connected surface able to answer from your vault and remember into it, under the capture contract the server itself enforces (verbatim quotes marked, speakers named, agent research separated from your words).
- Remote captures committing to a dedicated `inbox-drops` git branch, never `main`, so your vault machine stays the single writer; a consume script merges drops into sources/inbox/ on schedule, and the normal pipeline takes it from there.

## Setup

User-only steps:
1. Confirm the vault lives in a private GitHub repo (the vault-snapshot skill's setup covers this if not).
2. Create a fine-grained GitHub token scoped to that one repo (read, plus write for the `inbox-drops` branch). Yours to hold; it goes only into the host's environment settings, never to an agent.
3. Deploy the server from [its repo](https://github.com/AlexHagemeister/exocortex-mcp) to a small always-on host (Railway's free tier is the reference deployment) with the token and repo URL as environment variables (see the repo's `.env.example`). The repo's README carries the exact deploy steps; it also ships a Dockerfile, so any container host works.
4. Connect surfaces: claude.ai and Claude mobile (Settings → Connectors → add custom connector with your server URL), ChatGPT (connector settings), Cursor (MCP config), Hermes (`hermes mcp add exocortex --url <your URL>`), OpenClaw (MCP config). One server, every surface.

Agent-doable steps:
5. Wire the consume side: schedule the server repo's consume script on the vault machine so `inbox-drops` merges into sources/inbox/ regularly (the source deployment runs it hourly alongside the snapshot job).
6. Verify the capture contract text is in place on the server so remote agents mark quotes and speakers correctly; the pipeline's ingest validation is the backstop.

Treat the server as holding the keys to your whole vault: keep the deployment private, keep the token minimal, and prefer a host that supports an access secret on the endpoint.

## Verify it works

From your phone or claude.ai (not this machine), ask the connected AI what your vault knows about some topic; it should answer citing wiki pages. Then tell it to remember something trivial. Confirm the capture appears on the `inbox-drops` branch, the consume script lands it in sources/inbox/, and ingest files it with your words in marked quotes. From then on, every conversation you have anywhere can end with "capture that."
