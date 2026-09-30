"""Build the four books, plus the internal overview.

    python tools/pdf/books.py book1 book2 book3 book4 map    # the four books, then the whole-book map
    python tools/pdf/books.py overview                        # the internal Book Overview

The book is published as four books, split by part (chapters stay whole):

  1. Theory           How to Use This Book, Part 0 and Part 1: the ideas, no software.
  2. Practical        Parts 2 and 3: the analyst's tools, hands on.
  3. Implementation   Parts 4 to 7 and the closing chapter: building real systems.
  4. Be Interview Ready  Part 8.

Books 1 to 3 share one page count: each starts where the one before ended, so build them in order. Each
book saves its page labels beside it (build/<name>-heads.json), so a later book, or the map, can be built
alone. "map" writes "The whole book", a map of every part and chapter with its book and page, and inserts
it after the cover of all four books. The Book Overview (internal) is manuscript/book-overview.md, written
by tools/make_overview.py.
"""
import html, json, os, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build as B
from build import build_package, chapter_files, PART2_ORDER, PART3_ORDER, D, OUT

B.SAVE_GARBAGE = 1       # the default clean-up takes half an hour per save on a 1,500-page book

# (key, file name, sources, PDF title, cover, footer title, page count continues from)
BOOKS = [
    ('book1', 'Analyst-to-Architect-Book-1-Theory',
     ['front-how-to-use-this-book.md', 'part0-first-principles.md', 'part1-the-map.md'],
     'Analyst to Architect — Book 1: Theory',
     dict(KICKER='Analyst to Architect · Book 1 of 4', TITLE='Theory',
          SUB='How to use this book; Part 0, First Principles: Data from Zero; and Part 1, The Map. What data '
              'is, how a business runs on it, numbers without fear, thinking like an analyst, and the map of '
              'data careers. No software needed.'),
     'Analyst to Architect', None),
    ('book2', 'Analyst-to-Architect-Book-2-Practical',
     ['part2-the-analyst.md'] + chapter_files(PART2_ORDER)
     + ['part3-advanced-analytics.md'] + chapter_files(PART3_ORDER),
     'Analyst to Architect — Book 2: Practical',
     dict(KICKER='Analyst to Architect · Book 2 of 4', TITLE='Practical',
          SUB='Part 2, The Analyst, and Part 3, Advanced Analytics &amp; Analytics Engineering. Spreadsheets, '
              'SQL, cleaning, charts, Power BI, Python, statistics, business skills and a portfolio; then '
              'advanced SQL, the command line, dbt, experiments and causal inference.'),
     'Analyst to Architect', 'book1'),
    ('book3', 'Analyst-to-Architect-Book-3-Implementation',
     ['part4-machine-learning.md'] + chapter_files(range(35, 45))
     + ['part5-data-engineering.md'] + chapter_files(range(45, 53))
     + ['part6-production-ml-genai.md'] + chapter_files(range(53, 60))
     + ['part7-architecture-leadership.md'] + chapter_files(range(60, 68))
     + chapter_files([83]),
     'Analyst to Architect — Book 3: Implementation',
     dict(KICKER='Analyst to Architect · Book 3 of 4', TITLE='Implementation',
          SUB='Parts 4 to 7: machine learning, data engineering, production ML and generative AI, and '
              'architecture and leadership. Then the closing chapter, The Long Game.'),
     'Analyst to Architect', 'book2'),
    ('book4', 'Analyst-to-Architect-Book-4-Be-Interview-Ready',
     ['part8-interview-playbook.md'] + chapter_files(B.PART_PACKAGES['8'][1]),
     'Analyst to Architect — Book 4: Be Interview Ready',
     dict(KICKER='Analyst to Architect · Book 4 of 4', TITLE='Be Interview<br>Ready',
          SUB='Part 8. How data hiring works, the extra-points method, and a question bank for each skill '
              'and role, with take-home assignments and mock interviews.'),
     'Be Interview Ready', None),
]
BY_KEY = {b[0]: b for b in BOOKS}
OVERVIEW = ('Analyst-to-Architect-Book-Overview', ['book-overview.md'],
            'Analyst to Architect — Book Overview (internal)',
            dict(KICKER='Analyst to Architect · Internal', TITLE='Book Overview',
                 SUB='Every part and chapter, the skills each one covers, how long it takes, what it builds on, '
                     'and how the parts lead into each other.'))


def saved(key):
    """(heads, labels) saved when the book was built: heads is [(physical page, H1)], labels the page labels."""
    j = json.loads((D / f'{BY_KEY[key][1]}-heads.json').read_text())
    return [tuple(h) for h in j['heads']], j['labels']


