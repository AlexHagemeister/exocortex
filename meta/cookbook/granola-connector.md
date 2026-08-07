---
name: granola-connector
what: Ambient recording of anything spoken, with transcripts flowing into the vault as frozen, queryable sources
type: connector
requires: Granola account and app (Mac/iOS); a Claude surface that supports MCP connectors
effort: ~15 minutes (install the app, connect the connector); the habit takes a week
suggest_when: the user retells a conversation from memory, wishes they had a record of a meeting or call, or asks what was said or agreed in a past conversation
status: recommended
---

# Granola connector: ambient recording

Granola ([granola.ai](https://www.granola.ai), [download](https://notes.granola.ai/download)) is a transcription app that records device-side: it captures your microphone and system audio on the machine itself, and the phone app covers calls and in-person conversations. No bot joins your meeting. That design is why this recipe names Granola rather than a bot-based transcriber: bots announce themselves and only exist inside scheduled video calls, while device-side capture means a phone call, a walk-through, or an appointment records the same way a Zoom call does. It also exposes an MCP connector, which is what lets your agent pull transcripts straight into the vault.

## Why this is here

This recipe started as "record work meetings" and turned out to be something much bigger. In the vault this program came from, the meetings stream now holds client syncs, a trade-show sprint (ten vendor conversations captured in two days, each one a searchable record), phone calls with schedulers and support lines, and in-person appointments. The pattern that emerged: once recording is ambient, **anything spoken becomes a source**. You stop taking notes in the moment, stop reconstructing conversations from memory, and start asking the vault "what did they actually say?"

That is the latent potential of this recipe, and it compounds. Verbal commitments, expert advice given out loud, negotiation positions, what a doctor or contractor or landlord told you: whole categories of your life become queryable that never were before. The vault turns each transcript into speaker-weighted evidence, so a salesperson's pitch and your own recorded words carry different weight by design.

And the list above is a floor, not a ceiling. It is just what one vault's use surfaced in the first few months, and none of it was planned; each use appeared the first time a conversation happened near a running recorder. Once capture is ambient, you will find uses no recipe anticipated, and the vault will already be ready for them.

One obligation comes with it: recording other people carries consent norms and laws that vary by place. Knowing and honoring them is your call, not the agent's.

## What you'll end up with

- Granola recording your meetings and calls ambiently (mic plus system audio) and producing machine transcripts.
- A Claude connector that can list your meetings and pull any transcript on request.
- Transcripts flowing through sources/inbox/ into the sources/meetings/ stream as frozen records, then compiled into the wiki: people pages, project pages, and decision histories built from what was actually said.
- The evidential rules ride along automatically: sources/meetings/README.md weights claims by speaker, and no claim is born verified from a transcript alone.

## Setup

User-only steps:
1. Create a Granola account and install the app ([notes.granola.ai/download](https://notes.granola.ai/download); macOS, Windows, iOS, Android) on the devices where conversations happen. Grant microphone and system-audio permissions.
2. Connect the Granola MCP connector to your Claude surface (claude.ai: Settings → Connectors; Claude Code: add the MCP server). Granola's own guide: [granola.ai/help-center/sharing/integrations/mcp](https://granola.ai/help-center/sharing/integrations/mcp). Authentication is yours to complete.

Agent-doable steps (ask, and the agent does the rest):
3. Confirm the connector's tools are visible (listing meetings, fetching transcripts).
4. Pull a transcript, write it to sources/inbox/ with a provenance block (date, participants, capture tool), and run ingest. It files to sources/meetings/ under the date-plus-counterpart naming convention.

## Verify it works

Ask the agent to list your recent Granola meetings. Pick one, have it pulled through the inbox, and confirm ingest files it to sources/meetings/ and produces a summary page citing it. From then on, "pull yesterday's call into the vault" is a one-line request.
