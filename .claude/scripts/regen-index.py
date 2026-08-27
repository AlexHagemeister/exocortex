#!/usr/bin/env python3
"""regen-index.py <folder> — regenerate a derived index.md from page frontmatter.

Mechanical half of index regeneration (ingest step 7 / lint check 9):
  - refuses to touch an authored bundle hub (index.md carrying page
    frontmatter: type/title/status) — hub law: wiki/projects/README.md;
  - preserves the existing index's section headers and each page's section
    assignment (section slotting is the agent's judgment, and the user may
    re-slot freely — those choices stick);
  - new pages land under "# New (uncategorized)" and are printed so the
    agent slots them; entries for deleted pages are dropped and printed;
  - non-markdown stream items (PDFs, images) list by filename, since they
    carry no frontmatter — a derived index must not omit a filed source;
  - nested bundles appear as one entry per bundle — the authored hub
    (<sub>/index.md, same frontmatter test as the guard), titled and
    described from the hub's own frontmatter; satellites are reachable
    through the hub, never listed here (amendment, 2026-07-31);
  - entries are Obsidian wikilinks (link convention approved 2026-08-17):
    `* [[name|Title]] - description` when the target's basename (stem,
    case-insensitive) is unique across every non-dot folder of the vault,
    `* [[vault/relative/path|Title]] - description` otherwise (index and
    README targets always qualify). Non-md items link by filename with its
    extension, path-qualified on collision. Folders inside a dot-folder
    (.state/issues) keep markdown links, because Obsidian does not resolve
    wikilinks into dot-folders. Both forms parse back on the next run, so
    section assignments survive the changeover.

Exit codes: 0 regenerated · 1 usage/error · 2 refused (authored hub)
"""
import datetime
import re
import sys
from collections import defaultdict
from pathlib import Path

ENTRY_RE = re.compile(r"^\*\s+\[(?P<title>.*?)\]\((?P<path>[^)]+)\)(?:\s+-\s+(?P<desc>.*))?\s*$")
WIKI_ENTRY_RE = re.compile(r"^\*\s+\[\[(?P<target>[^\]|#]+)(?:\|(?P<title>[^\]]*))?\]\](?:\s+-\s+(?P<desc>.*))?\s*$")
EXCLUDE = {"index.md", "README.md", "log.md"}
NEW_SECTION = "New (uncategorized)"
VAULT_MARKERS = ("CLAUDE.md", "wiki")


def find_vault_root(folder: Path) -> Path:
    """Nearest ancestor holding CLAUDE.md and wiki/ (so a scratch copy of the vault
    works); falls back to this script's own vault (.claude/scripts/ -> root)."""
    for cand in (folder, *folder.parents):
        if all((cand / m).exists() for m in VAULT_MARKERS):
            return cand
    return Path(__file__).resolve().parents[2]


def is_dot_path(rel: Path) -> bool:
    return any(part.startswith(".") for part in rel.parts)


def stem_index(root: Path):
    """Uniqueness maps over every non-dot folder of the vault, mirroring
    migrate-links-pass1.py's Vault.by_stem (duplicated, ~15 lines, on purpose:
    scripts stay single-file). md_stems: lower stem -> [rel paths] of .md files.
    other_names: lower filename (with extension) -> [rel paths] of non-md files."""
    md_stems = defaultdict(list)
    other_names = defaultdict(list)
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if is_dot_path(rel):
            continue
        if p.suffix.lower() == ".md":
            md_stems[p.stem.lower()].append(rel.as_posix())
        else:
            other_names[p.name.lower()].append(rel.as_posix())
    return md_stems, other_names


def wikilink(target_rel: Path, title: str, md_stems, other_names, in_dot: bool) -> str:
    """Emit the entry's link. target_rel is vault-relative. Falls back to a
    markdown link when the target sits in a dot-folder or the title would break
    wikilink syntax; the parser accepts both forms."""
    if in_dot or "|" in title or "]]" in title or "[[" in title:
        return None
    if target_rel.suffix.lower() == ".md":
        hits = md_stems.get(target_rel.stem.lower(), [])
        name = target_rel.stem if len(hits) == 1 else target_rel.with_suffix("").as_posix()
        return f"[[{name}|{title}]]"
    hits = other_names.get(target_rel.name.lower(), [])
    if len(hits) == 1:
        return f"[[{target_rel.name}]]"
    return f"[[{target_rel.as_posix()}|{target_rel.name}]]"


def entry_key(target: str, folder_rel: Path, entries: dict) -> str:
    """Map a wikilink target back to the folder-relative entry key used for
    section assignment (`foo.md`, `sub/index.md`, `scan.pdf`)."""
    t = target.strip()
    if "/" in t:
        prefix = folder_rel.as_posix() + "/" if folder_rel.as_posix() not in ("", ".") else ""
        key = t[len(prefix):] if prefix and t.startswith(prefix) else Path(t).name
    else:
        key = t
    if Path(key).suffix == "":
        key = key + ".md"
    if key in entries:
        return key
    same = [n for n in entries if Path(n).name.lower() == Path(key).name.lower()]
    return same[0] if len(same) == 1 else key


def read_frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fm = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            val = m.group(2).strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            fm[m.group(1)] = val
    return fm


