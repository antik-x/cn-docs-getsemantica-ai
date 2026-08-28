#!/usr/bin/env python3
"""Structure verifier: compares source .md and target .mdx for translation conformance."""
import re, sys

def parse(path):
    txt = open(path, encoding='utf-8').read()
    lines = txt.split('\n')
    # extract frontmatter
    fm = None
    body_start = 0
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                fm = lines[1:i]
                body_start = i + 1
                break
    body = lines[body_start:]
    # fences: split body into (fence_content, prose) segments
    fences = []
    prose_lines = []
    in_fence = False
    cur = []
    fence_langs = []
    for ln in body:
        if re.match(r'^\s*```', ln):
            if not in_fence:
                in_fence = True
                cur = []
                m = re.match(r'^\s*```(.*)$', ln)
                fence_langs.append(m.group(1).strip())
            else:
                in_fence = False
                fences.append('\n'.join(cur))
            continue
        if in_fence:
            cur.append(ln)
        else:
            prose_lines.append(ln)
    return {'fm': fm, 'prose': prose_lines, 'fences': fences, 'fence_langs': fence_langs}

def analyze(d):
    prose = '\n'.join(d['prose'])
    res = {}
    res['h'] = {}
    for lvl in range(1, 5):
        res['h'][lvl] = sum(1 for ln in d['prose'] if re.match(r'^' + '#'*lvl + r' ', ln))
    res['fences'] = len(d['fences'])
    res['fence_langs'] = d['fence_langs']
    # list items (unordered -, *, ordered 1.)
    res['li_ul'] = sum(1 for ln in d['prose'] if re.match(r'^(\s*)[-*] ', ln))
    res['li_ol'] = sum(1 for ln in d['prose'] if re.match(r'^\s*\d+\. ', ln))
    # table lines
    res['table_lines'] = sum(1 for ln in d['prose'] if ln.strip().startswith('|'))
    # JSX tags
    res['jsx'] = re.findall(r'</?([A-Z][A-Za-z]+)', prose)
    # links: markdown [text](target)
    res['links'] = sorted(re.findall(r'\]\(([^)\s]+)\)', prose))
    res['anchors'] = sorted(re.findall(r'\]\(#([^)\s]+)\)', prose))
    # inline code count
    res['inline_code'] = len(re.findall(r'`[^`\n]+`', prose))
    # bare { or < in prose (excluding JSX tags and inline code)
    stripped = re.sub(r'`[^`\n]+`', '', prose)
    stripped = re.sub(r'</?[A-Za-z][^>\n]*>', '', stripped)
    res['bare_brace'] = stripped.count('{')
    res['bare_lt'] = len(re.findall(r'<[a-zA-Z/]', stripped))
    return res

def main(src, tgt):
    s, t = parse(src), parse(tgt)
    a, b = analyze(s), analyze(t)
    ok = True
    for lvl in range(1, 5):
        if a['h'][lvl] != b['h'][lvl]:
            print(f'MISMATCH H{lvl}: src={a["h"][lvl]} tgt={b["h"][lvl]}'); ok = False
    if a['fences'] != b['fences']:
        print(f'MISMATCH fences: src={a["fences"]} tgt={b["fences"]}'); ok = False
    for i, (fs, ft) in enumerate(zip(s['fences'], t['fences'])):
        if fs != ft:
            print(f'MISMATCH fence #{i+1} content'); ok = False
    if s['fence_langs'] != t['fence_langs']:
        print(f'MISMATCH fence langs:\n  src={s["fence_langs"]}\n  tgt={t["fence_langs"]}'); ok = False
    if a['li_ul'] != b['li_ul']:
        print(f'MISMATCH ul items: src={a["li_ul"]} tgt={b["li_ul"]}'); ok = False
    if a['li_ol'] != b['li_ol']:
        print(f'MISMATCH ol items: src={a["li_ol"]} tgt={b["li_ol"]}'); ok = False
    if a['table_lines'] != b['table_lines']:
        print(f'MISMATCH table lines: src={a["table_lines"]} tgt={b["table_lines"]}'); ok = False
    import collections
    if collections.Counter(a['jsx']) != collections.Counter(b['jsx']):
        print(f'MISMATCH JSX: src={collections.Counter(a["jsx"])} tgt={collections.Counter(b["jsx"])}'); ok = False
    if a['links'] != b['links']:
        print(f'MISMATCH links:\n  src={a["links"]}\n  tgt={b["links"]}'); ok = False
    # inline code multiset compare
    cs = sorted(re.findall(r'`([^`\n]+)`', '\n'.join(s['prose'])))
    ct = sorted(re.findall(r'`([^`\n]+)`', '\n'.join(t['prose'])))
    if cs != ct:
        from difflib import ndiff
        diff = [l for l in ndiff(cs, ct) if l[0] in '+-']
        print(f'INLINE CODE DIFF ({len(cs)} vs {len(ct)}):')
        for l in diff[:40]: print('  ' + l)
        ok = False
    if b['bare_brace'] or b['bare_lt']:
        print(f'MDX UNSAFE: bare {{ ={b["bare_brace"]}, bare < ={b["bare_lt"]}'); ok = False
    # frontmatter keys
    if s['fm'] and t['fm']:
        sk = [l.split(':')[0] for l in s['fm']]
        tk = [l.split(':')[0] for l in t['fm']]
        if sk != tk:
            print(f'MISMATCH fm keys: {sk} vs {tk}'); ok = False
    print(('OK ' if ok else 'FAIL ') + tgt)
    return ok

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
