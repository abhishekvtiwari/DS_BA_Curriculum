"""Assemble Appendix A, the glossary, from the book's own words.

Every chapter ends with a Key terms line. For each term this finds the sentence in which the book
defines it, prefers the chapter that lists the term, and records where it was taught. Nothing is
written from outside the book: a term with no definition sentence anywhere is listed as needing
one rather than given an invented meaning.

68 chapters point at Appendix A and it does not exist, so every one of those references is
currently a dead end.

    python tools/notebooks/make_glossary.py              # writes manuscript/appendix-a-glossary.md
    python tools/notebooks/make_glossary.py --report     # coverage only, write nothing
"""
import argparse
import pathlib
import re
import sys
from collections import OrderedDict

ROOT = pathlib.Path(__file__).resolve().parents[2]
MS = ROOT / 'manuscript'
OUT = MS / 'appendix-a-glossary.md'

CH_NUM = re.compile(r'^ch(\d+)([a-z]?)')


def chapter_label(key):
    m = CH_NUM.match(key)
    if not m:
        return key
    return f"Chapter {int(m.group(1))}{m.group(2).upper()}"


def load():
    """{key: (label, text)} for every chapter, in reading order of the file names."""
    out = OrderedDict()
    for f in sorted(MS.glob('ch*.md')):
        key = f.name.split('-')[0]
        out[key] = (chapter_label(key), f.read_text(encoding='utf-8'))
    return out


def key_terms(text):
    m = re.search(r'^## Key terms\s*\n+(.+?)(?=\n##|\n---|\Z)', text, re.S | re.M)
    if not m:
        return []
    body = re.sub(r'\*\(All terms.*?\)\*', '', m.group(1), flags=re.S)
    terms = []
    for raw in re.split(r'·|\n', body):
        t = raw.strip().strip('*').strip()
        t = re.sub(r'\s*\((?:Chapter|Appendix)[^)]*\)\s*$', '', t).strip()
        if not t or len(t) > 70 or t.lower().startswith('all terms'):
            continue
        terms.append(t)
    return terms


def sentences_around(text, term):
    """Candidate defining sentences for a term, best first."""
    esc = re.escape(term)
    # the strongest signals, in order: "A **term** is ...", "**term** is/are/means ...",
    # "**term**: ...", then any sentence that bolds the term at all.
    pats = [
        rf'((?:[A-Z][^.\n]{{0,80}}?)?\*\*{esc}\*\*\s+(?:is|are|means|refers to)\b[^.\n]*\.)',
        rf'(\*\*{esc}\*\*\s*[:,—-]\s*[^.\n]*\.)',
        rf'([^.\n]*\b(?:called|known as)\s+\*\*{esc}\*\*[^.\n]*\.)',
        rf'([^.\n]*\*\*{esc}\*\*[^.\n]*\.)',
        rf'([^.\n]*`{esc}`[^.\n]*\b(?:is|are|means|returns|gives)\b[^.\n]*\.)',
    ]
    for p in pats:
        m = re.search(p, text, re.I)
        if m:
            s = re.sub(r'\s+', ' ', m.group(1)).strip()
            if 20 <= len(s) <= 420:
                return s
    return None


def tidy(s):
    """Markdown down to plain prose, keeping code spans."""
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    return s.strip()


def build():
    chapters = load()
    terms = OrderedDict()
    for key, (label, text) in chapters.items():
        for t in key_terms(text):
            low = t.lower()
            entry = terms.setdefault(low, {'label': t, 'chs': [], 'defn': None, 'from': None})
            entry['chs'].append(label)
    # find a definition: the term's own chapters first, then the whole book
    order = list(chapters.items())
    for low, e in terms.items():
        own = [k for k, (lab, _) in order if lab in e['chs']]
        for key in own + [k for k, _ in order if k not in own]:
            s = sentences_around(chapters[key][1], e['label'])
            if s:
                e['defn'] = tidy(s)
                e['from'] = chapters[key][0]
                break
    return terms


def write(terms):
    have = {k: v for k, v in terms.items() if v['defn']}
    missing = {k: v for k, v in terms.items() if not v['defn']}
    groups = OrderedDict()
    for low, e in sorted(terms.items(), key=lambda kv: kv[0]):
        first = e['label'][0].upper()
        groups.setdefault(first if first.isalpha() else '#', []).append(e)

    lines = [
        '# Appendix A. Glossary',
        '',
        f'Every term the book marks as a key term: **{len(terms):,}** of them, drawn from the Key '
        f'terms list at the end of each of the {len(set(c for e in terms.values() for c in e["chs"]))} '
        f'chapters.',
        '',
        'Each entry gives the book\'s own definition and the chapter that teaches it. Where a term '
        'is taught in more than one chapter, the first is the one that introduces it.',
        '',
        '---',
        '',
    ]
    for letter, items in groups.items():
        lines += [f'## {letter}', '']
        for e in items:
            chs = ', '.join(dict.fromkeys(e['chs']))
            if e['defn']:
                lines.append(f"**{e['label']}** — {e['defn']}  \n*{chs}*")
            else:
                lines.append(f"**{e['label']}** — *Definition to write.*  \n*{chs}*")
            lines.append('')
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return len(terms), len(have), len(missing)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    terms = build()
    have = sum(1 for e in terms.values() if e['defn'])
    print(f"key terms found: {len(terms):,}")
    print(f"with a definition taken from the book: {have:,} ({have/len(terms):.0%})")
    print(f"still needing one: {len(terms) - have:,}")
    if not a.report:
        total, h, m = write(terms)
        print(f"\nwrote {OUT.relative_to(ROOT)}: {total:,} entries, {m:,} marked as needing a definition")
    else:
        print("\nexamples:")
        for e in list(terms.values())[:6]:
            print(f"  {e['label']}: {(e['defn'] or '(none found)')[:100]}")
