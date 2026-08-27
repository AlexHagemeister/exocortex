---
updated: 2026-08-22
---
# meta/ — construction reference, not runtime

Nothing here is loaded during normal agent work (one exception: cookbook/, whose README governs when recipes surface), and none of it ships in the bundle.

- [HANDOFF.md](HANDOFF.md): the build plan this vault was scaffolded from (historical record).
- [VAULT-DOCTRINE.md](VAULT-DOCTRINE.md): the design session's high-resolution construction artifact. Its operational rules are **superseded** by CLAUDE.md, the skills, and folder READMEs; only CONSTITUTION.md (vault root) remains authoritative for principles.
- [OKF-SPEC.md](OKF-SPEC.md): pinned copy of the external conformance target. **The bundle (wiki/) targets OKF v0.1** (draft, commit `ee67a5ca`, fetched 2026-07-16); the version declaration lives here rather than as frontmatter in wiki/index.md, because this vault keeps derived index files frontmatter-free (the `updated:` fields injected before 2026-07-20 are grandfathered; authored bundle hubs named `index.md` are pages, not indexes, hub law: wiki/projects/README.md). Never loaded at runtime. Already compiled into skill templates. Local deviation from spec: wiki links are Obsidian wikilinks by name (`[[name]]`, path-qualified `[[folder/name]]` when the name is not unique vault-wide), where spec §5 expects standard markdown links. Adopted 2026-08-17 (before that, file-relative markdown links, itself a deviation from the spec-recommended leading-slash form, which Obsidian resolves from the vault root and so breaks in the viewer). External consumers need a name-to-path index to follow links; files and folder structure are unchanged. The `sources:`/`depends_on:` extension fields are being retired in the same amendment; provenance is inline at the claim. A second deviation, documented deliberately at the 2026-07-31 check-1 respec: spec §6 expects `index.md` files frontmatter-free, but authored bundle hubs carry page frontmatter and are checked as pages (lint check 1); external consumers should treat any frontmatter-bearing `index.md` as a page.
- [DEPLOYMENT.md](DEPLOYMENT.md): environment bindings skills reference instead of hardcoding.
- [cookbook/](cookbook/README.md): opt-in recipe library: optional connectors, prompts, workflows, and automations the user can ask the agent to set up. Ships with the program; inert until the user opts in. Folder law in its README (added 2026-08-06).

This folder's name and location are the Curator's call; if it moves, grep the vault for `meta/` references and update every one via the amend skill.
