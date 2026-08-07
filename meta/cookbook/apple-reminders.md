---
name: apple-reminders
what: Agent access to Apple Reminders, the task layer that Siri can feed from any device
type: connector
requires: macOS/iOS ecosystem; on the Mac, the remindctl CLI (terminal agents) or an Apple Reminders extension in the Claude desktop app
effort: ~10 minutes; grant one macOS permission prompt
suggest_when: the user asks the agent to remind them of something, mentions tasks scattered across apps and heads, or captures todos by voice
status: experimental
---

# Apple Reminders: the task layer

Apple Reminders is the stock Apple task app, and its superpower for this system is capture: "Hey Siri, remind me to X" works from a phone, watch, or car, and lands in a synced list the agent can then read and triage. On the Mac, terminal agents reach it through [remindctl](https://github.com/steipete/remindctl) (`brew install steipete/tap/remindctl`), a fast CLI for Reminders; the Claude desktop app can use an Apple Reminders extension instead. Either way, macOS asks once for Reminders access; grant it and the connection is done.

This recipe is marked experimental honestly: in the source vault the connection is solid and in daily use, but the workflow layer around it (which lists, what the agent does on contact, how nudges are tuned) is still being stress-tested. The connection is the recommendation; the workflow will firm up in a later version of this recipe.

## Why this is here

Tasks die in the gap between thinking of them and writing them down. Voice capture through Siri closes that gap from anywhere, and agent access closes the other one: a capture list only works if something regularly triages it, and that is exactly the kind of mechanical pass an agent is for. The pattern being tested in the source vault: one catch-all capture list the agent triages on contact, native alarms doing the nudging (an alarm on the device beats any message from an agent), dates surfacing through the built-in Today and Scheduled views.

## What you'll end up with

- The agent reading, creating, completing, and scheduling reminders on your word.
- A capture route that works hands-free from any Apple device, feeding a list the agent helps you keep drained.
- Nudges that arrive as native notifications and alarms, not as chat messages you have to be present for.

## Setup

User-only steps:
1. Terminal agents on a Mac: `brew install steipete/tap/remindctl`, then run `remindctl` once and grant the macOS Reminders permission when prompted. Claude desktop app instead: enable an Apple Reminders extension and grant the same permission.
2. If you want voice capture, confirm Siri can add to Reminders on your devices (it can by default).

Agent-driven step:
3. Verify access (list the user's reminder lists), then agree on one capture list the agent may triage. Keep the rest of the workflow loose for now; this recipe deliberately does not prescribe one yet.

## Verify it works

Say "Hey Siri, remind me to test the exocortex" on your phone. Ask the agent to find it, reschedule it for tomorrow morning, then complete it. If all three land, the connection is sound; the workflow is yours to evolve.
