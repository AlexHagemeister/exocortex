---
updated: 2026-08-06
---
# cookbook/ — opt-in recipes

A curated library of optional add-ons: external tools to connect, prompts to run, workflows and automations to adopt. Everything here ships with the program and does nothing until the user opts in. Each recipe is an earned recommendation: it exists because it proved useful in real vault use, and it says so.

This folder is program content, not vault knowledge. Never sweep, ingest, cite as evidence, or index anything here. Recipes make no claims about the world; they describe things the user can choose to set up.

## What a recipe is

One markdown file per recipe. A recipe that outgrows one file (assets, multiple workflow documents) becomes a subfolder with an authored `index.md` hub, the same shape as a project bundle.

Frontmatter:

```yaml
name: <kebab-case-slug>
what: <one line: what the user ends up with>
type: connector | prompt | workflow | automation
requires: <accounts, tools, platforms needed; "none" is valid>
effort: <rough setup cost, e.g. "5 minutes, one API key">
suggest_when: <conversation friction that makes this recipe relevant>
status: recommended | experimental
```

The body opens with a short context paragraph before any numbered section: what the tool or technique is in plain terms, why this one over the obvious alternatives, and a direct link to where to get it. Never assume the reader knows the product; the recipe should hand the agent everything setup needs, links included. Then, in order:

1. **Why this is here** — the real use that earned the recommendation, and the larger unlock it points at. A recipe should communicate its latent potential, not just its mechanics; show the earned evidence, don't just declare the value.
2. **What you'll end up with** — concrete capability after setup, so the user can decide from this section alone.
3. **Setup** — exact steps and config detail, split into what the agent can do and what only the user can do (account creation, credentials, approvals). Enough detail that the agent can drive setup without outside research. Written for the agent driving it: prescribe exact settings and advise the user through their clicks; never hand the user a menu of configuration choices. The user decides whether to adopt the recipe and its optional parts; the recipe decides the settings.
4. **Verify it works** — how to confirm the recipe is live.

## Surfacing (binds you, the agent)

- Offer a recipe only when conversation friction matches its `suggest_when`. At most one suggestion per session, never mid-task.
- The digest may carry at most one recipe suggestion per cycle.
- A suggestion is one line and a pointer; the user's silence is a no. Set up only on an explicit yes, following the recipe's Setup section.
- If the user asks what's available ("what else can this do?"), the whole cookbook is fair to show.
- One exception to the friction gate: onboarding. The install handoff may overview the whole cookbook as orientation, before any friction exists. An introduction to what's possible, never a setup push.

## Authoring

When the user says "add this to the cookbook", draft the recipe here directly for their review. No inbox, no ingest: recipes are program content, and the format above is the gate. Keep config specifics generic (placeholders, never real keys or account names).
