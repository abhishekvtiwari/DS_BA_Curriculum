import re, subprocess, sys, html, pathlib, asyncio, os, json
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

LABEL_LINE = re.compile(r'^(> )?\*\*[^*]{1,60}?(:|\.)\*\*|^(> )?\*\*[^*]{1,60}?\*\*:')
LIST_LINE = re.compile(r'^(> )?(\s*[-*+]\s|\s*\d+\.\s)')

def label_breaks(md):
    """A line that starts with a bold label ("**Red flag:**", "**FR-02.**", "> **From:**") starts a new
    line, as the author wrote it. Markdown would otherwise run it into the previous line's paragraph
    (visual review: memo headers, requirement and use-case boxes, question-bank follow-ups)."""
    L = md.split('\n'); fence = False
    for i in range(1, len(L)):
        if L[i - 1].lstrip('> ').startswith('```'): fence = not fence
        if fence or not LABEL_LINE.match(L[i]): continue
        prev = L[i - 1]
        if prev.strip() in ('', '>') or re.match(r'^(> )?(\||#|```)', prev): continue
        if LIST_LINE.match(prev):                       # end the list first, or the label joins its last item
            L[i] = ('>\n' if L[i].startswith('>') else '\n') + L[i]
        elif not prev.endswith('\\') and not prev.endswith('  '):
            L[i - 1] = prev + '\\'
    return '\n'.join(L)

def md_to_html(src, out, bodyclass, title, toc_depth):
    # "$" is money in this book, never TeX maths (visual review V11: "$0.023 per GB" printed as maths)
    fmt = 'gfm+hard_line_breaks-tex_math_dollars' if 'blueprint' in src else 'gfm-tex_math_dollars'
    tmp = D/(pathlib.Path(src).stem + '.build.md')
    tmp.write_text(label_breaks(re.sub(r'^```mysql$', '```sql', pathlib.Path(src).read_text(), flags=re.M)))
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
    # V11 glyphs: Lora has no superscript T (it fell back to a glyph that reads as "S"), and a
    # combining macron lands on the wrong letter in Lora Italic. Draw both with markup instead.
    h = prose_only(h, typeset)
    h = prose_only(h, carets, split_tags=False)
    out.write_text(h)

SUP = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱᵀ', '0123456789+−=()niT'))
SUB = dict(zip('₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₙₛₜ', '0123456789+−=()aeoxnst'))

def prose_only(h, fn, split_tags=True):
    """Apply fn to text outside <pre> blocks and <code> spans (and outside tags, by default)."""
    pat = r'(<pre\b.*?</pre>|<code\b.*?</code>|<[^>]+>)' if split_tags else r'(<pre\b.*?</pre>|<code\b.*?</code>|<(?!/?(?:em|strong)>)[^>]+>)'
    parts = re.split(pat, h, flags=re.S)
    return ''.join(p if i % 2 else fn(p) for i, p in enumerate(parts))

def typeset(s):
    # V11 glyphs. Unicode sub/superscript digits come from a fallback font and sit on the
    # baseline (w₁x₁ reads as w1x1), and Lora has no superscript T: set them as real <sup>/<sub>.
    s = re.sub('[' + ''.join(SUP) + ']+', lambda m: '<sup>' + ''.join(SUP[c] for c in m.group()) + '</sup>', s)
    s = re.sub('[' + ''.join(SUB) + ']+', lambda m: '<sub>' + ''.join(SUB[c] for c in m.group()) + '</sub>', s)
    # a combining macron lands on the wrong letter in Lora Italic: draw the bar with CSS
    s = re.sub('(\\w)\u0304', r'<span class="ovl">\1</span>', s)
    # identifiers and ISO dates never break at their hyphens (V3.10, V25.12, V73.10 …)
    s = re.sub(r'\b(\d{4}-\d{2}-\d{2}|Q\d{2,3}[A-Z]?-\d{3}|[A-Z]{1,4}-\d{1,4})\b', r'<span class="nobr">\1</span>', s)
    return s

def carets(s):
    """Caret powers in prose ("e^(−λ)", "2^16", "*p*^*k*") become superscripts (V35.3, V37.6, V43.7, V52.12).
    Works on prose that may contain <em>/<strong>, never on code."""
    base = r'(?<=[\w)>])'
    s = re.sub(base + r'\^\(((?:[^()<]|<em>[^<]*</em>){1,40})\)', r'<sup>\1</sup>', s)
    s = re.sub(base + r'\^(<em>[^<]{1,10}</em>)', r'<sup>\1</sup>', s)
    s = re.sub(base + r'\^([−-]?(?:\w[\w.]{0,10})?\w)(?![\w.]*\w)', r'<sup>\1</sup>', s)
    return s

LAYOUT_JS = (HERE / 'layout.js').read_text()
PRINT_W_PX = round((210 - 18 - 18) * 96 / 25.4)    # A4 minus the @page side margins, in CSS px

def toc_numbers(html_text, marks):
    """Write page numbers into the contents (V2). marks is the ordered list of (title, page) bookmarks.
    Each contents entry takes the next unused bookmark whose title starts like it. Titles are matched
    loosely because Chromium writes a wrapped heading's bookmark with each line doubled."""
    pos = [0]
    def one(m):
        attrs, inner = m.group(1), m.group(2)
        if '<span class="toc-t">' in inner:
            inner = re.search(r'<span class="toc-t">(.*?)</span>', inner, re.S).group(1)
        key = norm_title(html.unescape(re.sub(r'<[^>]+>', '', inner)))[:12]
        pg = '00'
        for k in range(pos[0], len(marks)):
            if marks[k][0].startswith(key) or undouble(marks[k][0]).startswith(key):
                pg = str(marks[k][1]); pos[0] = k + 1; break
        return f'<a{attrs}><span class="toc-t">{inner}</span><span class="toc-dots"></span><span class="toc-pg">{pg}</span></a>'
    a, b = html_text.find('<nav id="TOC"'), html_text.find('</nav>')
    if a < 0: return html_text
    nav = re.sub(r'<a(\s+href="#[^"]*"[^>]*)>(.*?)</a>', one, html_text[a:b], flags=re.S)
    return html_text[:a] + nav + html_text[b:]

