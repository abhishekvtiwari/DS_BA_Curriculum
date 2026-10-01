import re, subprocess, sys, html, pathlib, asyncio, os
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

# Paths. This script originally ran in the sandbox the book was written in and hardcoded
# /home/claude/book/pdf. It now resolves everything from its own location so it works in a clone.
HERE = pathlib.Path(__file__).resolve().parent      # tools/pdf: template.html and cover.html live here
ROOT = HERE.parents[1]                              # the book root: manuscript/, figures/, companion/
MS   = ROOT / 'manuscript'                          # chapter sources
D    = pathlib.Path(os.environ.get('BOOK_BUILD_DIR', ROOT / 'build' / 'pdf'))   # scratch
OUT  = pathlib.Path(os.environ.get('BOOK_OUT_DIR', D))                          # finished PDFs
D.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

def md_to_html(src, out, bodyclass, title, toc_depth):
    fmt = 'gfm+hard_line_breaks' if 'blueprint' in src else 'gfm'
    tmp = D/(pathlib.Path(src).stem + '.build.md')
    tmp.write_text(re.sub(r'^```mysql$', '```sql', pathlib.Path(src).read_text(), flags=re.M))
    src = str(tmp)
    subprocess.run(['pandoc', '-f', fmt, '-t', 'html5', '-s', '--template', str(HERE/'template.html'),
                    '--toc', f'--toc-depth={toc_depth}', '-M', f'pagetitle={title}', '-V', f'bodyclass={bodyclass}',
                    src, '-o', str(out)], check=True)
    h = out.read_text()
    h = re.sub(r'<blockquote>(\s*<p><strong>Watch out)', r'<blockquote class="warn">\1', h)
    # The HTML is written to the scratch dir D, so relative links to the stylesheet (beside this
    # script) and to figures/ (under the book root) would not resolve. Point them at the real files.
    h = h.replace('href="book.css"', f'href="{(HERE/"book.css").as_uri()}"')
    h = re.sub(r'src="(figures/[^"]+)"', lambda m: f'src="{(ROOT/m.group(1)).as_uri()}"', h)
    out.write_text(h)

