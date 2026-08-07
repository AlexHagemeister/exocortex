---
name: obsidian-web-clipper
what: One-click capture of web pages and YouTube videos into the vault's inbox, as markdown with provenance-carrying frontmatter
type: connector
requires: Obsidian with the vault open; Chrome, Firefox, Safari, or Edge; optional LLM API key (e.g. OpenRouter) for auto-filled frontmatter
effort: ~10 minutes; the optional Interpreter step adds ~5 more and an API key
suggest_when: the user shares a link or article they want remembered, retells something they read, or can't relocate a page they know they saw
status: recommended
---

# Obsidian Web Clipper: web capture into the inbox

Obsidian Web Clipper is the free, open-source browser extension from the Obsidian team ([obsidian.md/web-clipper](https://obsidian.md/help/web-clipper)). It saves any web page, or just your selection and highlights, straight into your vault as markdown, with a template filling in frontmatter at the moment of capture. That template is why this recipe exists: unlike copy-paste or a read-later app, a clip lands in sources/inbox/ already shaped for the pipeline, provenance attached from birth. It handles article pages, papers, blog posts, and YouTube video pages alike.

Install for your browser: [Chrome](https://chromewebstore.google.com/detail/obsidian-web-clipper/cnjifjpddelmedmihgijeibhnjfabmlf) · [Firefox](https://addons.mozilla.org/en-US/firefox/addon/web-clipper-obsidian/) · [Safari (macOS/iOS/iPadOS)](https://apps.apple.com/us/app/obsidian-web-clipper/id6720708363) · [Edge](https://microsoftedge.microsoft.com/addons/detail/obsidian-web-clipper/eigdjhmgnaaeaonimdklocfekkaanfme)

## Why this is here

Clipping is the vault's main road for external knowledge. In the vault this program came from, essays, arXiv papers, client documents, launch posts, and YouTube videos all entered this way; nearly everything the wiki knows about the outside world started as a clip. The habit it replaces is the one where you read something good, think "I should remember this," and lose it.

The unlock is that a reading habit quietly becomes a compiled research brain. Because every clip carries its source URL and capture date, everything the wiki later builds from it stays traceable to the original: you can ask "what did that article actually argue?" months later and get an answer with citations, not a vibe. And it stacks with the rest of the pipeline for free: clip on any device, and ingest does the filing, summarizing, and cross-linking without you touching a folder.

## What you'll end up with

- A browser button (and mobile share-sheet entry via the Safari app) that saves any page or selection to sources/inbox/ as markdown.
- Frontmatter on every clip: title, source URL, author, clipped date, description, and a `clippings` tag, so provenance exists before the pipeline ever runs.
- Ingest filing each clip to its permanent stream (usually sources/articles/) and compiling wiki pages from it.
- Optionally, an LLM auto-filling the description at clip time (the Interpreter feature below).

## Setup

User-only steps:
1. Install the extension from the link above for your browser, with Obsidian installed and your vault open at least once.
2. In the extension's settings, add your vault under General so the clipper can write to it.

Steps the agent can walk you through (settings live in the extension, so your hands are on the clicks):
3. Edit the default template (templates accept arbitrary frontmatter properties, so these get defined, not found). Set the note location to `sources/inbox/` and define exactly these properties: `title`, `source`, `author`, `clipped-date`, `description`, and `tags: clippings`. Ingest validates these fields and generates the stream indexes from them.
4. Optional, the Interpreter (auto-fills the description at clip time). If the user wants it: in extension settings, toggle on Interpreter, set the provider to OpenRouter (a supported preset; one key reaches many models), set the model to a small fast one (Claude Haiku or Gemini Flash class; the task is light and Obsidian's docs recommend small models), and have the user paste their API key (theirs to handle; never take custody of a key). Then set the template's description property to a prompt variable, e.g. `{{"one-paragraph summary of what this page claims"}}`, and the clipper fills it at capture time. Docs: [Interpreter](https://obsidian.md/help/web-clipper/interpreter).

A note on the auto-filled fields: the pipeline already treats a capture tool's title and description as unverified and checks them against the body at ingest, so the Interpreter is a convenience, not a truth source. A wrong auto-summary gets caught before it freezes into the record.

## Verify it works

Clip any article. Confirm a markdown file appears in sources/inbox/ with the frontmatter filled. Then run the inbox (ask the agent, or wait for the scheduled process-inbox run) and confirm the clip files to sources/articles/ with a wiki summary page citing it. From then on, capture is one click from anywhere you read.
