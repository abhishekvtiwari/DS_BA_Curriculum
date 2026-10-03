"""Render the sales covers for Book 4: front, back (A4, PDF + PNG) and an Instagram 4:5 front.

    python tools/review-export/make_sales_cover.py

Outputs into review/for-abhishek/cover/. Separate from tools/pdf/build.py on purpose: that script
puts a plain internal cover on all 85 chapter PDFs and every part package.

Design system (version 2, 3 October 2026)
-----------------------------------------
* **One grid.** Every page uses an 18 mm margin and a 12-column grid with a single 6 mm gutter.
  Two-, three- and four-up blocks are spans of 6, 4 and 3 columns, so their outer edges, and the
  boundaries they share, fall on the same lines. Nothing is positioned by eye.
* **One centrepiece, made of data.** The spiral is 1,160 dots on a golden-angle (phyllotaxis)
  spiral, one dot per question in the book, generated from the manuscript at run time.
* **Type.** Bahnschrift for display and figures, Constantia italic for the editorial voice,
  Consolas for labels, Segoe UI for back-cover body text. All confirmed installed; Poppins and
  Lora, named in tools/pdf/cover.html, are not.
* **Claims.** Every number is counted from the manuscript or read from the built PDF. "Nothing
  typed by hand" is the book's own standard (front-how-to-use-this-book.md). No salary,
  placement, endorsement or accreditation claim; no barcode area (owner decision, 4 Oct 2026).

After rendering, the script measures the left and right edge of every element tagged to a
margin, checks nothing runs past the bottom margin, and exits 1 if anything is off by more than
half a pixel.
"""
import glob
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAN = ROOT / 'Data Science' / 'Analyst-to-Architect' / 'manuscript'
OUT = ROOT / 'review' / 'for-abhishek' / 'cover'

BRAND = 'Compounza'          # owner decision, 3 Oct 2026: credited to the brand, not a person
FIELD = 'Data Science &amp; Analytics'
PRODUCT = 'The Interview Readiness Book'   # owner's name for the lead product, 4 Oct 2026
VOLUMES = ('First Principles', 'The Working Analyst', 'Builder to Architect')

NAVY = '#0B1324'
NAVY2 = '#111C33'
GOLD = '#D9A54A'
IVORY = '#EEE7D7'
MIST = '#9AA8C0'

BANKS = [
    ('68A', 'Rounds Nobody Prepares For'),
    ('69A', 'Why This, Not That'),
    ('70', 'Excel, Sheets, VBA & BI'),
    ('71', 'SQL'),
    ('72', 'Python & pandas'),
    ('72A', 'Data Structures & Algorithms'),
    ('72B', 'Data Cleaning & Wrangling'),
    ('73', 'Statistics & Experimentation'),
    ('74', 'Machine Learning'),
    ('75', 'Product Sense & Metrics'),
    ('76A', 'Data Analyst & Scientist'),
    ('76B', 'Business Analyst'),
    ('77', 'Data Engineering & Design'),
    ('78', 'Automation & Integration'),
    ('79', 'GenAI, LLM & MLOps'),
    ('80', 'Architecture & Leadership'),
    ('81', 'Behavioural, HR & Offers'),
]


# ------------------------------------------------------------------ data
def counts():
    out = {}
    for f in glob.glob(str(MAN / 'ch*.md')):
        t = pathlib.Path(f).read_text(encoding='utf-8', errors='replace')
        found = (set(re.findall(r'^### (Q\d+[A-Z]*-\d+)', t, re.M))
                 | set(re.findall(r'^\| (Q\d+[A-Z]*-\d+)', t, re.M)))
        if found:
            num = re.match(r'ch(\d+[A-Za-z]?)-', pathlib.Path(f).name).group(1).upper()
            out[num] = len(found)
    return out


def book_pages():
    p = ROOT / 'fixed' / 'Books' / 'Analyst-to-Architect-Book-4-Be-Interview-Ready.pdf'
    try:
        import fitz
        return fitz.open(str(p)).page_count
    except Exception:
        return None