def render(pw, html_path, pdf_path, footer_text=None):
    b = pw.chromium.launch()
    p = b.new_page()
    p.goto(f'file://{html_path}')
    p.wait_for_load_state('networkidle')
    p.evaluate('document.fonts.ready')
    kw = dict(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
    if footer_text:
        kw.update(display_header_footer=True, header_template='<div></div>',
                  footer_template=f'<div style="width:100%;font-family:DejaVu Sans,sans-serif;font-size:7.5pt;color:#6b7383;padding:0 18mm;display:flex;justify-content:space-between;"><span>{html.escape(footer_text)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    try:
        p.pdf(outline=True, **kw)
    except TypeError:
        p.pdf(**kw)
    b.close()

def build(src, name, bodyclass, title, footer, cover, toc_depth):
    src = str(src if os.path.isabs(str(src)) else MS / str(src))   # bare names resolve to manuscript/
    body_html = D/f'{name}.html'
    md_to_html(src, body_html, bodyclass, title, toc_depth)
    c = (HERE/'cover.html').read_text()
    for k, v in cover.items(): c = c.replace('{{'+k+'}}', v)
    (D/f'{name}-cover.html').write_text(c)
    with sync_playwright() as pw:
        render(pw, D/f'{name}-cover.html', D/f'{name}-cover.pdf')
        render(pw, body_html, D/f'{name}-body.pdf', footer)
    w = PdfWriter()
    w.append(str(D/f'{name}-cover.pdf'))
    w.append(str(D/f'{name}-body.pdf'))
    w.add_metadata({'/Title': title, '/Author': 'Abhishek Tiwari'})
    out = str(OUT / f'{name}.pdf')
    with open(out, 'wb') as f: w.write(f)
    print(out, len(PdfReader(out).pages), 'pages')

JOBS = {}
JOBS['blueprint'] = lambda: build('blueprint.md', 'Analyst-to-Architect-Blueprint', '',
          'Analyst to Architect — Expansion Blueprint', 'Analyst to Architect · Expansion Blueprint v3',
          dict(KICKER='Analyst to Architect', TITLE='Expansion Blueprint',
               SUB='The plan for turning the first-edition draft into the complete book: from “what is data?” to data architect, with the Interview Playbook.',
               DOC='Planning document · Version 3', META='16 September 2026<br>83 chapters · 9 parts · ~497,000 words'), 3)
JOBS['ch12'] = lambda: build('ch12-databases-and-sql-foundations.md', 'Ch12-Databases-and-SQL-Foundations', '',
          'Chapter 12. Databases & SQL Foundations', 'Analyst to Architect · Chapter 12 · Databases & SQL Foundations',
          dict(KICKER='Analyst to Architect · Part II — The Analyst', TITLE='Chapter 12<br>Databases &amp; SQL Foundations',
               SUB='Go to the data: tables, keys, filters, NULLs, summaries, joins, subqueries and transactions, taught from zero on the Riverstone Supplies database, in PostgreSQL and MySQL.',
               DOC='Sample chapter · Draft v4', META='16 September 2026<br>Every query tested on PostgreSQL 16 and MySQL 8'), 2)
JOBS['ch13'] = lambda: build('ch13-sql-for-real-analysis.md', 'Ch13-SQL-for-Real-Analysis', '',
          'Chapter 13. SQL for Real Analysis', 'Analyst to Architect · Chapter 13 · SQL for Real Analysis',
          dict(KICKER='Analyst to Architect · Part II — The Analyst', TITLE='Chapter 13<br>SQL for Real Analysis',
               SUB='CTEs, views, and window functions, then ten patterns analysts use every week: top N, Pareto, deduplication, funnels, cohorts, streaks and more.',
               DOC='Draft chapter', META='16 September 2026<br>Every query tested on PostgreSQL 16 and MySQL 8'), 2)
JOBS['ch01'] = lambda: build('ch01-what-is-data.md', 'Ch01-What-Is-Data', '',
      'Chapter 1. What Is Data?', 'Analyst to Architect · Chapter 1 · What Is Data?',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 1<br>What Is Data?',
           SUB='From a shop receipt to a company database: what data is, the shapes and types it comes in, which calculations it allows, and how to tell whether you can trust it.',
           DOC='Draft chapter', META='16 September 2026<br>Every number in the examples checked'), 2)

JOBS['ch12v3'] = lambda: build('ch12.v3.md', 'Ch12-Databases-and-SQL-Foundations-v3-approved', '',
      'Chapter 12. Databases & SQL Foundations', 'Analyst to Architect · Chapter 12 · Databases & SQL Foundations',
      dict(KICKER='Analyst to Architect · Part II — The Analyst', TITLE='Chapter 12<br>Databases &amp; SQL Foundations',
           SUB='Go to the data: tables, keys, filters, NULLs, summaries, joins, subqueries and transactions, taught from zero on the Riverstone Supplies database, in PostgreSQL and MySQL.',
           DOC='Approved · Draft v3', META='16 September 2026<br>Every query tested on PostgreSQL 16 and MySQL 8'), 2)

JOBS['ch02'] = lambda: build('ch02-how-computers-store-move-protect-data.md', 'Ch02-How-Computers-Store-Move-Protect-Data', '',
      'Chapter 2. How Computers Store, Move and Protect Data', 'Analyst to Architect · Chapter 2 · How Computers Store, Move and Protect Data',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 2<br>How Computers Store, Move and Protect Data',
           SUB='Bits and bytes, file sizes, formats from CSV to Parquet, databases, servers and the cloud, APIs, and the habits that keep data safe.',
           DOC='Draft chapter', META='16 September 2026<br>Every size, output, and timing measured'), 2)

JOBS['ch03'] = lambda: build('ch03-how-a-business-runs-on-data.md', 'Ch03-How-a-Business-Runs-on-Data', '',
      'Chapter 3. How a Business Runs on Data', 'Analyst to Architect · Chapter 3 · How a Business Runs on Data',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 3<br>How a Business Runs on Data',
           SUB='Departments and their data, one order from enquiry to cash, business systems, bookings vs billings vs collections, KPIs, decisions, and where manual work hides.',
           DOC='Draft chapter', META='16 September 2026<br>Every number checked against the Riverstone database'), 2)

JOBS['ch04'] = lambda: build('ch04-numbers-without-fear.md', 'Ch04-Numbers-Without-Fear', '',
      'Chapter 4. Numbers Without Fear', 'Analyst to Architect · Chapter 4 · Numbers Without Fear',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 4<br>Numbers Without Fear',
           SUB='Percentages and points, ratios and rates, compound growth and CAGR, averages, rounding, honest charts, probability, estimation, and the number tricks in business news.',
           DOC='Draft chapter', META='16 September 2026<br>Every number checked against the Riverstone database'), 2)

