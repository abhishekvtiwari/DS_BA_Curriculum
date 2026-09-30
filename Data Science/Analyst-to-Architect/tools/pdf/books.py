"""Build the book as reader volumes, plus the internal overview.

    python tools/pdf/books.py              # all four PDFs into build/
    python tools/pdf/books.py overview     # or: volumes, playbook

- Analyst to Architect, Volume 1 (How to Use This Book, Parts 0 to 2) and Volume 2 (Parts 3 to 7 and
  the closing chapter). One page count runs through both volumes: Volume 2 starts where Volume 1 ends.
  A single file would be about 150 MB, over GitHub's 100 MB limit, so the book is split at "job-ready".
- The Interview Playbook: Part 8 as its own book.
- Book Overview (internal): every part and chapter, the skills each covers, and how they flow, from
  manuscript/book-overview.md (written by tools/make_overview.py).

Both volumes open with "The whole book", a map of every part and chapter with its volume and page.
"""
import html, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build as B
from build import build_package, chapter_files, PART2_ORDER, PART3_ORDER, D, OUT


V1 = ('Analyst-to-Architect-Volume-1-From-Zero-to-Job-Ready',
      ['front-how-to-use-this-book.md', 'part0-first-principles.md', 'part1-the-map.md',
       'part2-the-analyst.md'] + chapter_files(PART2_ORDER),
      'Analyst to Architect — Volume 1: From Zero to Job-Ready',
      dict(KICKER='Analyst to Architect · Volume 1 of 2', TITLE='From Zero<br>to Job-Ready',
           SUB='How to use this book; Part 0, First Principles; Part 1, The Map; and Part 2, The Analyst: '
               'from "what is data" to the skills of a first analyst job.'))
V2 = ('Analyst-to-Architect-Volume-2-From-Analyst-to-Architect',
      ['part3-advanced-analytics.md'] + chapter_files(PART3_ORDER)
      + ['part4-machine-learning.md'] + chapter_files(range(35, 45))
      + ['part5-data-engineering.md'] + chapter_files(range(45, 53))
      + ['part6-production-ml-genai.md'] + chapter_files(range(53, 60))
      + ['part7-architecture-leadership.md'] + chapter_files(range(60, 68))
      + chapter_files([83]),
      'Analyst to Architect — Volume 2: From Analyst to Architect',
      dict(KICKER='Analyst to Architect · Volume 2 of 2', TITLE='From Analyst<br>to Architect',
           SUB='Parts 3 to 7: advanced analytics, machine learning, data engineering, production ML and '
               'generative AI, and architecture and leadership; then the closing chapter, The Long Game.'))
PLAYBOOK = ('The-Interview-Playbook',
            ['part8-interview-playbook.md'] + chapter_files(B.PART_PACKAGES['8'][1]),
            'The Interview Playbook — a companion to Analyst to Architect',
            dict(KICKER='A companion to Analyst to Architect', TITLE='The Interview<br>Playbook',
                 SUB='How data hiring works, the extra-points method, and a question bank for each skill and '
                     'role, with take-home assignments and mock interviews.'))
OVERVIEW = ('Analyst-to-Architect-Book-Overview', ['book-overview.md'],
            'Analyst to Architect — Book Overview (internal)',
            dict(KICKER='Analyst to Architect · Internal', TITLE='Book Overview',
                 SUB='Every part and chapter, the skills each one covers, how long it takes, what it builds on, '
                     'and how the parts lead into each other.'))


def pages_used(name, label):
    """The last page label of a built package's body."""
    import pymupdf
    with pymupdf.open(str(D / f'{name}-body.pdf')) as d:
        return int(label(len(d)))


def whole_book_map(vols):
    """HTML for 'The whole book': each part and its chapters, with volume and page."""
    rows = []
    for v, heads, label in vols:
        for pg, t in heads:
            if t.startswith('Part ') or t.startswith('How to Use'):
                rows.append(f'<tr class="p"><td>{html.escape(t)}</td><td>Vol. {v}</td><td>{label(pg)}</td></tr>')
            elif t.startswith('Chapter '):
                if t.startswith('Chapter 83.'):
                    rows.append(f'<tr class="p"><td>Closing</td><td></td><td></td></tr>')
                rows.append(f'<tr><td class="c">{html.escape(t)}</td><td>Vol. {v}</td><td>{label(pg)}</td></tr>')
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
<p><em>Analyst to Architect</em> comes in two volumes with one page count. Volume 1 takes you from zero to
job-ready (Parts 0 to 2); Volume 2 goes on to the specialist and architect roles (Parts 3 to 7, then the
closing chapter). Each volume's own contents, after this map, lists the sections of its chapters. The
interview chapters (Part 8) are a separate book, <em>The Interview Playbook</em>.</p>
<table>{''.join(rows)}</table></body></html>"""


def add_map(pdf_name, map_pdf):
    """Insert the map after the cover, with a bookmark."""
    import pymupdf, os
    path = OUT / f'{pdf_name}.pdf'
    doc = pymupdf.open(str(path))
    m = pymupdf.open(str(map_pdf))
    toc = doc.get_toc(simple=False)
    doc.insert_pdf(m, start_at=1)
    for e in toc: e[2] += len(m)
    doc.set_toc([[1, 'The whole book', 2]] + toc)
    tmp = str(path) + '.tmp'
    doc.save(tmp, garbage=3, deflate=True)
    doc.close(); m.close()
    os.replace(tmp, str(path))


def volumes():
    name1, srcs1, title1, cover1 = V1
    heads1, label1 = build_package(srcs1, name1, title1, cover1)
    n1 = pages_used(name1, label1)
    name2, srcs2, title2, cover2 = V2
    heads2, label2 = build_package(srcs2, name2, title2, cover2, offset=n1)
    (D / 'whole-book-map.html').write_text(whole_book_map([(1, heads1, label1), (2, heads2, label2)]))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        B.render(pw, D / 'whole-book-map.html', D / 'whole-book-map.pdf')
    for name in (name1, name2):
        add_map(name, D / 'whole-book-map.pdf')
    print('Volume 1 ends on page', n1, '; Volume 2 ends on page', pages_used(name2, label2))


def playbook():
    name, srcs, title, cover = PLAYBOOK
    build_package(srcs, name, title, cover, book='The Interview Playbook')


def overview():
    name, srcs, title, cover = OVERVIEW
    build_package(srcs, name, title, cover, book='Book Overview')


if __name__ == '__main__':
    jobs = dict(overview=overview, playbook=playbook, volumes=volumes)
    for k in (sys.argv[1:] or ['overview', 'playbook', 'volumes']):
        jobs[k]()