def undouble(s):
    """Chromium writes a wrapped heading's bookmark as line1 line1 line2 line2 …: keep one of each."""
    out = ''
    while s:
        L = next((n for n in range(len(s) // 2, 2, -1) if s[:n] == s[n:2 * n]), 0)
        if not L: return out + s
        out += s[:L]; s = s[2 * L:]
    return out

def norm_title(s):
    return re.sub(r'\s+', '', s).lower()        # ignore spaces: a wrapped heading loses one in the PDF

def outline_pages(pdf_path):
    """Ordered (title, page) for every bookmark Chromium writes (one per heading)."""
    r = PdfReader(str(pdf_path)); out = []
    def walk(items):
        for it in items:
            if isinstance(it, list): walk(it); continue
            out.append((norm_title(it.title), r.get_destination_page_number(it) + 1))
    walk(r.outline)
    return out

def render(pw, html_path, pdf_path, footer_text=None, layout=False):
    b = pw.chromium.launch()
    p = b.new_page(viewport={'width': PRINT_W_PX, 'height': 1100})
    p.emulate_media(media='print')
    p.goto(f'file://{html_path}')
    p.wait_for_load_state('networkidle')
    p.evaluate('document.fonts.ready')
    rep = p.evaluate(LAYOUT_JS) if layout else None
    kw = dict(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
    if footer_text:
        kw.update(display_header_footer=True, header_template='<div></div>',
                  footer_template=f'<div style="width:100%;font-family:DejaVu Sans,sans-serif;font-size:7.5pt;color:#6b7383;padding:0 18mm;display:flex;justify-content:space-between;"><span>{html.escape(footer_text)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    try:
        p.pdf(outline=True, tagged=True, **kw)
    except TypeError:
        p.pdf(**kw)
    b.close()
    return rep

def build(src, name, bodyclass, title, footer, cover, toc_depth):
    src = str(src if os.path.isabs(str(src)) else MS / str(src))   # bare names resolve to manuscript/
    body_html = D/f'{name}.html'
    md_to_html(src, body_html, bodyclass, title, toc_depth)
    # V1: one cover template for every chapter. No draft/approval badge, version or date on a
    # reader-facing cover; "Chapter N." is written with its full stop, as in the headings (V12.27).
    cover = dict(cover, DOC='', META='')
    cover['TITLE'] = re.sub(r'^(Chapter \d+[A-Za-z]?)(<br>)', r'\1.\2', cover['TITLE'])
    c = (HERE/'cover.html').read_text()
    for k, v in cover.items(): c = c.replace('{{'+k+'}}', v)
    (D/f'{name}-cover.html').write_text(c)
    with sync_playwright() as pw:
        render(pw, D/f'{name}-cover.html', D/f'{name}-cover.pdf')
        # V2: render, read each heading's page from the PDF bookmarks, write the numbers into the
        # contents, and render again until the numbers stop changing (usually two passes).
        base = body_html.read_text()
        pages, rep = [], None
        for attempt in range(4):
            body_html.write_text(toc_numbers(base, pages))
            rep = render(pw, body_html, D/f'{name}-body.pdf', footer, layout=True)
            new = outline_pages(D/f'{name}-body.pdf')
            if new == pages: break
            pages = new
        (D/f'{name}-layout.json').write_text(json.dumps(rep, indent=1, ensure_ascii=False))
        if rep and rep.get('overflow'):
            print('  WARNING wider than the text block:', rep['overflow'][:3])
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

JOBS['ch06'] = lambda: build('ch06-setting-up-to-learn.md', 'Ch06-Planning-Your-Learning', '',
      'Chapter 6. Planning Your Learning', 'Analyst to Architect · Chapter 6 · Planning Your Learning',
      dict(KICKER='Analyst to Architect · Part 0 — First Principles', TITLE='Chapter 6<br>Planning Your Learning',
           SUB='How long the book really takes, a weekly rhythm you can keep, when each tool arrives, reading documentation, learning with AI assistants, and a plan for your first 90 days.',
           DOC='Draft chapter', META='17 September 2026<br>Versions and install steps checked against official sources'), 2)

JOBS['part0'] = lambda: build('part0-first-principles.md', 'Part0-First-Principles-Data-from-Zero', 'break-h1',
      'Analyst to Architect — Part 0: First Principles', 'Analyst to Architect · Part 0 · First Principles: Data from Zero',
      dict(KICKER='Analyst to Architect · Part 0', TITLE='First Principles:<br>Data from Zero',
           SUB='Chapters 1–6: what data is, how computers store and move it, how a business runs on it, numbers without fear, thinking like an analyst, and planning your learning.',
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

JOBS['front'] = lambda: build('front-how-to-use-this-book.md', 'Front-How-to-Use-This-Book', '',
      'How to Use This Book', 'Analyst to Architect · How to Use This Book',
      dict(KICKER='Analyst to Architect', TITLE='How to Use<br>This Book',
           SUB='How each chapter works, how to read the code and its output, the exercises and answers, how the parts climb, and where the companion files are.',
           DOC='', META=''), 2)

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
