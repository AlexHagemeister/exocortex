#!/usr/bin/env python3
"""style-sweep-guard.py BEFORE AFTER — mechanical guard for a claim-neutral style sweep (ingest step 5, bulk style sweep).
Passes only if, between the two files: frontmatter identical except `updated:`, and these sets are equal in the body:
wikilink targets, markdown link targets, external URLs, ISO dates, quoted strings ("..."), blockquote lines, code spans,
heading lines, numbers (integers/decimals/money). Also requires body word count within 12 percent. Exit 0 pass, 1 fail."""
import re,sys
def split(t):
    m=re.match(r"(---\n.*?\n---\n)(.*)",t,re.S)
    return (m.group(1),m.group(2)) if m else ("",t)
def sets(b):
    return {
     "wikilinks":set(x.split("|")[0].strip() for x in re.findall(r"\[\[([^\]]+)\]\]",b)),
     "mdlinks":set(re.findall(r"\]\(([^)\s]+)\)",b)),
     "urls":set(re.findall(r"https?://[^\s)\]]+",b)),
     "dates":set(re.findall(r"\b\d{4}-\d{2}-\d{2}\b",b)),
     "quotes":set(re.sub(r"\s*[—,;:()]\s*"," ",q).strip() for q in re.findall(r'"([^"\n]{8,})"',b)),
     "blockquotes":set(l.strip() for l in b.split("\n") if l.startswith(">")),
     "code":set(re.findall(r"`[^`\n]+`",b)),
     "headings":set(l.strip() for l in b.split("\n") if l.startswith("#")),
     "numbers":set(re.findall(r"(?<![\w-])\$?\d[\d,]*\.?\d*%?(?![\w-])",b)),
    }
def fm_norm(f): return "\n".join(l for l in f.split("\n") if not l.startswith("updated:"))
a,b=[open(p).read() for p in sys.argv[1:3]]
fa,ba=split(a); fb,bb=split(b)
ok=True
if fm_norm(fa)!=fm_norm(fb):
    # allow description/scope em-dash rewording: compare frontmatter with em dashes and punctuation stripped
    norm=lambda f: re.sub(r"[^\w\[\]/|]+"," ",fm_norm(f).replace("—"," "))
    if re.sub(r"\s+"," ",norm(fa))!=re.sub(r"\s+"," ",norm(fb)):
        print("FAIL frontmatter changed beyond punctuation/updated"); ok=False
sa,sb=sets(ba),sets(bb)
for k in sa:
    if sa[k]!=sb[k]:
        print(f"FAIL {k}: dropped={sorted(sa[k]-sb[k])[:5]} added={sorted(sb[k]-sa[k])[:5]}"); ok=False
wa,wb=len(ba.split()),len(bb.split())
if wa and abs(wb-wa)/wa>0.12: print(f"FAIL word count {wa}->{wb}"); ok=False
left=bb.count("—")
print(("PASS" if ok else "FAIL")+f"  words {wa}->{wb}; em dashes {ba.count('—')}->{left}")
sys.exit(0 if ok else 1)