JOBS['ch05'] = lambda: build('ch05-thinking-like-an-analyst.md', 'Ch05-Thinking-Like-an-Analyst', '',
      'Chapter 5. Thinking Like an Analyst', 'Analyst to Architect · Chapter 5 · Thinking Like an Analyst',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 5<br>Thinking Like an Analyst',
           SUB='Good questions, precise problem statements, hypotheses, issue trees and MECE, facts versus opinions, checking claims, bias, and deciding with data.',
           DOC='Draft chapter', META='17 September 2026<br>Every number checked against the Riverstone databases'), 2)

JOBS['ch06'] = lambda: build('ch06-setting-up-to-learn.md', 'Ch06-Setting-Up-to-Learn', '',
      'Chapter 6. Setting Up to Learn', 'Analyst to Architect · Chapter 6 · Setting Up to Learn',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 6<br>Setting Up to Learn',
           SUB='The computer you need, installing and checking the book\'s tools, companion files, documentation, learning with AI assistants, and a study plan you can keep.',
           DOC='Draft chapter', META='17 September 2026<br>Versions and install steps checked against official sources'), 2)

JOBS['part0'] = lambda: build('part0-first-principles.md', 'Part0-First-Principles-Data-from-Zero', 'break-h1',
      'Analyst to Architect — Part 0: First Principles', 'Analyst to Architect · Part 0 · First Principles: Data from Zero',
      dict(KICKER='Analyst to Architect · Part 0', TITLE='First Principles:<br>Data from Zero',
           SUB='Chapters 1–6: what data is, how computers store and move it, how a business runs on it, numbers without fear, thinking like an analyst, and setting up to learn.',
           DOC='Approved chapters · Version 1', META='17 September 2026<br>6 chapters · about 50,000 words · 23 figures · 88 exercises with answers'), 1)

JOBS['part1'] = lambda: build('part1-the-map.md', 'Part1-The-Map', 'break-h1',
      'Analyst to Architect — Part I: The Map', 'Analyst to Architect · Part I · The Map',
      dict(KICKER='Analyst to Architect · Part I', TITLE='The Map',
           SUB='Chapters 7–9: the data landscape, the career tree and how skills unlock roles, and how expertise actually forms.',
           DOC='Approved chapters · Version 1', META='17 September 2026<br>3 chapters · about 29,000 words · 13 figures · 43 exercises with answers'), 1)

JOBS['ch25'] = lambda: build('ch25-the-business-analyst-track.md', 'Ch25-The-Business-Analyst-Track', '',
      'Chapter 25. The Business Analyst Track', 'Analyst to Architect · Chapter 25 · The Business Analyst Track',
      dict(KICKER='Analyst to Architect · Part II — The Analyst', TITLE='Chapter 25<br>The Business Analyst Track',
           SUB='The business analyst on a data team: how the work divides between BA, data analyst, data scientist and data engineer, and how to specify the four things a data team is asked to build \u2014 a dashboard, a pipeline, a model, and a metric.',
           DOC='Draft chapter · v2', META='21 September 2026<br>Every example is a data product'), 2)

JOBS['ch26'] = lambda: build('ch26-the-professional-toolkit-git-agile-documentation-and-ai-assistants.md', 'Ch26-The-Professional-Toolkit', '',
      'Chapter 26. The Professional Toolkit: Git, Agile, Documentation & AI Assistants',
      'Analyst to Architect \u00b7 Chapter 26 \u00b7 The Professional Toolkit',
      dict(KICKER='Analyst to Architect \u00b7 Part II \u2014 The Analyst',
           TITLE='Chapter 26<br>The Professional Toolkit',
           SUB='Git, GitHub and pull requests; the four undos; keeping secrets out of a repository; one automated check; a README a stranger can follow; Agile, Scrum, Kanban and Jira; and working with an AI assistant.',
           DOC='Draft chapter \u00b7 v1', META='21 September 2026<br>Every terminal session was run and its output captured'), 2)

JOBS['ch27'] = lambda: build('ch27-capstone-your-analyst-portfolio.md', 'Ch27-Capstone-Your-Analyst-Portfolio', '',
      'Chapter 27. Capstone: Your Analyst Portfolio',
      'Analyst to Architect \u00b7 Chapter 27 \u00b7 Capstone: Your Analyst Portfolio',
      dict(KICKER='Analyst to Architect \u00b7 Part II \u2014 The Analyst',
           TITLE='Chapter 27<br>Capstone: Your<br>Analyst Portfolio',
           SUB='One question taken from the database to the memo, the check that turned a flattering finding into an honest one, and what happens to the work when a hiring manager opens it.',
           DOC='Draft chapter \u00b7 v1', META='21 September 2026<br>Every query and every output was run on the full three-year database'), 2)

