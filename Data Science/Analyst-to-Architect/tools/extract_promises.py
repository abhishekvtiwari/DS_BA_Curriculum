#!/usr/bin/env python3
"""extract_promises.py - list every forward reference ("Chapter N ...") that written chapters make to other chapters.
Usage: python3 extract_promises.py manuscript/ch*.md > promises.md
Chapters being written must deliver what earlier chapters promised about them."""
import re, sys, collections
prom = collections.defaultdict(list)
for path in sys.argv[1:]:
    md = open(path, encoding='utf-8').read()
    me = int(re.search(r'# Chapter (\d+)\.', md).group(1))
    md_nocode = re.sub(r'^```.*?^```$', '', md, flags=re.S | re.M)
    sentences = []
    for line in md_nocode.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        sentences += re.split(r'(?<=[.!?])\s+(?=[A-Z*"(])', line)
    for s in sentences:
        nums = set()
        for m in re.finditer(r'Chapters? ((?:\d+)(?:\s*(?:,|and|–|-|or)\s*\d+)*)', s):
            for n in re.findall(r'\d+', m.group(1)): nums.add(int(n))
        for m in re.finditer(r'\bCh (\d+)\b', s): nums.add(int(m.group(1)))
        for m in re.finditer(r'Appendix ([A-H])\b', s): nums.add(m.group(1))
        for n in nums:
            if n != me:
                clean = s.strip().lstrip('>-* ').replace('**', '')
                prom[n].append((me, clean[:400]))
def key(k): return (0, k) if isinstance(k, int) else (1, k)
for n in sorted(prom, key=key):
    label = f'Chapter {n}' if isinstance(n, int) else f'Appendix {n}'
    print(f'\n### {label}\n')
    seen = set()
    for src, s in prom[n]:
        if (src, s) in seen: continue
        seen.add((src, s)); print(f'- *(from Ch {src})* {s}')