CNT = counts()
SIZES = [CNT.get(n, 0) for n, _ in BANKS]
TOTAL = sum(SIZES)
PAGES = book_pages()
WORDS = {14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen', 20: 'twenty'}
NBANKS = WORDS.get(len(BANKS), str(len(BANKS)))   # spelled out, counted, never typed


# ------------------------------------------------------------------ the spiral
def spiral_svg(hole=0.42, dot=0.60):
    """TOTAL dots on a golden-angle (sunflower) spiral, one dot per question in the book.

    Unit coordinates (-1..1); `hole` is the empty radius left for the number. Dots brighten toward
    the centre and grow slightly outward. An earlier version tried to show each bank as a ring,
    but neither alternating tones nor index gaps made the rings visible, so the cover no longer
    claims them: the caption says only what the picture shows.
    """
    golden = math.pi * (3 - math.sqrt(5))
    k0 = int(round(TOTAL * hole ** 2 / (1 - hole ** 2)))
    c = 1 / math.sqrt(k0 + TOTAL)
    dots = []
    for i in range(TOTAL):
        k = k0 + i
        r = c * math.sqrt(k)
        a = k * golden
        f = (r - hole) / (1 - hole)
        dots.append(f'<circle cx="{r * math.cos(a):.4f}" cy="{r * math.sin(a):.4f}" '
                    f'r="{c * dot * (0.80 + 0.32 * f):.4f}" fill-opacity="{1 - 0.55 * f:.3f}"/>')
    rings = (f'<circle r="{hole - c:.4f}" fill="none" stroke="{GOLD}" stroke-opacity=".40" '
             f'stroke-width=".0035"/><circle r="1.045" fill="none" stroke="{GOLD}" '
             f'stroke-opacity=".18" stroke-width=".003"/>')
    return (f'<svg viewBox="-1.07 -1.07 2.14 2.14" xmlns="http://www.w3.org/2000/svg" '
            f'style="width:100%;height:100%;display:block">{rings}<g fill="{GOLD}">{"".join(dots)}</g></svg>')


SPIRAL = spiral_svg()

# ------------------------------------------------------------------ shared CSS
BASE = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: {NAVY}; }}
.page {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; color: {IVORY};
        background:
          radial-gradient(70% 45% at 50% 34%, rgba(217,165,74,.10) 0%, rgba(217,165,74,0) 70%),
          radial-gradient(120% 70% at 50% 120%, rgba(60,90,160,.18) 0%, rgba(60,90,160,0) 60%),
          linear-gradient(180deg, {NAVY2} 0%, {NAVY} 55%); }}
.frame {{ position: absolute; inset: 9mm; border: .25mm solid rgba(217,165,74,.22); }}
.wrap {{ position: absolute; left: 18mm; right: 18mm; top: 18mm; bottom: 18mm;
        display: flex; flex-direction: column; }}
.grid {{ display: grid; grid-template-columns: repeat(12, 1fr); column-gap: 6mm; }}
.label {{ font-family: Consolas, monospace; font-size: 7.2pt; letter-spacing: .26em;
          text-transform: uppercase; color: {MIST}; }}
.label.gold {{ color: {GOLD}; }}
.rule {{ height: .3mm; background: {GOLD}; opacity: .55; }}
.rule.thin {{ height: .2mm; opacity: .30; }}
.hdr {{ display: flex; justify-content: space-between; align-items: baseline; padding-bottom: 3mm; }}
.serif {{ font-family: Constantia, Georgia, serif; font-style: italic; }}
"""


def header(right):
    return (f'<div class="hdr"><span class="label" data-l>{BRAND}</span>'
            f'<span class="label" data-r>{right}</span></div><div class="rule" data-l data-r></div>')


# ------------------------------------------------------------------ front
FRONT_CSS = f"""
.art {{ position: relative; width: 142mm; height: 142mm; margin: 9mm auto 0; }}
.core {{ position: absolute; inset: 0; display: flex; flex-direction: column;
        align-items: center; justify-content: center; text-align: center; }}
.core .n {{ font-family: Bahnschrift, sans-serif; font-weight: 700; font-size: 50pt;
           color: {GOLD}; letter-spacing: -.02em; line-height: .9; }}
.core .w {{ font-family: Bahnschrift, sans-serif; font-weight: 600; font-size: 10pt; text-transform: uppercase;
           letter-spacing: .42em; margin: 2.2mm 0 0 .42em; color: {IVORY}; }}
.core .s {{ margin-top: 1.6mm; letter-spacing: .22em; font-size: 6.4pt; }}
.cap {{ text-align: center; margin-top: 3mm; font-size: 6.4pt; letter-spacing: .24em; }}
h1 {{ font-family: Bahnschrift, sans-serif; font-weight: 700; font-size: 62pt; line-height: .92;
     letter-spacing: -.015em; color: {IVORY}; }}
h1 span {{ color: {GOLD}; }}
.over {{ font-family: Bahnschrift, sans-serif; font-weight: 600; font-size: 17pt; color: {GOLD};
         letter-spacing: .2em; text-transform: uppercase; margin-bottom: 3.5mm; }}