JOBS['ch83'] = lambda: build('ch83-the-long-game.md', 'Ch83-The-Long-Game', '',
      'Chapter 83. The Long Game',
      'Analyst to Architect \u00b7 Chapter 83 \u00b7 The Long Game',
      dict(KICKER='Analyst to Architect \u00b7 Closing',
           TITLE='Chapter 83<br>The Long Game',
           SUB='What the book actually costs in hours, the pace that survives a bad month, how to choose your own summit, and the four plateaus that arrive after the first job.',
           DOC='Draft chapter \u00b7 v1', META='21 September 2026<br>The hours are computed from the book\u2019s own chapter estimates'), 2)

# ---------------------------------------------------------------------------
# Generic builder.
#
# Only 12 of the book's 85 chapters have a hand-written job above; those are the ones that were
# built in the sandbox this script came from. Every other chapter is built from its own opening
# lines instead. A derived cover will not match a hand-written cover word for word, but it is
# still exactly one page, so page numbers inside the body are unaffected and stay comparable
# with the page references in review/visual/.

# Eight chapters' released PDF filenames are shorter than their full H1 title. Pinned here so a
# rebuilt file is named exactly like the one the review looked at.
NAMES = {
    'ch02': 'Ch02-How-Computers-Store-Move-Protect-Data',
    'ch18': 'Ch18-Python-for-Analysts',
    'ch19': 'Ch19-Spreadsheet-Automation',
    'ch26': 'Ch26-The-Professional-Toolkit',
    'ch51': 'Ch51-Data-Activation',
    'ch54': 'Ch54-Generative-AI-and-LLMs',
    'ch55': 'Ch55-Building-AI-Applications',
    'ch56': 'Ch56-MLOps',
}

# Two released footers carry a shorter title than the chapter's H1. Pinned for the same reason.
FOOTER_NAMES = {
    'ch19': 'Spreadsheet Automation: Macros, VBA, Office Scripts & Apps Script',
    'ch51': 'Data Activation',
}


def chapter_md(key):
    """manuscript/<key>-*.md for a key like 'ch40' or 'ch72a'."""
    hits = sorted(MS.glob(key + '-*.md'))
    return hits[0] if hits else None


def generic_job(key):
    src = chapter_md(key)
    if src is None:
        raise SystemExit('no chapter file matching %r in %s' % (key, MS))
    head = src.read_text(encoding='utf-8').splitlines()[:6]
    h1 = next((l[2:].strip() for l in head if l.startswith('# ')), key)
    part = next((l.strip().strip('*') for l in head if l.startswith('*Part')), 'Closing')
    m = re.match(r'Chapter\s+([0-9]+[A-Za-z]?)\.\s*(.+)', h1)
    num, name = (m.group(1), m.group(2)) if m else ('', h1)
    slug = re.sub(r'[^A-Za-z0-9]+', '-', name.replace('&', 'and')).strip('-')
    pad = num.zfill(3)[-3:] if False else (num if len(num.rstrip('ABCDEFGHIJabcdefghij')) >= 2 else num.zfill(2) if num.isdigit() else num[:-1].zfill(2) + num[-1].upper())
    out_name = NAMES.get(key) or (('Ch%s-%s' % (pad, slug)) if num else slug)
    title_html = ('Chapter %s<br>%s' % (num, html.escape(name))) if num else html.escape(name)
    return build(src.name, out_name, '', h1,
                 # released footers read "Chapter 40 · Time Series & Forecasting", not "Chapter 40. …"
                 'Analyst to Architect · ' + (('Chapter %s · %s' % (num, FOOTER_NAMES.get(key, name))) if num else h1),
                 dict(KICKER='Analyst to Architect · ' + part,
                      TITLE=title_html,
                      SUB='',
                      DOC='Rebuilt',
                      META=''),
                 2)


def run(key):
    if key in JOBS:
        JOBS[key]()
    else:
        generic_job(key)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] in (['--list'], ['-l']):
        print('hand-written jobs:', ' '.join(sorted(JOBS)))
        print('any other chapter key (ch07, ch40, ch72a ...) builds with a derived cover')
        print('all-chapters      builds every chapter in manuscript/')
        raise SystemExit
    if args == ['all-chapters']:
        args = sorted({f.name.split('-')[0] for f in MS.glob('ch*.md')})
    for k in (args or list(JOBS)):
        run(k)
