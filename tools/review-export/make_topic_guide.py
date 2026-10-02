"""Build the topic guide: where every subject in the book is taught, and what you practise it with.

Everything here is read out of the manuscript and the companion folder. Nothing is typed in by
hand, so the guide cannot drift from the book: rebuild it after any change and it is current.

It writes one Markdown file, which `export_section.py` then renders to DOCX and PDF, and an Excel
workbook with the same content in sortable sheets.

    python tools/review-export/make_topic_guide.py <out.md> [out.xlsx]
"""
import collections
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[2]
BOOK = ROOT / 'Data Science' / 'Analyst-to-Architect'
MS = BOOK / 'manuscript'
COMP = BOOK / 'companion'

# Which book each part ends up in, from tools/pdf/books.py.
BOOK_OF_PART = {
    'front': '1 · Theory', '0': '1 · Theory', '1': '1 · Theory',
    '2': '2 · Practical', '3': '2 · Practical',
    '4': '3 · Implementation', '5': '3 · Implementation',
    '6': '3 · Implementation', '7': '3 · Implementation',
    '8': '4 · Be Interview Ready',
    'closing': '3 · Implementation',   # Ch 83 is marked *Closing*, and books.py puts it in Book 3
}
PART_TITLES = {
    '0': 'Part 0 — First Principles: Data from Zero',
    '1': 'Part 1 — The Map',
    '2': 'Part 2 — The Analyst',
    '3': 'Part 3 — Advanced Analytics & Analytics Engineering',
    '4': 'Part 4 — Machine Learning',
    '5': 'Part 5 — Data Engineering',
    '6': 'Part 6 — Production ML & Generative AI',
    '7': 'Part 7 — Architecture & Leadership',
    '8': 'Part 8 — Be Interview Ready',
    'closing': 'Closing',
}


def chapter_key(p):
    m = re.match(r'ch(\d+)([a-z]?)', p.name)
    return int(m.group(1)), m.group(2)


def field(text, name):
    """Pull one '> **Name:** ...' line out of the at-a-glance block."""
    m = re.search(r'\*\*' + re.escape(name) + r'\*\*(.+?)(?=\n>\s*\n|\n\n)', text[:6000], re.S)
    if not m:
        return ''
    v = re.sub(r'\n>\s?', ' ', m.group(1)).strip()
    return re.sub(r'\s+', ' ', v)


def strip_md(s):
    s = re.sub(r'`([^`]*)`', r'\1', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'\1', s)
    return s.strip()


def key_terms(text):
    """The Key terms list, split on the book's own middle-dot separator."""
    m = re.search(r'^## Key terms\s*\n(.+?)(?=\n## |\Z)', text, re.S | re.M)
    if not m:
        return []
    body = re.sub(r'\n+', ' ', m.group(1)).strip()
    terms = [strip_md(t) for t in body.split('·')]
    return [t for t in terms if t and len(t) < 70]


def practice_for(key):
    """What is in companion/<key>/, summarised by kind."""
    d = COMP / key
    if not d.is_dir():
        return {}
    out = collections.Counter()
    names = {}
    for f in sorted(d.rglob('*')):
        if not f.is_file() or '.git' in f.parts or '__pycache__' in f.parts:
            continue
        ext = f.suffix.lower().lstrip('.')
        kind = {'ipynb': 'notebook', 'sql': 'SQL', 'py': 'Python script',
                'csv': 'dataset (csv)', 'parquet': 'dataset (parquet)',
                'xlsx': 'Excel workbook', 'json': 'data (json)', 'md': 'notes',
                'yml': 'config', 'txt': 'text'}.get(ext)
        if not kind:
            continue
        out[kind] += 1
        names.setdefault(kind, []).append(f.name)
    return {'counts': out, 'names': names}


