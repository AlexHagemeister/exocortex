---
name: google-calendar-connector
what: Agent-managed Google Calendar, with a commute-etiquette that makes plans physically realistic
type: connector
requires: a Google account; claude.ai's built-in Google Calendar connector (or any Google Calendar MCP server on other surfaces)
effort: ~5 minutes to connect; the etiquette applies per event from then on
suggest_when: the user asks the agent to schedule anything, plan a day or week, or mentions running late, double-booking, or forgetting travel time
status: recommended
---

# Google Calendar connector: a calendar the agent maintains

Google Calendar needs no introduction, but the connector might: claude.ai ships a first-party Google Calendar connector (Settings → Connectors, a normal Google sign-in), so there is nothing to deploy or host. Once connected, the agent can read your schedule and create, move, and update events with your approval. Other surfaces can get the same access through any Google Calendar MCP server. The reason this is a recipe and not just a checkbox is the etiquette that comes with it, learned the hard way in real use.

## Why this is here

A calendar the agent can write to turns "remind me about dinner Friday" into a placed, durable plan; scheduling stops being a copy-paste job between the conversation and the calendar app. But the earned part of this recipe is smaller and sharper: **events with a location get commute events**. In the source vault's use, every located event gets a paired → event before (travel there) and ← event after (travel back), each carrying origin and destination in its location field. The plan on the calendar is then the plan in reality: no more back-to-back bookings that pretend teleportation, no more being reminded of an event at the moment you were supposed to leave.

The second lesson cuts against agent instinct: **the agent never estimates travel time**. Estimates are confidently wrong in both directions. The user checks the real route in Google Maps at planning time (a 30-second act with traffic-aware ground truth) and tells the agent the number. The unlock compounds from there: once the calendar is agent-writable and physically honest, it becomes the agent's surface for your whole day: prep notes in event descriptions, buffers, follow-ups placed while you talk.

## What you'll end up with

- The agent reading your calendar and creating, moving, and updating events on your word.
- Every located event flanked by → and ← commute events with real (user-checked) durations and origin→destination locations.
- Day and week planning that starts from your actual schedule instead of your description of it.

## Setup

User-only step:
1. On claude.ai: Settings → Connectors → connect Google Calendar and complete the Google sign-in. On other surfaces, add a Google Calendar MCP server per that surface's MCP configuration.

Agent behavior (this part is configuration-free; adopting it is the recipe):
2. When creating any event with a location, drive the etiquette proactively; don't wait to be asked. Ask the user to check Google Maps for the real travel time from where they'll actually be coming from. Never substitute your own estimate. Then create the → and ← commute events around the event, origin→destination in each location field.
3. Confirm before writing. Calendar events are outward-facing (invites, shared calendars), so show the user what you're about to create and get their yes.
4. When planning a day or week, read the calendar first and treat commute events as immovable as the events they serve.

## Verify it works

Ask the agent to schedule a test event somewhere across town. It should ask you for the Maps travel time, propose the event plus two commute events, and create all three on your confirmation. Check your calendar: three blocks, physically honest. Delete the test and it's live.
