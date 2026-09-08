#!/usr/bin/env python3
"""vault_graph — compile the exocortex vault into a typed NetworkX graph and run lint/analysis queries.

Read-only over the vault. Pilot version: report to stdout. Writes nothing.

Usage: vault_graph.py [--vault PATH]   (default: the vault this script lives in)

Node id = path relative to vault root (e.g. "wiki/concepts/x.md").
Node kinds: wiki (parsed pages), source/note/other (link targets outside wiki/, added as stubs).
Edge kinds: body (markdown/wiki links in body). Every body link into wiki/ is a dependency edge.

Resolution (link convention approved 2026-08-17):
  body [[wikilink]]      stem match across the whole vault (non-dot folders, case-insensitive):
                         one hit -> "wikilink-name"; several -> "ambiguous-name(N)" (a finding);
                         none -> vault-relative path, with or without .md -> "wikilink-path";
                         else "dangling". A target containing "/" tries the path first.
  body [md](link)        file-relative, then vault-relative. No basename fallback. Else "dangling".

The frontmatter fields `sources:` and `depends_on:` were retired 2026-08-17: provenance and
dependencies now live as inline links in the body. A page still carrying either field is reported
under "Retired fields still present", not walked for edges.
"""

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

import networkx as nx
import yaml

# vault root = two levels up from this script (.claude/scripts/vault_graph.py); --vault overrides
VAULT = Path(__file__).resolve().parents[2]
WIKI = VAULT / "wiki"


def set_vault(root: Path):
    global VAULT, WIKI
    VAULT = root.resolve()
    WIKI = VAULT / "wiki"


FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)", re.S)
# markdown links [text](target) — skip images ![...], external URLs, anchors
MD_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def is_dot_rel(rel: Path) -> bool:
    return any(part.startswith(".") for part in rel.parts)


def scan_vault_files():
    """Every file under non-dot folders of the vault, as vault-relative posix paths."""
    out = []
    for p in VAULT.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(VAULT)
        if is_dot_rel(rel):
            continue
        out.append(rel.as_posix())
    return out


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


class Resolver:
    """Resolve a link/path string to a canonical vault-relative path."""

    def __init__(self, vault_files):
        # vault-wide maps for wikilinks: lower stem -> [rel] (.md files),
        # lower filename -> [rel] (non-md), lower rel path sans .md -> rel
        self.md_by_stem = defaultdict(list)
        self.other_by_name = defaultdict(list)
        self.by_relpath = {}
        for rel in vault_files:
            rp = Path(rel)
            self.by_relpath[rel.lower()] = rel
            if rp.suffix.lower() == ".md":
                self.md_by_stem[rp.stem.lower()].append(rel)
                self.by_relpath[rel[:-3].lower()] = rel
            else:
                self.other_by_name[rp.name.lower()].append(rel)

    def resolve_wikilink(self, raw: str):
        """[[name]] / [[name|alias]] / [[name#h]] (target already isolated by WIKILINK_RE)."""
        t = unquote(raw.strip())
        if not t:
            return None, "anchor-only"
        if t.startswith(("http://", "https://", "mailto:", "obsidian://")):
            return None, "external"
        t = t.rstrip("/") if t.endswith("/") and t.count("/") > 1 else t
        low = t.lower()

        def by_path():
            hit = self.by_relpath.get(low)
            if hit is None and low.endswith(".md"):
                hit = self.by_relpath.get(low[:-3])
            return hit

        if "/" in t:
            hit = by_path()
            if hit:
                return hit, "wikilink-path"
        name = Path(t).name
        stem = name[:-3] if name.lower().endswith(".md") else name
        hits = self.md_by_stem.get(stem.lower(), [])
        if not hits and Path(name).suffix:  # [[scan.pdf]]: non-md by full filename
            hits = self.other_by_name.get(name.lower(), [])
        if "/" not in t:
            if len(hits) == 1:
                return hits[0], "wikilink-name"
            if len(hits) > 1:
                # A bare name that exactly matches a vault-root file is already its
                # path-qualified form (the name and the path coincide there), and
                # Obsidian resolves it to the root file. Not a collision. (2026-09-04)
                root = [h for h in hits if "/" not in h]
                if len(root) == 1:
                    return root[0], "wikilink-root"
                return None, f"ambiguous-name({len(hits)})"
            hit = by_path()  # root-level file with an odd extension, etc.
            if hit:
                return hit, "wikilink-path"
        return None, "dangling"

    def resolve(self, raw: str, from_file: Path):
        r = raw.strip().strip('"')
        r = re.sub(r"^\[\[|\]\]$", "", r)  # tolerate wikilink syntax
        if r.startswith(("http://", "https://", "mailto:", "obsidian://")):
            return None, "external"
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
                if not p.is_relative_to(VAULT):
                    return None, "out-of-vault"
                return p.relative_to(VAULT).as_posix(), "file-relative"
            # 2. relative to vault root
            p = (VAULT / name).resolve()
            if p.exists() and p.is_file():
                if not p.is_relative_to(VAULT):
                    return None, "out-of-vault"
                return p.relative_to(VAULT).as_posix(), "vault-relative"
        return None, "dangling"


