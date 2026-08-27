#!/usr/bin/env python3
"""regen-issues.py [vault-root] — regenerate ISSUES.md's open-issue list from disk.

The friction log's two derived surfaces have different shapes, so they have
different generators:
  - .state/issues/index.md (every issue, open and resolved) is an ordinary
    folder index: `regen-index.py .state/issues`;
  - ISSUES.md (open issues only, each row suffixed with its `rule:` and
    `opened:` values) is this script.

Everything from the top of ISSUES.md through the `## Open` heading is authored
rule text and is preserved byte for byte, except the `updated:` field, which is
restamped with today's bare date. Only the row list below `## Open` is written.

Reads frontmatter through regen-index.py's parser rather than a fresh one. Every
recorded transcription defect in this file's history came from an agent writing
its own frontmatter handling (a naive quote-strip truncated two `rule:` values
mid-sentence on 2026-08-11), so there is exactly one parser and this imports it.

Exit codes: 0 regenerated · 1 usage/error
"""
import datetime
import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REQUIRED = ("title", "status", "opened", "rule", "kind")

# Open rows are grouped by `kind` (ISSUES.md conventions define the vocabulary).
# Anything with a missing or unrecognized kind lands in the defect bucket, so a
# lazily filed issue degrades to the most attention-getting section, never hides.
SECTIONS = (
    ("decision", "On your desk"),
    ("defect", "Defects and other"),
    ("watch", "Watches accruing evidence"),
)


def _load_parser():
    """Import read_frontmatter from regen-index.py (hyphen blocks a plain import)."""
    path = SCRIPTS / "regen-index.py"
    spec = importlib.util.spec_from_file_location("regen_index", path)
    if spec is None or spec.loader is None:
        print(f"ERROR: cannot load {path}", file=sys.stderr)
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.read_frontmatter


def escape(text: str) -> str:
    """Square brackets in a title would terminate the markdown link text early."""
    return text.replace("[", r"\[").replace("]", r"\]")


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: regen-issues.py [vault-root]", file=sys.stderr)
        return 1
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else SCRIPTS.parent.parent
    issues_dir = root / ".state" / "issues"
    target = root / "ISSUES.md"
    if not issues_dir.is_dir():
        print(f"ERROR: not a folder: {issues_dir}", file=sys.stderr)
        return 1
    if not target.is_file():
        print(f"ERROR: not a file: {target}", file=sys.stderr)
        return 1

    read_frontmatter = _load_parser()

    # Preserve the authored header through "## Open"; restamp `updated:` only.
    header: list[str] = []
    found_open = False
    in_frontmatter = False
    for i, line in enumerate(target.read_text(encoding="utf-8").splitlines()):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
        elif in_frontmatter and line.strip() == "---":
            in_frontmatter = False
        elif in_frontmatter and line.startswith("updated:"):
            line = f"updated: {datetime.datetime.now():%Y-%m-%d}"
        header.append(line)
        if line.strip() == "## Open":
            found_open = True
            break
    if not found_open:
        print(f"ERROR: no '## Open' heading in {target}; refusing to guess where "
              "the authored header ends.", file=sys.stderr)
        return 1

    grouped: dict[str, list[str]] = {key: [] for key, _ in SECTIONS}
    warnings: list[str] = []
    counts = {"open": 0, "resolved": 0, "wontfix": 0, "other": 0}
    for p in sorted(issues_dir.glob("*.md")):
        if p.name in {"index.md", "README.md"}:
            continue
        fm = read_frontmatter(p)
        status = fm.get("status", "")
        counts[status if status in counts else "other"] += 1
        if status != "open":
            continue
        missing = [f for f in REQUIRED if not fm.get(f)]
        if missing:
            warnings.append(f"  {p.name}: missing {', '.join(missing)}")
        title = fm.get("title") or p.stem.replace("-", " ")
        row = f"* [{escape(title)}](.state/issues/{p.name})"
        suffix = ", ".join(x for x in (fm.get("rule"),
                                       f"opened {fm['opened']}" if fm.get("opened") else "")
                           if x)
        kind = fm.get("kind", "")
        bucket = kind if kind in grouped else "defect"
        grouped[bucket].append(f"{row} — {suffix}" if suffix else row)

    body: list[str] = []
    for key, heading in SECTIONS:
        body.append(f"\n### {heading} — {len(grouped[key])}\n")
        body.extend(grouped[key])

    target.write_text("\n".join(header + body) + "\n", encoding="utf-8")

    n_open = sum(len(v) for v in grouped.values())
    print(f"REGENERATED: {target} ({n_open} open: "
          + ", ".join(f"{len(grouped[k])} {k}" for k, _ in SECTIONS) + ")")
    print(f"  counted: {counts['open']} open, {counts['resolved']} resolved, "
          f"{counts['wontfix']} wontfix, {counts['other']} unrecognized status")
    if warnings:
        print("INCOMPLETE FRONTMATTER (row still written, fix the file):")
        for w in warnings:
            print(w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
