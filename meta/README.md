# meta/ — construction reference, not runtime

Nothing here is loaded during normal agent work, and none of it ships in the bundle.

- [HANDOFF.md](HANDOFF.md) — the build plan this vault was scaffolded from (historical record).
- [VAULT-DOCTRINE.md](VAULT-DOCTRINE.md) — the design session's high-resolution construction artifact. Its operational rules are **superseded** by CLAUDE.md, the skills, and folder READMEs; only CONSTITUTION.md (vault root) remains authoritative for principles.
- [OKF-SPEC.md](OKF-SPEC.md) — pinned copy of the external conformance target. **The bundle (wiki/) targets OKF v0.1** (draft, commit `ee67a5ca`, fetched 2026-07-16); the version declaration lives here rather than as frontmatter in wiki/index.md, because this vault keeps index files frontmatter-free. Never loaded at runtime — already compiled into skill templates. Local deviation from spec guidance: wiki links use file-relative paths, not the spec-recommended leading-slash form (spec §5.2 permits this) — Obsidian resolves leading-slash from the vault root, which breaks every link in the viewer.
- [DEPLOYMENT.md](DEPLOYMENT.md) — environment bindings skills reference instead of hardcoding.

This folder's name and location are the Curator's call; if it moves, update the references in `.claude/skills/mirror-snapshot/SKILL.md` and `.claude/skills/amend/SKILL.md` via the amend skill.
