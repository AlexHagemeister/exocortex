#!/usr/bin/env python3
"""compaction-guard.py — mechanical half of the compaction guard (ingest step 5).

Compares a wiki page before and after a compaction or fold and refuses the
rewrite when anything the vault treats as provenance changed:

  - frontmatter must be identical, except `updated:` (any change) and, at a
    fold, `pending_review:` (may clear) and `verified_at:` (the fold is a
    review act). Pass --fold to allow the latter two. At a fold the receipt
    check also relaxes from verbatim sentences to the set of review dates
    those sentences name, because the folded annex headings carry the
    confirmation receipt and dissolve into prose.
  - the sets of wikilink targets, external URLs, ISO dates (YYYY-MM-DD), and
    receipt sentences in the body must be EQUAL between before and after.
    Additions fail as well as drops: an added citation or date is a claim the
    old page did not carry (the smuggling direction). The one allowed addition
    is the compaction receipt sentence the rewrite itself appends, whose date
    and day-log link are excepted.

This is the mechanical guard only. It cannot see meaning; a rewrite that keeps
every link and date and still changes a claim passes here. The semantic guard
(a second agent tracing every claim both ways) is the other half and is
required alongside this one. Neither proves neutrality; together with git and
audit sampling they make a bad rewrite detectable rather than silent.

Usage:
  compaction-guard.py BEFORE AFTER [--fold] [--json]
Exit 0 = pass, 1 = fail, 2 = usage. Prints a report either way.
"""
import argparse
import json
import re
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")
DATE_RE = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
RECEIPT_MARKERS = (
    "digest review",
    "page review",
    "audit review",
    "Verified by Alex",
    "Verified at birth",
    "user confirmed",
    "confirmed by Alex",
    "Compacted ",
)
COMPACTION_RECEIPT_RE = re.compile(r"Compacted (20\d\d-\d\d-\d\d)[^.]*\.")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def split(text: str):
    """Return (frontmatter_lines, body). Frontmatter excludes the --- fences."""
    if not text.startswith("---\n"):
        return [], text
    end = text.find("\n---", 4)
    if end == -1:
        return [], text
    fm = text[4:end].splitlines()
    body = text[end + 4:]
    if body.startswith("\n"):
        body = body[1:]
    return fm, body


def fm_dict(lines):
    """Top-level key -> full text of that key's block (value + continuation lines)."""
    out, key = {}, None
    for ln in lines:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$", ln)
        if m:
            key = m.group(1)
            out[key] = m.group(2).strip()
        elif key is not None:
            out[key] += "\n" + ln
    return out


def receipts(body: str):
    found = set()
    for para in body.split("\n"):
        for s in SENTENCE_SPLIT_RE.split(para.strip()):
            if any(mk in s for mk in RECEIPT_MARKERS) and DATE_RE.search(s):
                found.add(s.strip())
    return found


def inventory(body: str):
    return {
        "wikilinks": {t.strip().rstrip("/") for t in WIKILINK_RE.findall(body)},
        "urls": set(URL_RE.findall(body)),
        "dates": set(DATE_RE.findall(body)),
        "receipts": receipts(body),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--fold", action="store_true",
                    help="allow pending_review: to change (fold on confirmation)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    bt = Path(a.before).read_text(encoding="utf-8")
    at = Path(a.after).read_text(encoding="utf-8")
    bfm, bbody = split(bt)
    afm, abody = split(at)

    failures, notes = [], []

    # frontmatter
    bd, ad = fm_dict(bfm), fm_dict(afm)
    allowed = {"updated"} | ({"pending_review", "verified_at"} if a.fold else set())
    for k in sorted(set(bd) | set(ad)):
        if k in allowed:
            continue
        if bd.get(k) != ad.get(k):
            failures.append(f"frontmatter `{k}:` changed")
    if bfm and [ln.split(":")[0] for ln in bfm if re.match(r"^[A-Za-z_]", ln)] != \
            [ln.split(":")[0] for ln in afm if re.match(r"^[A-Za-z_]", ln)]:
        # key order or key set changed beyond allowed
        bkeys = [ln.split(":")[0] for ln in bfm if re.match(r"^[A-Za-z_]", ln)]
        akeys = [ln.split(":")[0] for ln in afm if re.match(r"^[A-Za-z_]", ln)]
        if [k for k in bkeys if k not in allowed] != [k for k in akeys if k not in allowed]:
            failures.append("frontmatter key set or order changed")

    # body inventories
    bi, ai = inventory(bbody), inventory(abody)

    # except the compaction receipt the rewrite appends
    new_receipts = ai["receipts"] - bi["receipts"]
    comp = [r for r in new_receipts if COMPACTION_RECEIPT_RE.search(r)]
    if len(comp) > 1:
        failures.append("more than one new compaction receipt")
    excepted_dates, excepted_links = set(), set()
    for r in comp:
        excepted_dates |= set(DATE_RE.findall(r))
        excepted_links |= {t.strip() for t in WIKILINK_RE.findall(r)}
        ai["receipts"].discard(r)
        notes.append(f"compaction receipt accepted: {r}")

    for kind in ("wikilinks", "urls", "dates", "receipts"):
        b, n = bi[kind], ai[kind]
        if kind == "dates":
            n = n - (excepted_dates - b)
        if kind == "wikilinks":
            n = n - (excepted_links - b)
        if kind == "receipts" and a.fold:
            # At a fold the annex headings that carried the confirmation
            # ("... merge confirmed in digest review, 2026-07-24") dissolve into
            # prose, so verbatim equality cannot hold. Compare the set of review
            # dates the receipt sentences name instead: no review event may be
            # lost or invented.
            b = {d for s in b for d in DATE_RE.findall(s)}
            n = {d for s in n for d in DATE_RE.findall(s)}
            notes.append("fold: receipts compared by review date, not verbatim")
        dropped, added = sorted(b - n), sorted(n - b)
        for d in dropped:
            failures.append(f"{kind} dropped: {d}")
        for x in added:
            failures.append(f"{kind} added: {x}")

    report = {
        "pass": not failures,
        "failures": failures,
        "notes": notes,
        "counts_before": {k: len(v) for k, v in bi.items()},
        "counts_after": {k: len(v) for k, v in ai.items()},
        "words_before": len(bbody.split()),
        "words_after": len(abody.split()),
    }
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        print("PASS" if report["pass"] else "FAIL")
        for f in failures:
            print("  -", f)
        for n in notes:
            print("  note:", n)
        print(f"  words {report['words_before']} -> {report['words_after']}; "
              + "; ".join(f"{k} {report['counts_before'][k]}->{report['counts_after'][k]}"
                          for k in bi))
    sys.exit(0 if report["pass"] else 1)


if __name__ == "__main__":
    main()
