#!/usr/bin/env python3
"""stranded-sources.py: list filed sources that no wiki page mentions.

Crash check for the inbox drain (skill: .claude/skills/process-inbox, pass 1).
Ingest files a source and ledgers its hash (.state/ingest-hashes.txt) before
it writes the wiki. A run that dies between those steps leaves a source
filed and ledgered but never synthesized, and nothing downstream notices.
This script lists every ledgered source whose basename appears nowhere under
wiki/ (wikilink, path, or plain mention). Those are the stranded ones.

Judgment stays with the agent: whether a hit is truly stranded, and finishing
its ingest. Read-only; never writes.

Exit codes: 0 none stranded · 2 stranded sources listed on stdout · 1 error
"""
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
LEDGER = VAULT / ".state" / "ingest-hashes.txt"
WIKI = VAULT / "wiki"


def main():
    if not LEDGER.exists():
        print(f"error: no ledger at {LEDGER}", file=sys.stderr)
        return 1
    paths = sorted({
        parts[1]
        for line in LEDGER.read_text().splitlines()
        if len(parts := line.split(None, 1)) == 2
    })
    text = "\n".join(
        p.read_text(errors="ignore") for p in WIKI.rglob("*.md")
    )
    stranded = [
        p for p in paths
        if (VAULT / p).exists() and Path(p).stem not in text
    ]
    for p in stranded:
        print(p)
    return 2 if stranded else 0


if __name__ == "__main__":
    sys.exit(main())