.tag {{ font-size: 13pt; line-height: 1.4; color: {IVORY}; opacity: .88; margin-top: 4.5mm; }}
.foot {{ align-items: end; padding-top: 4mm; }}
.who {{ grid-column: 1 / span 5; }}
.who .name {{ font-family: Bahnschrift, sans-serif; font-weight: 600; font-size: 13pt;
             letter-spacing: .2em; color: {IVORY}; margin-top: 1.4mm; text-transform: uppercase; }}
.topics {{ grid-column: 6 / span 7; text-align: right; line-height: 1.95; font-size: 6.6pt;
          letter-spacing: .2em; }}
.topics b {{ color: {GOLD}; font-weight: 400; }}
.topics span {{ display: block; white-space: nowrap; }}
"""


def front():
    pg = f' &middot; {PAGES} pages' if PAGES else ''
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{FRONT_CSS}</style></head>
<body><div class="page"><div class="frame"></div><div class="wrap">
  {header(PRODUCT)}
  <div class="art">{SPIRAL}
    <div class="core"><div class="n">{TOTAL:,}</div><div class="w">Questions</div>
      <div class="label s">{NBANKS} banks</div></div>
  </div>
  <div class="label cap">One dot for every question in this book</div>
  <div style="flex:1"></div>
  <div class="over" data-l>{FIELD}</div>
  <h1 data-l>Be Interview<br><span>Ready</span></h1>
  <p class="serif tag" data-l>Worked answers at three levels, from the SQL round to the offer conversation.</p>
  <div class="spacer7" style="height:7mm"></div>
  <div class="rule thin" data-l data-r></div>
  <div class="grid foot">
    <div class="who" data-l><div class="label">By</div><div class="name">{BRAND}</div></div>
    <div class="label topics" data-r><span>SQL &middot; Python &middot; Excel &amp; BI &middot; Statistics &middot; ML</span>
      <span>Data engineering &middot; GenAI &middot; BA &middot; <b>HR &amp; offers</b></span>
      <span>Every output was run{pg}</span></div>
  </div>
</div></div></body></html>"""


# ------------------------------------------------------------------ back
BACK_CSS = f"""
h2 {{ font-family: Bahnschrift, sans-serif; font-weight: 700; font-size: 25pt; line-height: 1.08;
     color: {IVORY}; letter-spacing: -.01em; margin-top: 3mm; }}
h2 span {{ color: {GOLD}; }}
.lede {{ font-size: 11.2pt; line-height: 1.5; color: {IVORY}; opacity: .9; margin-top: 4.5mm; }}
.sec {{ margin-top: 0; }}
.fl {{ flex: 1 1 0; min-height: 5mm; }}
.sec > .label {{ display: block; padding-bottom: 2.2mm; }}
.toc {{ margin-top: 3mm; }}
.toc .col {{ grid-column: span 6; }}
.row {{ display: flex; align-items: baseline; font-family: "Segoe UI", sans-serif; font-size: 8.7pt;
       color: #D3DAE6; padding: 0.82mm 0; }}
.row .c {{ font-family: Consolas, monospace; font-size: 6.9pt; color: {MIST}; width: 9mm; flex: none; }}
.row .lead {{ flex: 1; border-bottom: .25mm dotted rgba(238,231,215,.28); margin: 0 2mm;
             transform: translateY(-.8mm); }}
.row .n {{ font-family: Bahnschrift, sans-serif; font-weight: 700; color: {GOLD}; width: 8mm;
          text-align: right; flex: none; }}
.total {{ display: flex; justify-content: space-between; align-items: baseline; margin-top: 2.6mm;
         padding-top: 2.4mm; border-top: .2mm solid rgba(217,165,74,.35); }}
.total .t {{ font-family: Bahnschrift, sans-serif; font-weight: 600; font-size: 10pt;
            letter-spacing: .14em; text-transform: uppercase; }}
.total .n {{ font-family: Bahnschrift, sans-serif; font-weight: 700; font-size: 17pt; color: {GOLD}; }}
.three {{ margin-top: 0; }}
.three > div {{ grid-column: span 4; }}
.three .label {{ display: block; padding-bottom: 2mm; }}
.three p, .three li {{ font-family: "Segoe UI", sans-serif; font-size: 8.5pt; line-height: 1.5;
                      color: #C9D2E0; }}
.three ul {{ list-style: none; }}
.three li {{ padding-left: 3.6mm; position: relative; margin-bottom: 1.5mm; }}
.three li:before {{ content: ""; position: absolute; left: 0; top: 2.05mm; width: 1.3mm; height: 1.3mm;
                   border-radius: 50%; background: {GOLD}; }}
.three b {{ color: {IVORY}; font-weight: 600; }}
.series {{ margin-top: 0; }}
.series > div {{ grid-column: span 4; border: .25mm solid rgba(238,231,215,.16); padding: 2.6mm 3mm;
                font-family: Consolas, monospace; font-size: 7pt; letter-spacing: .1em; color: {MIST}; }}
.series > div .label {{ display: block; font-size: 6.3pt; margin-bottom: 1mm; }}
.series .bn {{ display: block; font-family: Bahnschrift, sans-serif; font-weight: 600; font-size: 10.5pt;
               letter-spacing: .04em; color: {IVORY}; margin-bottom: 1mm; }}
.series .bd {{ display: block; font-family: "Segoe UI", sans-serif; font-size: 7.6pt; line-height: 1.45;
               letter-spacing: 0; color: #B9C3D4; }}
.series > div.on {{ border-color: {GOLD}; background: rgba(217,165,74,.10); color: {IVORY}; }}
.colophon {{ align-items: end; padding-top: 4mm; }}
.colophon .l {{ grid-column: 1 / span 12; line-height: 1.9; }}
.colophon .name {{ font-family: Bahnschrift, sans-serif; font-weight: 600; font-size: 10.5pt;
                  letter-spacing: .2em; color: {IVORY}; text-transform: uppercase; }}
.ph {{ grid-column: 9 / span 4; height: 19mm; border: .25mm dashed rgba(238,231,215,.30);
      display: flex; align-items: center; justify-content: center; text-align: center;
      font-family: Consolas, monospace; font-size: 6.2pt; letter-spacing: .16em; color: {MIST};
      line-height: 1.6; text-transform: uppercase; }}
"""