def build_book(key):
    _, name, srcs, title, cover, footer, after = BY_KEY[key]
    offset = int(saved(after)[1][-1]) if after else 0
    heads, label = build_package(srcs, name, title, cover, offset=offset, book=footer)
    import pymupdf
    with pymupdf.open(str(D / f'{name}-body.pdf')) as d:
        labels = [label(n) for n in range(1, len(d) + 1)]
    (D / f'{name}-heads.json').write_text(json.dumps(dict(heads=heads, labels=labels)))
    print(name, 'pages', labels[0], '…', labels[-1])


def whole_book_map():
    """HTML for 'The whole book': each part and its chapters, with book and page."""
    rows = []
    for n, (key, *_rest) in enumerate(BOOKS, 1):
        heads, labels = saved(key)
        for pg, t in heads:
            p = labels[pg - 1]
            if t.startswith('Part ') or t.startswith('How to Use'):
                rows.append(f'<tr class="p"><td>{html.escape(t)}</td><td>Book {n}</td><td>{p}</td></tr>')
            elif t.startswith('Chapter '):
                if t.startswith('Chapter 83.'):
                    rows.append('<tr class="p"><td>Closing</td><td></td><td></td></tr>')
                rows.append(f'<tr><td class="c">{html.escape(t)}</td><td>Book {n}</td><td>{p}</td></tr>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 20mm 20mm 18mm; }}
body {{ font-family: "Lora","DejaVu Serif",serif; font-size: 10pt; color:#1d2330; }}
h1 {{ font-family: "Poppins","DejaVu Sans",sans-serif; font-size: 22pt; color:#0f3d5c; margin: 0 0 3mm; }}
p {{ line-height: 1.45; margin: 0 0 3mm; }}
table {{ width:100%; border-collapse: collapse; }}
td {{ padding: 1.1mm 0; vertical-align: top; }}
td:nth-child(2) {{ width: 16mm; color:#4a5363; font-size: 9pt; }}
td:nth-child(3) {{ width: 12mm; text-align: right; font-variant-numeric: tabular-nums; }}
tr.p td {{ font-family: "Poppins","DejaVu Sans",sans-serif; font-weight: 600; color:#0f3d5c;
          padding-top: 3.5mm; break-after: avoid; }}
td.c {{ padding-left: 5mm; }}
tr {{ break-inside: avoid; }}
</style></head><body>
<h1>The whole book</h1>
<p><em>Analyst to Architect</em> comes as four books. <strong>Book 1, Theory</strong>, gives you the ideas, with
no software (Parts 0 and 1). <strong>Book 2, Practical</strong>, teaches the analyst's tools, hands on (Parts 2
and 3). <strong>Book 3, Implementation</strong>, builds real systems (Parts 4 to 7, then the closing chapter).
<strong>Book 4, Be Interview Ready</strong>, is Part 8. Books 1 to 3 share one page count; Book 4 has its own.
Each book's contents, after this map, lists the sections of its chapters.</p>
<table>{''.join(rows)}</table></body></html>"""


def add_map(pdf_name, map_pdf):
    """Insert the map after the cover, with a bookmark (replacing an earlier map)."""
    import pymupdf
    path = OUT / f'{pdf_name}.pdf'
    doc = pymupdf.open(str(path))
    m = pymupdf.open(str(map_pdf))
    toc = doc.get_toc(simple=False)
    if toc and toc[0][1] == 'The whole book':
        old = toc[1][2] - 2
        doc.delete_pages(1, old)
        toc = toc[1:]
        for e in toc: e[2] -= old
    doc.insert_pdf(m, start_at=1)
    for e in toc: e[2] += len(m)
    doc.set_toc([[1, 'The whole book', 2]] + toc)
    tmp = str(path) + '.tmp'
    doc.save(tmp, garbage=1, deflate=True)
    doc.close(); m.close()
    os.replace(tmp, str(path))


def book_map():
    (D / 'whole-book-map.html').write_text(whole_book_map())
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        B.render(pw, D / 'whole-book-map.html', D / 'whole-book-map.pdf')
    for b in BOOKS:
        add_map(b[1], D / 'whole-book-map.pdf')
        print('map added to', b[1])


def overview():
    name, srcs, title, cover = OVERVIEW
    build_package(srcs, name, title, cover, book='Book Overview')


if __name__ == '__main__':
    jobs = dict(overview=overview, map=book_map, **{b[0]: (lambda k: lambda: build_book(k))(b[0]) for b in BOOKS})
    for k in (sys.argv[1:] or [b[0] for b in BOOKS] + ['map', 'overview']):
        jobs[k]()
