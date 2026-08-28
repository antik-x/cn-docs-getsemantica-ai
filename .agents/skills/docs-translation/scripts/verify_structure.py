#!/usr/bin/env python3
"""Structural parity verifier: each source page vs its translated counterpart.

Checks per pair, per the translation rules:
  - frontmatter key sets match
  - heading lines per level match (outside code fences)
  - fenced code blocks: count AND byte-identical content sequence
  - list item counts (ordered/unordered) match (outside fences)
  - table line counts match (outside fences)
  - JSX component tag counts match
  - link targets (markdown links + <img src>) match as ordered lists
  - inline code span counts match

Defaults come from project.json in the skill root directory (parent of
this scripts/ directory); override via env:
  SRC_DIR   directory of source pages   (default <source_cache>/<upstream.docs_dir>)
  DST_DIR   directory of translated pages (default <site_root>)
  PAIRS_FILE  src/dst pair list          (default <pairs>)

Usage: python3 verify_structure.py
Exit code 0 = all green; prints a per-file report.
"""
import os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))  # <skill>/scripts
SKILL_DIR = os.path.dirname(HERE)  # skill root, holds project.json
try:
    CFG = json.load(open(os.path.join(SKILL_DIR, "project.json"), encoding="utf-8"))
except FileNotFoundError:
    CFG = {}
UP = CFG.get("upstream", {})
SRC = os.environ.get("SRC_DIR") or os.path.join(
    CFG.get("source_cache", "/tmp/upstream-src"), UP.get("docs_dir", "docs")
)
DST = os.environ.get("DST_DIR") or os.path.normpath(os.path.join(SKILL_DIR, CFG.get("site_root", "../../..")))
BATCHES = os.environ.get("PAIRS_FILE") or os.path.join(SKILL_DIR, CFG.get("pairs", "state/batches.json"))

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+")
LIST_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
JSX_RE = re.compile(r"<(/?)([A-Z][A-Za-z]+)")
MDLINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMGSRC_RE = re.compile(r"<img[^>]*src=\"([^\"]+)\"")
CODESPAN_RE = re.compile(r"(?<!`)(`+)(?!`)")


def split_fences(text):
    """Return (text_without_fence_lines, [fence_contents_byte_exact])."""
    out, fences, in_fence, closer = [], [], False, None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if not in_fence and m:
            in_fence, closer = True, m.group(2)[0] * len(m.group(2))
            fences.append([])
            continue
        if in_fence:
            if m and m.group(2)[0] == closer[0] and len(m.group(2)) >= len(closer):
                in_fence = False
                continue
            fences[-1].append(line)
            continue
        out.append(line)
    return "\n".join(out), ["\n".join(f) for f in fences]


def frontmatter(text):
    if not text.startswith("---"):
        return set(), text
    end = text.find("\n---", 3)
    if end < 0:
        return set(), text
    fm = text[3:end]
    keys = set(re.findall(r"^([A-Za-z_-]+):", fm, re.M))
    return keys, text[end + 4:]


def analyze(text):
    keys, body = frontmatter(text)
    nofence, fences = split_fences(body)
    headings = {}
    for line in nofence.split("\n"):
        m = HEADING_RE.match(line)
        if m:
            headings[len(m.group(1))] = headings.get(len(m.group(1)), 0) + 1
    lists_u = lists_o = 0
    for line in nofence.split("\n"):
        m = LIST_RE.match(line)
        if m:
            if m.group(1) in "-*+":
                lists_u += 1
            else:
                lists_o += 1
    tables = sum(1 for line in nofence.split("\n") if TABLE_RE.match(line))
    jsx = {}
    for m in JSX_RE.finditer(nofence):
        jsx[m.group(2)] = jsx.get(m.group(2), 0) + 1
    links = MDLINK_RE.findall(nofence) + IMGSRC_RE.findall(nofence)
    codespans = len(CODESPAN_RE.findall(nofence))
    return {
        "fm_keys": keys, "headings": headings, "fences": fences,
        "lists_u": lists_u, "lists_o": lists_o, "tables": tables,
        "jsx": jsx, "links": links, "codespans": codespans,
    }


def main():
    pairs = []
    for b, files in json.load(open(BATCHES)).items():
        for f in files:
            pairs.append((f["src"], f["dst"]))
    bad = 0
    for src_rel, dst_rel in pairs:
        sp = os.path.join(SRC, src_rel)
        dp = os.path.join(DST, dst_rel)
        label = dst_rel
        if not os.path.exists(dp):
            print(f"MISSING  {label}")
            bad += 1
            continue
        a = analyze(open(sp, encoding="utf-8").read())
        b = analyze(open(dp, encoding="utf-8").read())
        issues = []
        if a["fm_keys"] != b["fm_keys"]:
            issues.append(f"frontmatter keys {sorted(a['fm_keys'])} != {sorted(b['fm_keys'])}")
        if a["headings"] != b["headings"]:
            issues.append(f"headings {a['headings']} != {b['headings']}")
        if len(a["fences"]) != len(b["fences"]):
            issues.append(f"fence count {len(a['fences'])} != {len(b['fences'])}")
        else:
            for i, (fa, fb) in enumerate(zip(a["fences"], b["fences"])):
                if fa != fb:
                    issues.append(f"fence #{i+1} content differs")
                    break
        if (a["lists_u"], a["lists_o"]) != (b["lists_u"], b["lists_o"]):
            issues.append(f"lists u:{a['lists_u']}/{b['lists_u']} o:{a['lists_o']}/{b['lists_o']}")
        if a["tables"] != b["tables"]:
            issues.append(f"table lines {a['tables']} != {b['tables']}")
        if a["jsx"] != b["jsx"]:
            diff = {k: (a["jsx"].get(k, 0), b["jsx"].get(k, 0))
                    for k in set(a["jsx"]) | set(b["jsx"])
                    if a["jsx"].get(k, 0) != b["jsx"].get(k, 0)}
            issues.append(f"jsx tags src/dst {diff}")
        if a["links"] != b["links"]:
            sa, sb = set(a["links"]), set(b["links"])
            issues.append(f"links differ; src-only={sorted(sa-sb)[:4]} dst-only={sorted(sb-sa)[:4]}")
        if a["codespans"] != b["codespans"]:
            issues.append(f"inline code spans {a['codespans']} != {b['codespans']}")
        if issues:
            bad += 1
            print(f"FAIL     {label}")
            for it in issues:
                print(f"         - {it}")
        else:
            print(f"OK       {label}")
    print(f"\n{len(pairs)-bad}/{len(pairs)} pairs pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