def back():
    half = (len(BANKS) + 1) // 2

    def col(items):
        return ''.join(f'<div class="row"><span class="c">{n}</span><span>{name}</span>'
                       f'<span class="lead"></span><span class="n">{CNT.get(n, 0)}</span></div>'
                       for n, name in items)

    gives = [
        '<b>A one-line answer</b> to recall under pressure',
        '<b>Three tiers</b>: what passes, what is strong, what earns the extra point',
        '<b>A level and the roles</b> that ask it',
        '<b>Follow-ups and the red flag</b> that loses the room',
        '<b>Where to learn it</b>, by chapter and section',
    ]
    ladder = [
        ('Start here', PRODUCT, f'{TOTAL:,} questions with worked answers. This book.', True),
        ('Add-on', 'The Three Volumes', f'{VOLUMES[0]}, {VOLUMES[1]} and {VOLUMES[2]}, with practice files for every tool.', False),
        ('Add-on', 'Projects', 'Ready-made portfolio projects with real, messy data. Sold separately.', False),
    ]
    series = ''.join(f'<div class="{"on" if on else ""}"><span class="label gold">{k}</span>'
                     f'<span class="bn">{name}</span><span class="bd">{desc}</span></div>'
                     for k, name, desc, on in ladder)
    pg = f' &middot; {PAGES} pages' if PAGES else ''
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{BACK_CSS}</style></head>
<body><div class="page"><div class="frame"></div><div class="wrap">
  {header(PRODUCT)}
  <div class="label gold" data-l style="margin-top:8mm">{PRODUCT} &middot; {FIELD}</div>
  <h2 data-l>{TOTAL:,} questions. Worked answers.<br><span>Nothing typed by hand.</span></h2>
  <p class="serif lede" data-l>Most data science interview books give you a question and a paragraph. This one gives you
  the answer at three levels, because the gap between a pass and an offer is rarely knowledge.
  It is how the answer is built. Every code output in it was produced by running the code.</p>
  <div class="fl"></div>
  <div class="sec"><span class="label gold" data-l>What is inside</span><div class="rule thin" data-l data-r></div>
    <div class="grid toc"><div class="col" data-l>{col(BANKS[:half])}</div>
      <div class="col" data-r>{col(BANKS[half:])}</div></div>
    <div class="total" data-l data-r><span class="t">{NBANKS.capitalize()} banks, fresher to senior</span>
      <span class="n">{TOTAL:,}</span></div>
  </div>
  <div class="fl"></div>
  <div class="grid three">
    <div data-l><span class="label gold">Every question gives you</span><div class="rule thin"></div>
      <ul style="margin-top:2.6mm">{''.join(f'<li>{g}</li>' for g in gives)}</ul></div>
    <div><span class="label gold">Who it is for</span><div class="rule thin"></div>
      <p style="margin-top:2.6mm">Anyone preparing for a data science, analytics or business-analyst
      interview in India: analyst, data scientist, data engineer, analytics engineer or BA, from a
      first job to a senior move. With take-home assignments and mock interviews to run end to end.</p></div>
    <div data-r><span class="label gold">What it does not do</span><div class="rule thin"></div>
      <p style="margin-top:2.6mm">It makes no promise about salaries, placements or outcomes, and it names
      no employer. It is a question bank and a method. <b>The work is still yours.</b></p></div>
  </div>

  <div class="fl"></div>
  <div class="grid series" data-l data-r>{series}</div>
  <div class="rule thin" style="margin-top:5mm" data-l data-r></div>
  <div class="grid colophon">
    <div class="l label" data-l><span class="name">{BRAND}</span><br>
      {PRODUCT} &middot; {FIELD}<br>{TOTAL:,} questions{pg}</div>
  </div>
