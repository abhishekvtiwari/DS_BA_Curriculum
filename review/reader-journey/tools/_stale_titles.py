#!/usr/bin/env python3
"""Chapter citations whose title does not match the chapter file they point at.

    python review/_stale_titles.py            # whole manuscript
    python review/_stale_titles.py 30 31 34   # some chapters

Catches "Chapter 24, Forecasting" when ch24 is Requirements: a right number with a
wrong title, which a renumbering substitution leaves untouched.
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'manuscript')
STOP = {'the', 'and', 'with', 'for', 'from', 'your', 'you', 'data', 'chapter', 'bank', 'question', 'questions',
        'analysis', 'analytics', 'business', 'not', 'what', 'how', 'that', 'this', 'actually', 'need', 'first',
        'look', 'without', 'real', 'basics', 'track', 'track,', 'into', 'covers', 'takes', 'turns', 'uses', 'is',
        'shows', 'builds', 'has', 'where', 'when', 'goes', 'adds', 'applies', 'rebuilds', 'reads', 'explains'}

def titles():
    out = {}
    for p in glob.glob(os.path.join(MAN, 'ch*-*.md')):
        base = os.path.basename(p)
        num = re.match(r'ch(\d{2}[ab]?)-', base).group(1).lstrip('0').upper()
        h1 = open(p, encoding='utf-8').readline().strip()
        m = re.match(r'# Chapter \S+\s+(.*)', h1)
        out[num] = m.group(1) if m else h1
    return out

def words(s):
    return {w for w in re.findall(r"[A-Za-z][A-Za-z']+", s.lower()) if w not in STOP and len(w) > 2}

PAT_A = re.compile(r'Chapter (\d{1,2}[AB]?)[,:]\*{0,2} ([A-Z][^.;|\n*]{3,70}?)(?:[,.:;*(]|\s(?:is|are|has|was|covers|takes|turns|uses|shows|builds|puts|goes|adds|reads|does|and|which|where|for|on|to|in)\s)')
PAT_B = re.compile(r'(?:the |The )([A-Z][A-Za-z&,\' ]{4,60}?(?:[Bb]ank|[Cc]hapter|capstone))\s*\(Chapter (\d{1,2}[AB]?)\)')

def check(ch, T):
    p = glob.glob(os.path.join(MAN, 'ch%s-*.md' % (ch.zfill(2) if ch.isdigit() else ch.lower())))[0]
    md = open(p, encoding='utf-8').read()
    hits = []
    for m in PAT_A.finditer(md):
        num, cited = m.group(1).upper(), m.group(2).strip()
        if num == ch.upper() or num not in T:
            continue
        cw, tw = words(cited), words(T[num])
        if cw and not (cw & tw):
            hits.append((md.count('\n', 0, m.start()) + 1, num, cited, T[num]))
    for m in PAT_B.finditer(md):
        cited, num = m.group(1).strip(), m.group(2).upper()
        if num == ch.upper() or num not in T:
            continue
        cw, tw = words(cited), words(T[num])
        if cw and not (cw & tw):
            hits.append((md.count('\n', 0, m.start()) + 1, num, cited, T[num]))
    return hits

if __name__ == '__main__':
    T = titles()
    chs = sys.argv[1:] or sorted(T, key=lambda k: (int(re.sub(r'\D', '', k)), k))
    total = 0
    for ch in chs:
        for line, num, cited, actual in check(ch, T):
            total += 1
            print('ch%-4s line %-5d cites "Chapter %s, %s"  ->  actual: %s' % (ch, line, num, cited[:45], actual[:50]))
    print('%d stale citations' % total)
