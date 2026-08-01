#!/usr/bin/env python3
"""notes-cursor-diff.py [--write] — diff notes/ against the sweep cursor.

Mechanical half of the notes sweep (skill: .claude/skills/process-inbox,
pass 2): walk notes/, hash, compare to .state/notes-cursor.txt, and report
NEW / CHANGED / DELETED / EVICTED / CONFLICT / NO-INGEST. With --write,
rewrite the cursor (unchanged entries keep their read timestamps; new and
changed entries get now; deleted entries drop; evicted entries persist).

Judgment stays with the agent: what to ingest, the per-run cap, recording
deletions in .state/deleted-notes.txt (this script never writes that file —
the mass-deletion guard is the agent's call), and all frontmatter write-back.

Exit codes: 0 ok · 1 error · 3 mass-deletion warning (report, don't record)
"""
import datetime
import hashlib
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
NOTES = VAULT / "notes"
CURSOR = VAULT / ".state" / "notes-cursor.txt"

OS_JUNK = {".DS_Store", "Thumbs.db", "desktop.ini"}
CONFLICT_RE = re.compile(r"(conflicted copy|Conflicted Copy)", re.I)
DUP_SUFFIX_RE = re.compile(r"^(.*) \d+(\.[^.]+)$")
NO_INGEST_RE = re.compile(r"#no-ingest\b|(^tags:.*no-ingest)", re.M)


def is_conflict(p: Path) -> bool:
    if CONFLICT_RE.search(p.name):
        return True
    m = DUP_SUFFIX_RE.match(p.name)
    return bool(m and (p.parent / (m.group(1) + m.group(2))).exists())


def main() -> int:
    write = "--write" in sys.argv[1:]
    if not NOTES.is_dir():
        print(f"ERROR: no notes/ at {NOTES}", file=sys.stderr)
        return 1

    cursor: dict[str, tuple[str, str]] = {}  # relpath -> (hash, timestamp)
    if CURSOR.exists():
        for line in CURSOR.read_text(encoding="utf-8").splitlines():
            parts = line.split("  ", 2)
            if len(parts) == 3:
                cursor[parts[2]] = (parts[0], parts[1])

    seen, evicted, conflicts, no_ingest = {}, [], [], []
    for p in sorted(NOTES.rglob("*")):
        if not p.is_file() or p.name in OS_JUNK:
            continue
        rel = str(p.relative_to(NOTES))
        if rel == "index.md":
            continue  # the derived index is invisible to the sweep
        if p.name.startswith(".") and p.suffix == ".icloud":
            evicted.append(rel)
            continue
        if is_conflict(p):
            conflicts.append(rel)
            continue
        data = p.read_bytes()
        if NO_INGEST_RE.search(data.decode("utf-8", errors="replace")):
            no_ingest.append(rel)
            continue
        seen[rel] = hashlib.sha256(data).hexdigest()

    def unevicted(rel: str) -> str:
        p = Path(rel)
        return str(p.parent / p.name[1:-len(".icloud")]) if str(p.parent) != "." \
            else p.name[1:-len(".icloud")]

    evicted_known = {unevicted(e): e for e in evicted}
    new = [r for r in seen if r not in cursor]
    changed = [r for r in seen if r in cursor and cursor[r][0] != seen[r]]
    deleted = [r for r in cursor
               if r not in seen and r not in evicted_known
               and r not in no_ingest and r not in conflicts]

    for label, items in [("NEW", new), ("CHANGED", changed), ("DELETED", deleted),
                         ("EVICTED", evicted), ("CONFLICT", conflicts),
                         ("NO-INGEST", no_ingest)]:
        print(f"{label} ({len(items)}):")
        for r in items:
            print(f"  {r}")

    warn = len(cursor) > 0 and len(deleted) > 5 and len(deleted) / len(cursor) > 0.2
    if warn:
        print("\nWARNING: large share of the cursor reads as deleted — almost certainly "
              "a bugged walk, not real deletions. Stop and report; do not record "
              "these in deleted-notes.txt (process-inbox pass 2, step 6).")

    if write:
        now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        lines = []
        for rel, h in seen.items():
            ts = now if rel in new or rel in changed else cursor[rel][1]
            lines.append(f"{h}  {ts}  {rel}")
        for stem, _ in evicted_known.items():  # evicted = present, keep prior entry
            if stem in cursor:
                h, ts = cursor[stem]
                lines.append(f"{h}  {ts}  {stem}")
        CURSOR.parent.mkdir(exist_ok=True)
        CURSOR.write_text("\n".join(sorted(lines, key=lambda l: l.split("  ", 2)[2])) + "\n",
                          encoding="utf-8")
        print(f"\nCURSOR REWRITTEN: {len(lines)} entries")

    return 3 if warn else 0


if __name__ == "__main__":
    sys.exit(main())