def collect():
    rows = []
    for p in sorted(MS.glob('ch*.md'), key=chapter_key):
        text = p.read_text(encoding='utf-8')
        lines = text.splitlines()
        title = lines[0].lstrip('# ').strip()
        num = re.match(r'Chapter ([\w]+)\.', title)
        number = num.group(1) if num else ''
        name = re.sub(r'^Chapter [\w]+\.\s*', '', title)
        partline = next((l for l in lines[1:6] if l.strip().startswith('*Part')), '')
        pm = re.search(r'Part\s+(\d+)', partline)
        if pm:
            part = pm.group(1)
        else:
            # Chapter 83 is headed *Closing* rather than a part; it ships inside Book 3.
            closing = next((l for l in lines[1:6] if l.strip().strip('*').lower() == 'closing'), None)
            part = 'closing' if closing else '?'
        sections = [(m.group(1), m.group(2).strip())
                    for m in re.finditer(r'^## (\d+\.\d+)\s+(.+)$', text, re.M)]
        rows.append(dict(
            key=p.name.split('-')[0], file=p.name, number=number, name=name, part=part,
            book=BOOK_OF_PART.get(part, '?'),
            learn=strip_md(field(text, 'You will learn to:')),
            before=strip_md(field(text, 'Before you start:')),
            time=strip_md(field(text, 'Time needed:')),
            sections=sections, terms=key_terms(text),
            words=len(text.split()), practice=practice_for(p.name.split('-')[0]),
        ))
    return rows


def short_time(s):
    """Just the headline figure, for a table meant to be scanned.

    The book's Time needed lines often carry a full week-by-week plan, which is useful to read and
    useless to scan, so the table takes the first duration and the detail below keeps all of it.
    """
    m = re.search(r'(\d+\s*[-–]\s*\d+|\d+)\s*(hours|hour|minutes)', s)
    return m.group(0).replace('-', '–') if m else (s[:28] + '…' if len(s) > 28 else s)


def hours(s):
    """The midpoint of a 'Time needed' range, for a part total. Returns None if unreadable."""
    nums = [float(x.replace('½', '.5')) for x in re.findall(r'\d+(?:[.,]\d+)?', s.replace('–', '-'))[:2]]
    m = re.search(r'(\d+)\s*[-–]\s*(\d+)\s*hours', s)
    if m:
        return (int(m.group(1)) + int(m.group(2))) / 2
    m = re.search(r'(\d+)\s*hours', s)
    return float(m.group(1)) if m else None


