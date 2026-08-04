#!/usr/bin/env python3
"""vault_graph — compile the exocortex vault into a typed NetworkX graph and run lint/analysis queries.

Read-only over the vault. Pilot version: report to stdout.

Node id = path relative to vault root (e.g. "wiki/concepts/x.md").
Node kinds: wiki (parsed pages), source/note/other (link targets outside wiki/, added as stubs).
Edge kinds: depends_on, source (frontmatter sources:), body (markdown/wiki links in body).
"""

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

import networkx as nx
import yaml

# vault root = two levels up from this script (.claude/scripts/vault_graph.py)
VAULT = Path(__file__).resolve().parents[2]
WIKI = VAULT / "wiki"

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)", re.S)
# markdown links [text](target) — skip images ![...], external URLs, anchors
MD_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
CODE_FENCE_RE = re.compile(r"```.*?```", re.S)


def parse_file(path: Path):
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None, text, None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            return None, m.group(2), f"frontmatter is {type(fm).__name__}, not mapping"
        return fm, m.group(2), None
    except yaml.YAMLError as e:
        return None, m.group(2), f"YAML error: {str(e).splitlines()[0]}"


def classify_format(raw: str) -> str:
    """Which of the coexisting path formats is this entry written in?"""
    r = raw.strip().strip('"')
    if r.startswith("[["):
        return "wikilink"
    if r.startswith(("wiki/", "sources/", "notes/", "attachments/", "meta/")):
        return "vault-relative"
    if r.startswith(("./", "../")):
        return "file-relative"
    if "/" in r:
        return "subpath"  # e.g. projects/x.md — relative but with folders
    return "bare"


class Resolver:
    """Resolve a link/path string to a canonical vault-relative path."""

    def __init__(self, wiki_pages):
        self.by_base = defaultdict(list)
        for p in wiki_pages:
            self.by_base[p.name].append(p)

    def resolve(self, raw: str, from_file: Path):
        r = raw.strip().strip('"')
        r = re.sub(r"^\[\[|\]\]$", "", r)  # tolerate wikilink syntax
        if r.startswith(("http://", "https://", "mailto:", "obsidian://")):
            return None, "external"
        # provenance prose, not a path: "user confirmed in digest review, 2026-07-16"
        if ".md" not in r and not r.rstrip("/").endswith((".png", ".jpg", ".pdf", ".canvas")):
            if "/" not in r or " " in r.split("/")[0]:
                return None, "provenance-note"
        # strip trailing annotation: "notes/x.md (read 2026-07-17T19:00Z)"
        if ".md" in r:
            r = r[: r.index(".md") + 3]
        r = unquote(r.split("#")[0])
        if not r:
            return None, "anchor-only"
        # folder links like "concepts/" or "../projects/"
        if r.endswith("/"):
            for base in (from_file.parent, VAULT):
                if (base / r).resolve().is_dir():
                    return None, "folder"
        cand_names = [r] if r.endswith(".md") else [r + ".md", r]
        for name in cand_names:
            # 1. relative to the linking file's directory
            p = (from_file.parent / name).resolve()
            if p.exists() and p.is_file():
                return p.relative_to(VAULT).as_posix(), "file-relative"
            # 2. relative to vault root
            p = (VAULT / name).resolve()
            if p.exists() and p.is_file():
                return p.relative_to(VAULT).as_posix(), "vault-relative"
        # 3. unique basename match within wiki/
        base = Path(cand_names[0]).name
        hits = self.by_base.get(base, [])
        if len(hits) == 1:
            return hits[0].relative_to(VAULT).as_posix(), "basename-unique"
        if len(hits) > 1:
            return None, f"ambiguous-basename({len(hits)})"
        return None, "dangling"