def build():
    G = nx.MultiDiGraph()
    wiki_pages = sorted(WIKI.rglob("*.md"))
    vault_files = scan_vault_files()
    resolver = Resolver(vault_files)
    problems = {
        "yaml_errors": [],       # (page, msg)
        "no_frontmatter": [],
        "dangling": [],          # (page, field, raw, why)
        "retired_fields": [],    # page paths still carrying sources:/depends_on:
        "body_kinds": Counter(), # resolved_via for body links -> count
        "vault_files": vault_files,
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
        if (fm.get("depends_on") or fm.get("sources")) and not rel.startswith(("wiki/log/", "wiki/chronicle/")):
            # dated records written before 2026-08-17 keep their fields as written
            problems["retired_fields"].append(rel)
        body_clean = INLINE_CODE_RE.sub("", CODE_FENCE_RE.sub("", body or ""))

        seen = set()
        body_links = [(raw, "md") for raw in MD_LINK_RE.findall(body_clean)] + \
                     [(raw, "wiki") for raw in WIKILINK_RE.findall(body_clean)]
        for raw, syntax in body_links:
            if syntax == "wiki":
                target, how = resolver.resolve_wikilink(raw)
            else:
                target, how = resolver.resolve(raw, path)
            problems["body_kinds"][how] += 1
            if target is None:
                if how not in ("external", "anchor-only", "folder"):
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

    P("## Retired fields still present (sources:/depends_on: removed 2026-08-17)")
    if not problems["retired_fields"]:
        P("  none")
    else:
        for rel in problems["retired_fields"]:
            P(f"  {rel}")

    P("\n## Parse problems")
    for rel, err in problems["yaml_errors"]:
        P(f"  YAML: {rel}: {err}")
    for rel in problems["no_frontmatter"]:
        P(f"  no frontmatter: {rel}")
    if not problems["yaml_errors"] and not problems["no_frontmatter"]:
        P("  none")

    P("\n## Body-link resolution inventory (how each body link resolved)")
    for how, c in sorted(problems["body_kinds"].items(), key=lambda x: -x[1]):
        P(f"  {c:5d}  {how}")

    P("\n## Dangling links")
    dangling_by_field = Counter(field for _, field, _, _ in problems["dangling"])
    if not problems["dangling"]:
        P("  none")
    else:
        P("  counts: " + ", ".join(f"{f}={c}" for f, c in sorted(dangling_by_field.items())))
    for rel, field, raw, why in problems["dangling"]:
        P(f"  {rel} [{field}] -> {raw!r} ({why})")

    P("\n## Basename collisions (wiki pages sharing a stem with any vault file)")
    # Under the wikilink convention a bare [[name]] only resolves when the stem is
    # unique across every non-dot folder. Each stem below forces path-qualified
    # links; a body [[name]] that hit one is listed as an ambiguous finding.
    by_stem = defaultdict(list)
    for rel in problems["vault_files"]:
        if rel.lower().endswith(".md"):
            by_stem[Path(rel).stem.lower()].append(rel)
    groups = {"wiki-vs-wiki": [], "wiki-vs-notes": [], "wiki-vs-other": []}
    for stem, paths in sorted(by_stem.items()):
        if len(paths) < 2 or not any(p.startswith("wiki/") for p in paths):
            continue
        zones = {p.split("/", 1)[0] for p in paths}
        if zones == {"wiki"}:
            groups["wiki-vs-wiki"].append((stem, paths))
        elif zones - {"wiki"} == {"notes"}:
            groups["wiki-vs-notes"].append((stem, paths))
        else:
            groups["wiki-vs-other"].append((stem, paths))
    for grp, items in groups.items():
        P(f"  {grp} ({len(items)})")
        for stem, paths in items:
            P(f"    {stem}: " + ", ".join(sorted(paths)))
    ambiguous_wl = [(rel, raw, why) for rel, field, raw, why in problems["dangling"]
                    if field == "body" and why.startswith("ambiguous-name")]
    P(f"  ambiguous body wikilinks (bare [[name]] hitting a collision): {len(ambiguous_wl)}")
    for rel, raw, why in ambiguous_wl:
        P(f"    {rel}  [[{raw}]]  ({why})")

    P("\n## Status-integrity")
    P("  verified pages ranked by distinct body-link targets (any body link into wiki/) whose status is draft/stale/disputed:")
    weak = Counter()
    for u, v, d in G.edges(data=True):
        if d["kind"] != "body" or not v.startswith("wiki/"):
            continue
        if G.nodes[u].get("status") == "verified" and G.nodes[v].get("status") in ("draft", "stale", "disputed"):
            weak[(u, v)] += 1
    per_page = Counter(u for (u, _v) in weak)
    n_verified = sum(1 for _n, d in wiki_nodes(G) if d.get("status") == "verified")
    P(f"    total: {sum(per_page.values())} weak targets across {len(per_page)} of {n_verified} verified pages")
    for u, c in per_page.most_common(20):
        P(f"    {c:4d}  {u}")
    if not per_page:
        P("    none")

    P("\n## Link cycles (wiki-internal body links; strongly connected components of size > 1)")
    # Body links are dense enough that enumerating simple cycles is exponential
    # (it hung on 2026-08-17). SCCs answer the same question in linear time:
    # every page in a component of size > 1 sits on at least one cycle. Report
    # only: cross-linking between wiki pages is normal, not a finding.
    dep = nx.DiGraph((u, v) for u, v, d in G.edges(data=True)
                      if d["kind"] == "body" and u.startswith("wiki/") and v.startswith("wiki/"))
    sccs = sorted((c for c in nx.strongly_connected_components(dep) if len(c) > 1), key=len, reverse=True)
    if sccs:
        P(f"  {len(sccs)} component(s); sizes: {', '.join(str(len(c)) for c in sccs[:10])}")
        for c in sccs:
            if len(c) <= 6:
                P(f"  {' <-> '.join(sorted(c))}")
    else:
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
        P("  (no incoming body links reference it)")

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
    ap = argparse.ArgumentParser(description="Read-only vault graph report (writes nothing).")
    ap.add_argument("--vault", default=None, help="vault root (default: the vault this script lives in)")
    args = ap.parse_args()
    if args.vault:
        set_vault(Path(args.vault))
    if not WIKI.is_dir():
        sys.exit(f"no wiki/ under {VAULT}")
    print(f"Vault: {VAULT}\n")
    G, problems = build()
    report(G, problems)