def write_md(rows, out):
    L = []
    w = L.append
    total_words = sum(r['words'] for r in rows)
    nb = sum(1 for r in rows if r['practice'] and r['practice']['counts'].get('notebook'))
    sq = sum(1 for r in rows if r['practice']
             and any(n.endswith('_postgresql.sql') for n in r['practice']['names'].get('SQL', []))
             and any(n.endswith('_mysql.sql') for n in r['practice']['names'].get('SQL', [])))

    w('# Where everything is')
    w('')
    w('*A map of Analyst to Architect: every chapter, what it teaches, how long it takes, and what '
      'you practise it with. Generated from the manuscript, so it cannot drift from the book.*')
    w('')
    w('## How to use this')
    w('')
    w('Three ways in, depending on what you are looking for.')
    w('')
    w('- **"Which book do I open?"** — the table in *The four books* below.')
    w('- **"Where is topic X taught?"** — *The topic index* at the end. It is alphabetical, built '
      'from every chapter\'s own Key terms list, and points at the chapter.')
    w('- **"What do I actually do in this chapter?"** — the part-by-part tables. Each chapter names '
      'the practice files that ship with it.')
    w('')
    w(f'The book is **{len(rows)} chapters**, about **{total_words:,} words**. '
      f'**{nb}** chapters have a worked notebook and **{sq}** ship runnable SQL in both PostgreSQL '
      'and MySQL.')
    w('')
    w('## The four books')
    w('')
    w('| Book | Parts | Chapters | What it is for |')
    w('|---|---|---|---|')
    bybook = collections.OrderedDict()
    for r in rows:
        bybook.setdefault(r['book'], []).append(r)
    purpose = {
        '1 · Theory': 'The ideas, with no software to install. Read it first.',
        '2 · Practical': 'The analyst\'s tools, hands on: spreadsheets, SQL, cleaning, charts, BI, '
                         'Python, statistics, then the advanced layer.',
        '3 · Implementation': 'Building real systems: machine learning, data engineering, '
                              'production ML and generative AI, architecture and leadership.',
        '4 · Be Interview Ready': 'The question banks, the extra-points method, take-homes and '
                                  'mock interviews.',
    }
    for b, rs in bybook.items():
        parts = sorted({r['part'] for r in rs}, key=lambda x: (len(x), x))
        w(f'| **Book {b}** | {", ".join(parts)} | {len(rs)} | {purpose.get(b, "")} |')
    w('')

    # ------------------------------------------------------------------ per part
    for part in sorted({r['part'] for r in rows}, key=lambda x: (len(x), x)):
        rs = [r for r in rows if r['part'] == part]
        hs = [hours(r['time']) for r in rs]
        known = [h for h in hs if h]
        w('---')
        w('')
        w(f'## {PART_TITLES.get(part, "Part " + part)}')
        w('')
        line = f'**Book {rs[0]["book"]}** · {len(rs)} chapters'
        if known:
            line += f' · roughly {int(sum(known))} hours in total'
        w(line)
        w('')
        w('| Ch | Chapter | Time | What you practise with |')
        w('|---|---|---|---|')
        for r in rs:
            pr = r['practice']
            if pr and pr['counts']:
                bits = [f'{n} {k}' if n > 1 else k for k, n in sorted(pr['counts'].items())]
                prac = ', '.join(bits)
            else:
                prac = '*reading only*'
            w(f'| {r["number"]} | **{r["name"]}** | {short_time(r["time"]) if r["time"] else "—"} | {prac} |')
        w('')
        for r in rs:
            w(f'### Chapter {r["number"]}. {r["name"]}')
            w('')
            if r['learn']:
                w(f'**You will learn to:** {r["learn"]}')
                w('')
            if r['before']:
                w(f'**Before you start:** {r["before"]}')
                w('')
            if r['time']:
                w(f'**Time needed:** {r["time"]}')
                w('')
            if r['sections']:
                w('**Sections:** ' + ' · '.join(f'{n} {t}' for n, t in r['sections']))
                w('')
            pr = r['practice']
            if pr and pr['names']:
                shown = []
                for kind in ['notebook', 'SQL', 'Python script', 'Excel workbook',
                             'dataset (csv)', 'dataset (parquet)']:
                    if kind in pr['names']:
                        fs = pr['names'][kind]
                        head = ', '.join(f'`{x}`' for x in fs[:4])
                        if len(fs) > 4:
                            head += f', and {len(fs) - 4} more'
                        shown.append(f'*{kind}:* {head}')
                if shown:
                    w(f'**In `companion/{r["key"]}/`** — ' + ' · '.join(shown))
                    w('')
            w('')

    # ------------------------------------------------------------------ topic index
    w('---')
    w('')
    w('## The topic index')
    w('')
    w('Every term the book defines, alphabetically, with the chapter that teaches it. Built from '
      'each chapter\'s own Key terms list. A term taught in more than one place lists them all, '
      'earliest first.')
    w('')
    index = collections.defaultdict(list)
    for r in rows:
        for t in r['terms']:
            index[t].append(r['number'])
    letters = collections.defaultdict(list)
    for term in sorted(index, key=lambda s: (re.sub(r'^\W+', '', s).lower(), s)):
        first = re.sub(r'^\W+', '', term)[:1].upper() or '#'
        if not first.isalpha():
            first = '#'
        letters[first].append((term, index[term]))
    w(f'**{len(index):,} terms.**')
    w('')
    for letter in sorted(letters):
        w(f'### {letter}')
        w('')
        w('| Term | Taught in |')
        w('|---|---|')
        for term, chs in letters[letter]:
            seen = []
            for c in chs:
                if c not in seen:
                    seen.append(c)
            w(f'| {term} | ' + ', '.join(f'Ch {c}' for c in seen) + ' |')
        w('')
    out.write_text('\n'.join(L) + '\n', encoding='utf-8')
    return len(index)


