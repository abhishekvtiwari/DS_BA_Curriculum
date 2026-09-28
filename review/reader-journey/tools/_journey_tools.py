#!/usr/bin/env python3
"""Fable A's scripted checks, run over any set of chapters.

    python review/_journey_tools.py 1 2 3 4 5 6 7 8 9

Three things the reading cannot do by hand across 855,000 words:

  1. The overwhelm profile: per chapter, words, key terms, bold terms, code
     blocks, figures, exercises, tools named, and the time the chapter claims.
  2. Every cross-reference to a chapter number, and which of them will point at
     the wrong chapter after the renumbering pass (chapter-map.md, issue 24).
  3. The first-appearance ledger: for every term a chapter puts in bold, the
     first chapter (in READING order) where the word is used in plain text.
     A term used before the chapter that bolds it is used before it is taught.

Reading order and the old-to-new map come from planning/chapter-map.md.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, 'manuscript')

# ---- reading order (chapter-map.md, top table) and the renumbering ---------
# Part II and III are read in this order; files keep their old numbers.
READING_ORDER = (['1', '2', '3', '4', '5', '6', '7', '8', '9']
                 + ['10', '11', '19', '12', '13', '17', '18', '14', '15', '16', '20']
                 + ['21', '22', '23', '24', '25', '26', '27']
                 + ['28', '34', '29', '32', '33', '30', '31']
                 + [str(n) for n in range(35, 73)] + ['72a', '73', '74', '75', '76a', '76b']
                 + [str(n) for n in range(77, 84)])
OLD_TO_NEW = {'19': 12, '12': 13, '13': 14, '17': 15, '18': 16, '14': 17, '15': 18, '16': 19,
              '34': 29, '29': 30, '32': 31, '33': 32, '30': 33, '31': 34,
              '72a': 73, '73': 74, '74': 75, '75': 76, '76a': 77, '76b': 78,
              '77': 79, '78': 80, '79': 81, '80': 82, '81': 83, '82': 84, '83': 85}


def path_of(ch):
    hits = glob.glob(os.path.join(MAN, 'ch%s-*.md' % ch.zfill(2) if ch.isdigit() else 'ch%s-*.md' % ch))
    return hits[0] if hits else None


def load(ch):
    p = path_of(ch)
    return open(p, encoding='utf-8').read() if p else ''


def prose(md):
    """Text a reader reads: no code blocks, no tables, no figure lines."""
    md = re.sub(r'^```.*?^```', ' ', md, flags=re.S | re.M)
    md = re.sub(r'^\|.*$', ' ', md, flags=re.M)
    md = re.sub(r'^!\[.*$', ' ', md, flags=re.M)
    return md


def section(md, head):
    m = re.search(r'^## %s.*?$(.*?)(?=^## |\Z)' % re.escape(head), md, re.S | re.M)
    return m.group(1) if m else ''


def glance(md, field):
    m = re.search(r'\*\*%s:\*\*\s*(.+?)$' % re.escape(field), md, re.M)
    return m.group(1).strip() if m else ''


# ---- 1. overwhelm profile -------------------------------------------------
def profile(ch):
    md = load(ch)
    if not md:
        return None
    body = md.split('## Answers to practice exercises')[0]
    key = section(md, 'Key terms')
    terms = [t.strip() for t in re.sub(r'\*\(.*?\)\*', '', key).replace('\n', ' ').split('·') if t.strip()]
    bold = set(t.lower() for t in re.findall(r'\*\*([A-Za-z][^*]{1,40})\*\*', prose(body)))
    ex = section(md, 'Practice exercises')
    return {
        'ch': ch, 'words': len(body.split()), 'key_terms': len(terms), 'bold': len(bold),
        'code': len(re.findall(r'^```', body, re.M)) // 2,
        'figures': len(re.findall(r'^!\[', body, re.M)),
        'exercises': len(re.findall(r'^\d+\.\s', ex, re.M)),
        'time': glance(md, 'Time needed'), 'tools': glance(md, 'Tools')[:70],
        'sections': len(re.findall(r'^## \d+\.\d+ ', md, re.M)),
    }


# ---- 2. cross-references that move at renumbering --------------------------
REF = re.compile(r'\b(Chapters?|section|Figure)\s+(\d{1,2})([a-b]?)(?:\.(\d+))?', re.I)
RANGE = re.compile(r'\bChapters\s+(\d{1,2})\s*[–-]\s*(\d{1,2})')


def moving_refs(ch):
    md = load(ch)
    out = []
    for m in RANGE.finditer(md):
        a, b = int(m.group(1)), int(m.group(2))
        inside = [str(n) for n in range(a, b + 1) if str(n) in OLD_TO_NEW]
        if inside:
            out.append((m.group(0), 'range spans renumbered chapters %s' % ','.join(inside)))
    for m in REF.finditer(md):
        kind, num, suf, sub = m.group(1), m.group(2), m.group(3).lower(), m.group(4)
        key = num + suf
        if key in OLD_TO_NEW and key != ch:
            out.append((m.group(0), 'old %s -> new %d' % (key, OLD_TO_NEW[key])))
    return out


# ---- 3. first-appearance ledger --------------------------------------------
LEDGER_STOP = {'you', 'exactly', 'people', 'questions', 'rules', 'form', 'file', 'files', 'size', 'number',
               'specific', 'steps', 'examples', 'text', 'desk', 'region', 'core', 'useful', 'key', 'due',
               'leading', 'timing', 'about to', 'the version', 'the website', 'must have', 'not needed',
               "what you'll do", 'a small example', 'pen and paper', 'estimate', 'judgment', 'skill',
               'study', 'project', 'projects', 'feedback', 'compound', 'chance', 'fact', 'opinion',
               'assumption', 'definition', 'report', 'share', 'points', 'rate', 'ratio', 'average', 'mean',
               'percentage', 'wholesale', 'revenue', 'invoice', 'collected', 'automation', 'a spreadsheet',
               'storage', 'databases', 'cloud', 'packets', 'pixels'}


def ledger(chapters):
    texts = {c: prose(load(c).split('## Answers to practice exercises')[0]) for c in chapters}
    order = [c for c in READING_ORDER if c in chapters]
    defined, used = {}, {}
    for c in order:
        for t in re.findall(r'\*\*([A-Za-z][A-Za-z0-9 /()\'-]{2,40})\*\*', texts[c]):
            t = re.sub(r'\s*\(.*?\)', '', t).strip().lower()
            if t.startswith(('chapter', 'appendix')) or t in LEDGER_STOP:
                continue
            if 2 < len(t) < 40 and t not in defined:
                defined[t] = c
    for t, dc in defined.items():
        pat = re.compile(r'\b%s\b' % re.escape(t), re.I)
        for c in order:
            plain = re.sub(r'\*\*[^*]+\*\*', ' ', texts[c])
            if pat.search(plain):
                used[t] = c
                break
    early = [(t, used[t], defined[t]) for t in defined if t in used
             and order.index(used[t]) < order.index(defined[t])]
    return defined, used, early


if __name__ == '__main__':
    chs = sys.argv[1:] or READING_ORDER[:9]
    print('=== overwhelm profile ===')
    print('%-4s %6s %5s %5s %4s %4s %4s %4s  %-22s %s' % ('ch', 'words', 'keys', 'bold', 'code', 'fig', 'exer', 'sect', 'time', 'tools'))
    for c in chs:
        p = profile(c)
        if p:
            print('%-4s %6d %5d %5d %4d %4d %4d %4d  %-22s %s' % (p['ch'], p['words'], p['key_terms'], p['bold'], p['code'],
                                                                 p['figures'], p['exercises'], p['sections'], p['time'][:22], p['tools']))
    print()
    print('=== references that point at the wrong chapter after renumbering ===')
    total = 0
    for c in chs:
        refs = moving_refs(c)
        total += len(refs)
        if refs:
            seen = {}
            for txt, why in refs:
                seen.setdefault((txt, why), 0)
                seen[(txt, why)] += 1
            print('ch %s: %d' % (c, len(refs)))
            for (txt, why), n in sorted(seen.items()):
                print('    %-24s %s%s' % (txt, why, '  x%d' % n if n > 1 else ''))
    print('total moving references in these chapters: %d' % total)
    print()
    print('=== first-appearance ledger: bold terms used in plain text BEFORE the chapter that bolds them ===')
    defined, used, early = ledger(chs)
    print('%d terms bolded across these chapters; %d used before defined' % (len(defined), len(early)))
    for t, u, d in sorted(early, key=lambda x: (READING_ORDER.index(x[1]), x[0])):
        print('    %-34s used ch %-3s  defined ch %s' % (t, u, d))
