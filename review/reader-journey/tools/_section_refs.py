#!/usr/bin/env python3
"""Every 'section X.Y' pointer in a chapter, next to the heading it actually lands on.

    python review/_section_refs.py 27 26 25 ...

A pointer is wrong when the heading it lands on is not the topic the sentence
promises. The script cannot judge that; it prints the sentence fragment and the
real heading side by side so a reader can, in one pass.
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'manuscript')

def path_of(ch):
    hits = glob.glob(os.path.join(MAN, 'ch%s-*.md' % (ch.zfill(2) if ch.isdigit() else ch)))
    return hits[0] if hits else None

def headings(ch):
    p = path_of(ch)
    if not p:
        return {}
    out = {}
    for m in re.finditer(r'^## (\d{1,2})\.(\d{1,2}) (.+)$', open(p, encoding='utf-8').read(), re.M):
        out[(m.group(1), m.group(2))] = m.group(3).strip()
    return out

REF = re.compile(r'(?:Chapter (\d{1,2})[,\s]+)?[Ss]ection (\d{1,2})\.(\d{1,2})')

def check(ch):
    md = open(path_of(ch), encoding='utf-8').read()
    body = md.split('## Answers to practice exercises')[0]
    rows = []
    for m in REF.finditer(body):
        tch, sch, sec = m.group(1), m.group(2), m.group(3)
        target = tch or sch
        if target != sch and tch:      # "Chapter 14 section 14.9": chapter and section agree?
            pass
        head = headings(sch).get((sch, sec), '<< no such section >>')
        ctx = body[max(0, m.start()-70):m.end()+40].replace('\n', ' ')
        if sch != ch.zfill(2).lstrip('0') and sch != ch:   # cross-chapter pointers only
            rows.append((sch, sec, head, ctx))
    return rows

if __name__ == '__main__':
    for ch in sys.argv[1:]:
        rows = check(ch)
        print('=== ch %s: %d section pointers ===' % (ch, len(rows)))
        seen = set()
        for sch, sec, head, ctx in rows:
            key = (sch, sec, ctx[-60:])
            if key in seen:
                continue
            seen.add(key)
            print('  -> %s.%-3s %-52s | ...%s' % (sch, sec, head[:52], ctx[-105:]))