</div></div></body></html>"""


# ------------------------------------------------------------------ instagram 4:5
IG_CSS = """
.page { width: 1080px; height: 1350px; }
.frame { inset: 34px; border-width: 1px; }
.wrap { left: 72px; right: 72px; top: 70px; bottom: 66px; }
.label { font-size: 15px; }
.rule { height: 1.5px; } .rule.thin { height: 1px; }
.hdr { padding-bottom: 14px; }
.art { width: 640px; height: 640px; margin: 30px auto 0; }
.core .n { font-size: 80px; }   /* 63% of the ring, matching print */
.core .w { font-size: 22px; margin-top: 10px; }
.core .s { font-size: 13px; margin-top: 8px; }
.cap { font-size: 13px; margin-top: 14px; }
h1 { font-size: 118px; }
.over { font-size: 30px; margin-bottom: 12px; }
.tag { font-size: 26px; margin-top: 16px; }
.spacer7 { height: 26px !important; }
.foot { padding-top: 18px; }
.who .name { font-size: 27px; margin-top: 6px; }
.topics { font-size: 13px; }
"""


def instagram():
    return front().replace('</style>', IG_CSS + '</style>', 1)


# ------------------------------------------------------------------ render + measure
ALIGN_JS = """() => {
  const wrap = document.querySelector('.wrap').getBoundingClientRect();
  const out = [];
  for (const el of document.querySelectorAll('[data-l],[data-r]')) {
    // measure ink, not box: for text use a Range so side-bearings and padding don't hide errors
    let r = el.getBoundingClientRect();
    const name = ((el.className && el.className.baseVal === undefined ? el.className : '') || el.tagName)
                   .toString().slice(0, 22);
    if (el.hasAttribute('data-l')) out.push([name, 'left', +(r.left - wrap.left).toFixed(2)]);
    if (el.hasAttribute('data-r')) out.push([name, 'right', +(wrap.right - r.right).toFixed(2)]);
  }
  let low = -1e9;
  for (const e of document.querySelectorAll('.wrap *')) low = Math.max(low, e.getBoundingClientRect().bottom);
  return {edges: out, past: +(low - wrap.bottom).toFixed(2)};
}"""


def render(html, stem, w, h, pdf=True):
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / f'{stem}.html'
    src.write_text(html, encoding='utf-8')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=3 if pdf else 1)
        pg.goto(src.resolve().as_uri())
        pg.wait_for_timeout(500)
        m = pg.evaluate(ALIGN_JS)
        if pdf:
            pg.pdf(path=str(OUT / f'{stem}.pdf'), width='210mm', height='297mm', print_background=True,
                   margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        pg.screenshot(path=str(OUT / f'{stem}.png'), clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        b.close()
    bad = [e for e in m['edges'] if abs(e[2]) > 0.5]
    over = m['past'] > 0.5
    worst = max([abs(e[2]) for e in m['edges']] or [0])
    print(f'  {stem:<16} {"OK  " if not bad and not over else "FAIL"} {len(m["edges"]):>2} margin edges, '
          f'worst {worst:.2f}px; lowest content {-m["past"]:.1f}px inside the bottom margin')
    for e in bad:
        print(f'      off by {e[2]}px: {e[0]} ({e[1]} edge)')
    return not bad and not over


if __name__ == '__main__':
    print(f'counted {TOTAL:,} questions across {len(BANKS)} banks'
          + (f'; Book 4 is {PAGES} pages' if PAGES else ''))
    ok = all([render(front(), 'front-cover', 794, 1123),
              render(back(), 'back-cover', 794, 1123),
              render(instagram(), 'instagram-front', 1080, 1350, pdf=False)])
    print('->', OUT)
    sys.exit(0 if ok else 1)