def listify(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return [x for x in v if isinstance(x, str)]
    return []


def build():
    G = nx.MultiDiGraph()
    wiki_pages = sorted(WIKI.rglob("*.md"))
    resolver = Resolver(wiki_pages)
    problems = {
        "yaml_errors": [],       # (page, msg)
        "no_frontmatter": [],
        "dangling": [],          # (page, field, raw, why)
        "formats": Counter(),    # (field, format) -> count
    }

    for path in wiki_pages:
        rel = path.relative_to(VAULT).as_posix()
        fm, body, err = parse_file(path)
        exempt = path.name in ("index.md", "README.md", "log.md") or rel.startswith("wiki/log/")
        if err:
            problems["yaml_errors"].append((rel, err))
            fm = {}
        elif fm is None:
            # index/README/log pages are frontmatter-free by design (lint check 1's exemption)
            if not exempt:
                problems["no_frontmatter"].append(rel)
            fm = {}
        G.add_node(
            rel, kind="wiki",
            status=fm.get("status"), type=fm.get("type"),
            title=fm.get("title"), tags=fm.get("tags") or [],
            pending_review=fm.get("pending_review", False),
        )
        body_clean = CODE_FENCE_RE.sub("", body or "")

        for field, kind in (("depends_on", "depends_on"), ("sources", "source")):
            for raw in listify(fm.get(field)):
                problems["formats"][(field, classify_format(raw))] += 1
                target, how = resolver.resolve(raw, path)
                if target is None:
                    if how not in ("external", "provenance-note", "folder"):
                        problems["dangling"].append((rel, field, raw, how))
                    continue
                if not G.has_node(target):
                    G.add_node(target, kind=target.split("/")[0].rstrip("s") if not target.startswith("wiki/") else "wiki")
                G.add_edge(rel, target, kind=kind, raw=raw, resolved_via=how)

        seen = set()
        for raw in MD_LINK_RE.findall(body_clean) + WIKILINK_RE.findall(body_clean):
            target, how = resolver.resolve(raw, path)
            if target is None:
                if how not in ("external", "anchor-only", "provenance-note", "folder"):
                    problems["dangling"].append((rel, "body", raw, how))
                continue
            if target == rel or (rel, target) in seen:
                continue
            seen.add((rel, target))
            if not G.has_node(target):
                G.add_node(target, kind="wiki" if target.startswith("wiki/") else target.split("/")[0])
            G.add_edge(rel, target, kind="body", raw=raw, resolved_via=how)

    return G, problems


def wiki_nodes(G, exclude_meta=True):
    for n, d in G.nodes(data=True):
        if d.get("kind") != "wiki" or not n.startswith("wiki/"):
            continue
        if exclude_meta and (Path(n).name in ("index.md", "README.md", "log.md") or n.startswith("wiki/log/")):
            continue
        yield n, d


def report(G, problems):
    P = print
    n_wiki = sum(1 for _ in wiki_nodes(G, exclude_meta=False))
    kinds = Counter(d["kind"] for _, _, d in G.edges(data=True))
    P(f"# Vault graph report\n")
    P(f"Nodes: {G.number_of_nodes()} ({n_wiki} wiki pages, {G.number_of_nodes()-n_wiki} external stubs)")
    P(f"Edges: {G.number_of_edges()}  {dict(kinds)}\n")

    P("## Frontmatter edge-format inventory (migration recon)")
    for (field, fmt), c in sorted(problems["formats"].items()):
        P(f"  {field:11s} {fmt:15s} {c}")

    P("\n## Parse problems")
    for rel, err in problems["yaml_errors"]:
        P(f"  YAML: {rel}: {err}")
    for rel in problems["no_frontmatter"]:
        P(f"  no frontmatter: {rel}")
    if not problems["yaml_errors"] and not problems["no_frontmatter"]:
        P("  none")

    P("\n## Dangling links")
    if not problems["dangling"]:
        P("  none")
    for rel, field, raw, why in problems["dangling"]:
        P(f"  {rel} [{field}] -> {raw!r} ({why})")

    P("\n## Basename-fallback exposure (edges one filename collision from breaking)")
    # An edge written as a bare basename or an unrooted subpath resolves only
    # because exactly one file in wiki/ carries that name. Creating any second
    # file with the same basename anywhere in wiki/ silently kills it — which is
    # what happened on 2026-08-01 when a pattern hub took the name of the
    # concept page it enumerates, breaking three edges that had resolved since
    # 2026-07-16. This count is the population at risk; it is not an error list.
    fallback = Counter()
    by_target = Counter()
    for _u, v, d in G.edges(data=True):
        if d.get("resolved_via") == "basename-unique":
            fallback[d.get("kind", "?")] += 1
            by_target[Path(v).name] += 1
    total = sum(fallback.values())
    if not total:
        P("  none — every edge resolves by an explicit path")
    else:
        P(f"  {total} edges resolve by unique-basename fallback:")
        for kind, c in sorted(fallback.items(), key=lambda x: -x[1]):
            P(f"    {c:4d}  {kind}")
        P("  most-depended basenames (a new file with this name breaks all of them):")
        for name, c in by_target.most_common(8):
            P(f"    {c:4d}  {name}")
    ambiguous = [(rel, field, raw, why) for rel, field, raw, why in problems["dangling"]
                 if why.startswith("ambiguous-basename")]
    if ambiguous:
        P(f"  ALREADY BROKEN — {len(ambiguous)} edge(s) hit a basename collision:")
        for rel, field, raw, why in ambiguous:
            P(f"    {rel}  [{field}]  {raw}  ({why})")

    P("\n## Status-integrity: page depends_on a weaker-status page")
    rank = {"verified": 3, "draft": 2, "stale": 1, "disputed": 0, None: 2}
    hits = 0
    for u, v, d in G.edges(data=True):
        if d["kind"] != "depends_on":
            continue
        su, sv = G.nodes[u].get("status"), G.nodes[v].get("status")
        if sv in ("disputed", "stale") or (su == "verified" and rank.get(sv, 2) < 3):
            P(f"  {u} ({su}) -> {v} ({sv})")
            hits += 1
    if not hits:
        P("  none")

    P("\n## depends_on cycles")
    dep = nx.DiGraph((u, v) for u, v, d in G.edges(data=True) if d["kind"] == "depends_on")
    cycles = list(nx.simple_cycles(dep))
    for c in cycles:
        P(f"  {' -> '.join(c)}")
    if not cycles:
        P("  none")

    P("\n## Typed-graph orphans (content pages, no typed edges in or out, incl. body links)")
    orphans = [n for n, d in wiki_nodes(G) if G.degree(n) == 0]
    for n in orphans:
        P(f"  {n}")
    if not orphans:
        P("  none")

    P("\n## Hubs: top in-degree (wiki-internal edges only)")
    indeg = Counter()
    for u, v, d in G.edges(data=True):
        if v.startswith("wiki/") and u.startswith("wiki/"):
            indeg[v] += 1
    for n, c in indeg.most_common(12):
        st = G.nodes[n].get("status")
        P(f"  {c:3d}  {n}  [{st}]")

    P("\n## Promotion-shortlist heuristic: draft pages with high in-degree")
    for n, c in indeg.most_common(30):
        if G.nodes[n].get("status") == "draft" and c >= 4:
            P(f"  {c:3d}  {n}")

    P("\n## Retraction-walk demo: transitive dependents of decision-as-hypothesis.md")
    target = "wiki/concepts/decision-as-hypothesis.md"
    rdep = dep.reverse(copy=True)
    if target in rdep:
        deps = nx.descendants(rdep, target)
        P(f"  {len(deps)} pages transitively depend on it:")
        for n in sorted(deps):
            P(f"    {n}")
    else:
        P("  (no depends_on edges reference it)")

    P("\n## Communities (greedy modularity on undirected wiki-internal projection)")
    content = {n for n, _ in wiki_nodes(G)}  # excludes log/, index.md, README.md
    U = nx.Graph()
    for u, v, d in G.edges(data=True):
        if u in content and v in content:
            U.add_edge(u, v)
    comms = nx.community.greedy_modularity_communities(U)
    conn_pages = {n for n in U if n.startswith("wiki/connections/")}
    for i, com in enumerate(comms[:8]):
        has_conn = bool(com & conn_pages)
        sample = sorted(com, key=lambda n: -U.degree(n))[:4]
        P(f"  C{i} ({len(com)} pages, connections-page: {'yes' if has_conn else 'NO'}): " + ", ".join(Path(s).stem for s in sample))


if __name__ == "__main__":
    G, problems = build()
    report(G, problems)