def stamp() -> str:
    # Bare date, nothing else (ingest step 5, amendment 2026-08-04: binds every
    # write path that touches frontmatter). The prose stamp this replaced was
    # hand-corrected on sight and reverted on the next run, which cost agents
    # their only in-band evidence that a generator had produced the file.
    return f"{datetime.datetime.now():%Y-%m-%d}"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: regen-index.py <folder>", file=sys.stderr)
        return 1
    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        print(f"ERROR: not a folder: {folder}", file=sys.stderr)
        return 1
    index = folder / "index.md"

    # Hub guard: page frontmatter means authored hub, never a derived listing.
    if index.exists():
        fm = read_frontmatter(index)
        if "type" in fm or "status" in fm:
            print(f"REFUSED: {index} carries page frontmatter ({', '.join(sorted(set(fm) & {'type','title','status'}))}) — "
                  "authored bundle hub, never regenerated (hub law: wiki/projects/README.md).")
            return 2

    # Link form: wikilinks under the vault-wide uniqueness rule; markdown links
    # stay for folders inside a dot-folder (Obsidian never resolves those).
    root = find_vault_root(folder)
    try:
        folder_rel = folder.relative_to(root)
    except ValueError:
        folder_rel = Path(folder.name)
    in_dot = is_dot_path(folder_rel)
    md_stems, other_names = ({}, {}) if in_dot else stem_index(root)

    def link(name: str, title: str) -> str:
        wl = wikilink(folder_rel / name, title, md_stems, other_names, in_dot)
        return wl if wl is not None else f"[{title}]({name})"

    # Scan folder pages.
    pages = sorted(p for p in folder.iterdir()
                   if p.suffix == ".md" and p.name not in EXCLUDE and p.is_file())
    entries = {}
    for p in pages:
        fm = read_frontmatter(p)
        title = fm.get("title") or p.stem.replace("-", " ")
        desc = fm.get("description", "").strip()
        entries[p.name] = f"* {link(p.name, title)}" + (f" - {desc}" if desc else "")

    # Non-markdown stream items (PDFs, images): no frontmatter to pull, so they
    # list by filename. A filed source the index omits is unreachable from its
    # own stream, and the index is derived, so there is no hand-edit path.
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() != ".md" and not p.name.startswith("."):
            entries[p.name] = f"* {link(p.name, p.name)}"

    # Nested bundles: one entry per authored hub (same test as the guard).
    for sub in sorted(p for p in folder.iterdir() if p.is_dir()):
        hub = sub / "index.md"
        fm = read_frontmatter(hub) if hub.exists() else {}
        if "type" in fm or "status" in fm:
            rel = f"{sub.name}/index.md"
            title = fm.get("title") or sub.name.replace("-", " ")
            desc = fm.get("description", "").strip()
            entries[rel] = f"* {link(rel, title)}" + (f" - {desc}" if desc else "")

    # Parse existing index: title line, section order, entry -> section.
    # Accepts both the markdown form (pre-2026-08-17) and the wikilink form.
    h1 = f"# {folder.name.capitalize()}"
    sections: list[str] = []
    assignment: dict[str, str] = {}
    flat = True
    if index.exists():
        current = None
        seen_h1 = False
        for line in index.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                if not seen_h1:
                    h1 = line.rstrip()
                    seen_h1 = True
                else:
                    flat = False
                    current = line[2:].strip()
                    if current not in sections:
                        sections.append(current)
                continue
            m = ENTRY_RE.match(line)
            if m:
                assignment[m.group("path")] = current or ""
                continue
            m = WIKI_ENTRY_RE.match(line)
            if m:
                assignment[entry_key(m.group("target"), folder_rel, entries)] = current or ""

    new = [n for n in entries if n not in assignment]
    gone = [n for n in assignment if n not in entries]

    out = ["---", f"updated: {stamp()}", "---", h1, "",
           "Derived listing — regenerated by the pipeline, never hand-maintained.", ""]
    if flat:
        out += [entries[n] for n in sorted(entries)]
    else:
        for sec in sections:
            members = [n for n, s in assignment.items() if s == sec and n in entries]
            if not members and not any(assignment[g] == sec for g in gone):
                continue
            if members:
                out += [f"# {sec}", ""]
                out += [entries[n] for n in members]
                out += [""]
        if new:
            out += [f"# {NEW_SECTION}", ""]
            out += [entries[n] for n in sorted(new)]
            out += [""]
    if not entries:
        # A folder with no listable pages (e.g. the wiki/ root, whose index is an
        # authored directory of folder links) must never be overwritten with an
        # empty listing. Refuse and leave the file as it is. (Guard added
        # 2026-08-17 after a regen wiped wiki/index.md; restored from git.)
        print(f"REFUSED: {index} — folder has no listable pages; not overwriting an authored index")
        return
    index.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")

    print(f"REGENERATED: {index} ({len(entries)} entries)")
    if new:
        print("NEW (slot these into sections, or leave flat):")
        for n in sorted(new):
            print(f"  {n}")
    if gone:
        absent = sorted(n for n in gone if not (folder / n).exists())
        present = sorted(n for n in gone if (folder / n).exists())
        if absent:
            print("DROPPED (files no longer present):")
            for n in absent:
                print(f"  {n}")
        if present:
            print("DELISTED (still on disk, not indexable):")
            for n in present:
                print(f"  {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