def write_xlsx(rows, path):
    try:
        import xlsxwriter
    except ImportError:
        print('xlsxwriter not available; skipping the workbook')
        return
    wb = xlsxwriter.Workbook(str(path))
    head = wb.add_format({'bold': True, 'bg_color': '#ECECEC', 'border': 1, 'valign': 'top'})
    wrap = wb.add_format({'text_wrap': True, 'valign': 'top'})
    top = wb.add_format({'valign': 'top'})

    ws = wb.add_worksheet('Chapters')
    cols = ['Book', 'Part', 'Ch', 'Chapter', 'Time needed', 'Words', 'Practice files',
            'You will learn to', 'Before you start']
    for i, c in enumerate(cols):
        ws.write(0, i, c, head)
    for ri, r in enumerate(rows, 1):
        pr = r['practice']
        prac = ', '.join(f'{k} x{n}' for k, n in sorted(pr['counts'].items())) if pr and pr['counts'] else ''
        for ci, v in enumerate([r['book'], r['part'], r['number'], r['name'], r['time'],
                                r['words'], prac, r['learn'], r['before']]):
            ws.write(ri, ci, v, wrap if ci in (3, 4, 6, 7, 8) else top)
    ws.set_column(0, 0, 20); ws.set_column(1, 2, 6); ws.set_column(3, 3, 42)
    ws.set_column(4, 4, 34); ws.set_column(5, 5, 9); ws.set_column(6, 6, 34)
    ws.set_column(7, 8, 60)
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, len(rows), len(cols) - 1)

    ws2 = wb.add_worksheet('Sections')
    for i, c in enumerate(['Book', 'Ch', 'Chapter', 'Section', 'Section title']):
        ws2.write(0, i, c, head)
    r2 = 1
    for r in rows:
        for n, t in r['sections']:
            for ci, v in enumerate([r['book'], r['number'], r['name'], n, t]):
                ws2.write(r2, ci, v, top)
            r2 += 1
    ws2.set_column(0, 0, 20); ws2.set_column(1, 1, 6); ws2.set_column(2, 2, 40)
    ws2.set_column(3, 3, 10); ws2.set_column(4, 4, 60)
    ws2.freeze_panes(1, 0); ws2.autofilter(0, 0, r2 - 1, 4)

    ws3 = wb.add_worksheet('Topic index')
    for i, c in enumerate(['Term', 'Taught in', 'Chapters']):
        ws3.write(0, i, c, head)
    index = collections.defaultdict(list)
    for r in rows:
        for t in r['terms']:
            if r['number'] not in index[t]:
                index[t].append(r['number'])
    for ri, term in enumerate(sorted(index, key=lambda s: s.lower()), 1):
        ws3.write(ri, 0, term, top)
        ws3.write(ri, 1, ', '.join(f'Ch {c}' for c in index[term]), top)
        ws3.write(ri, 2, len(index[term]), top)
    ws3.set_column(0, 0, 46); ws3.set_column(1, 1, 36); ws3.set_column(2, 2, 10)
    ws3.freeze_panes(1, 0); ws3.autofilter(0, 0, len(index), 2)
    wb.close()
    print(f'xlsx -> {path}  (3 sheets: {len(rows)} chapters, {r2 - 1} sections, {len(index)} terms)')


if __name__ == '__main__':
    out = pathlib.Path(sys.argv[1])
    rows = collect()
    n = write_md(rows, out)
    print(f'md   -> {out}  ({len(rows)} chapters, {n} index terms, '
          f'{len(out.read_text(encoding="utf-8").split()):,} words)')
    if len(sys.argv) > 2:
        write_xlsx(rows, pathlib.Path(sys.argv[2]))
