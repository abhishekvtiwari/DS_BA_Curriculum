"""Render the front and back sales covers for Book 4, plus an Instagram-sized front.

    python tools/review-export/make_sales_cover.py

Outputs into review/for-abhishek/cover/:
    front-cover.pdf / .png      A4, print
    back-cover.pdf  / .png      A4, print
    instagram-front.png         1080 x 1350, feed-ready

This is deliberately separate from tools/pdf/build.py. That script puts a plain internal cover
on all 85 chapter PDFs and every part package; this one makes the two pages that sell the book,
and changing the internal cover is a different decision.

Two notes on the design:

* **Fonts.** Poppins and Lora are named in tools/pdf/cover.html and are not installed on this
  machine, so that cover has been silently falling back to DejaVu. This file uses only fonts
  confirmed present: Bahnschrift for display and figures, Consolas for the technical micro-type,
  Segoe UI for back-cover body text.
* **Claims.** Every number here is counted from the manuscript at run time, not typed. The
  "nothing typed by hand" line is the book's own standard, quoted from
  manuscript/front-how-to-use-this-book.md. No salary, placement, endorsement or accreditation
  claim appears anywhere, and none should be added.
"""
import glob
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOOK = ROOT / 'Data Science' / 'Analyst-to-Architect'
MAN = BOOK / 'manuscript'
OUT = ROOT / 'review' / 'for-abhishek' / 'cover'

INK = '#0A0F1C'
INK2 = '#121A2E'
AMBER = '#F4A52A'
AMBER_DIM = '#C98A28'
PAPER = '#F7F5F1'

BANKS = [
    ('69A', 'Why This, Not That: tool choice & judgement'),
    ('70', 'Excel, Google Sheets, VBA & BI'),
    ('71', 'SQL'),
    ('72', 'Python & pandas'),
    ('72A', 'Data Structures & Algorithms'),
    ('72B', 'Data Cleaning & Wrangling'),
    ('73', 'Statistics, Probability & Experimentation'),
    ('74', 'Machine Learning'),
    ('75', 'Product Sense, Metrics & Case Studies'),
    ('76A', 'Data Analyst & Data Scientist'),
    ('76B', 'Business Analyst'),
    ('77', 'Data Engineering & System Design'),
    ('78', 'Automation & Integration'),
    ('79', 'GenAI, LLM & MLOps'),
    ('80', 'Architecture & Leadership'),
    ('81', 'Behavioural, HR & Offer Conversations'),
]


def counts():
    """Count distinct question codes per chapter, from the manuscript."""
    out, codes = {}, []
    for f in glob.glob(str(MAN / 'ch*.md')):
        t = pathlib.Path(f).read_text(encoding='utf-8', errors='replace')
        found = (set(re.findall(r'^### (Q\d+[A-Z]*-\d+)', t, re.M))
                 | set(re.findall(r'^\| (Q\d+[A-Z]*-\d+)', t, re.M)))
        if not found:
            continue
        num = re.match(r'ch(\d+[A-Za-z]?)-', pathlib.Path(f).name).group(1).upper()
        out[num] = len(found)
        codes += sorted(found)
    return out, codes


def pages():
    """Page count of the built Book 4, if it is there."""
    p = ROOT / 'fixed' / 'Books' / 'Analyst-to-Architect-Book-4-Be-Interview-Ready.pdf'
    if not p.exists():
        return None
    try:
        import fitz
        return fitz.open(str(p)).page_count
    except Exception:
        return None


CNT, CODES = counts()
TOTAL = sum(CNT.get(n, 0) for n, _ in BANKS)
PAGES = pages()

# A faint field of real question codes, used as background texture. The rotated block has to
# cover a full A4 diagonal, so the list is cycled until there are enough of them.
_pool = CODES[::7] or ['Q00-000']
TEXTURE = ' &nbsp; '.join((_pool * (1400 // len(_pool) + 1))[:1400])

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:{INK}; }}
.page {{ width:210mm; height:297mm; position:relative; overflow:hidden;
        background:
          radial-gradient(130% 80% at 100% 0%, rgba(244,165,42,.16) 0%, rgba(244,165,42,0) 55%),
          radial-gradient(90% 60% at 0% 100%, rgba(80,130,220,.12) 0%, rgba(80,130,220,0) 60%),
          linear-gradient(170deg, {INK2} 0%, {INK} 62%); }}
.texture {{ position:absolute; left:-18%; top:-14%; width:136%; height:132%;
           font-family:Consolas,monospace; font-size:7.3pt; line-height:2.5; color:#9FB4D8;
           opacity:.05; word-spacing:.16em; letter-spacing:.05em; overflow:hidden;
           transform:rotate(-7deg); pointer-events:none;
           -webkit-mask-image: radial-gradient(120% 95% at 72% 8%, #000 0%, rgba(0,0,0,.55) 48%, rgba(0,0,0,.12) 82%); }}
.inner {{ position:absolute; inset:0; padding:21mm 20mm 18mm; display:flex; flex-direction:column; }}
.rule {{ width:17mm; height:3.2px; background:{AMBER}; border-radius:2px; }}
.top {{ display:flex; justify-content:space-between; align-items:flex-end;
       font-family:Consolas,monospace; font-size:8.4pt; letter-spacing:.26em;
       text-transform:uppercase; color:#C9D6EC; opacity:.78; margin-top:6mm; }}
h1 {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:700; color:#fff;
     font-size:97pt; line-height:.9; letter-spacing:-.02em; margin:0; }}
h1 .amber {{ color:{AMBER}; }}
.hairline {{ height:1px; background:linear-gradient(90deg,{AMBER} 0%, rgba(244,165,42,.08) 76%, transparent 100%);
            margin:7mm 0 0; }}
.badge {{ display:flex; align-items:baseline; gap:5mm; margin-top:7mm; }}
.big {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:700; font-size:78pt;
       color:{AMBER}; line-height:.86; letter-spacing:-.03em; }}
.bword {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:600; font-size:17pt;
         color:#fff; letter-spacing:.21em; text-transform:uppercase; line-height:1.25; }}
.bsub {{ font-family:Consolas,monospace; font-size:8.6pt; letter-spacing:.17em; color:#9FB4D8;
        text-transform:uppercase; margin-top:1.6mm; }}
.skills {{ font-family:Consolas,monospace; font-size:9.3pt; line-height:2.05; letter-spacing:.14em;
          color:#C9D6EC; opacity:.80; text-transform:uppercase; }}
.skills b {{ color:{AMBER}; font-weight:400; }}
.foot {{ display:flex; justify-content:space-between; align-items:flex-end;
        font-family:Consolas,monospace; font-size:8.4pt; letter-spacing:.13em; color:#8FA4C6; }}
.foot .r {{ text-align:right; }}
.spacer {{ flex:1 1 auto; }}
"""

BACK_CSS = f"""
h2 {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:700; color:#fff; font-size:25pt;
     line-height:1.1; letter-spacing:-.012em; margin:0 0 4.5mm; }}
h2 .amber {{ color:{AMBER}; }}
.lede {{ font-family:"Segoe UI",sans-serif; font-size:10.1pt; line-height:1.56; color:#D7E0EF;
        max-width:152mm; margin:0 0 6mm; }}
.lede b {{ color:#fff; font-weight:600; }}
.cols {{ display:flex; gap:9mm; }}
.card {{ background:rgba(255,255,255,.045); border:1px solid rgba(255,255,255,.10);
        border-radius:3.2px; padding:6mm 6.5mm; }}
.card h3 {{ font-family:Consolas,monospace; font-size:8.2pt; letter-spacing:.22em; color:{AMBER};
          text-transform:uppercase; margin:0 0 4mm; font-weight:400; }}
table {{ width:100%; border-collapse:collapse; font-family:"Segoe UI",sans-serif; font-size:8.9pt; }}
td {{ padding:1.18mm 0; color:#CBD6E8; vertical-align:top; }}
td.n {{ text-align:right; font-family:Bahnschrift,sans-serif; font-weight:700; color:{AMBER};
       width:11mm; padding-left:3mm; }}
td.c {{ font-family:Consolas,monospace; font-size:7.6pt; color:#7F93B5; width:12mm; }}
.tot td {{ border-top:1px solid rgba(255,255,255,.17); padding-top:2.6mm; color:#fff;
          font-weight:600; font-size:9.6pt; }}
.tot td.n {{ font-size:13pt; }}
ul {{ margin:0; padding:0; list-style:none; }}
li {{ font-family:"Segoe UI",sans-serif; font-size:9.1pt; line-height:1.47; color:#CBD6E8;
     padding-left:6.5mm; position:relative; margin-bottom:2.7mm; }}
li:before {{ content:"\\2014"; position:absolute; left:0; color:{AMBER}; }}
li b {{ color:#fff; font-weight:600; }}
.note {{ font-family:"Segoe UI",sans-serif; font-size:8.9pt; line-height:1.55; color:#9FB0CA;
        border-left:2px solid {AMBER_DIM}; padding:1mm 0 1mm 5mm; margin-top:1mm; }}
.note b {{ color:#D7E0EF; font-weight:600; }}
.series {{ display:flex; gap:3.4mm; margin-top:7mm; }}
.bk {{ flex:1; border:1px solid rgba(255,255,255,.14); border-radius:3px; padding:3.4mm 4mm;
      font-family:Consolas,monospace; font-size:7.7pt; letter-spacing:.09em; color:#8FA4C6; }}
.bk.on {{ border-color:{AMBER}; background:rgba(244,165,42,.11); color:#fff; }}
.bk span {{ display:block; color:{AMBER}; font-size:7pt; letter-spacing:.2em; margin-bottom:1.3mm; }}
.isbn {{ margin-top:auto; padding-top:6mm; display:flex; justify-content:space-between;
        align-items:flex-end; gap:8mm; }}
.ph {{ width:44mm; height:17mm; border:1px dashed rgba(255,255,255,.28); border-radius:2px;
      display:flex; align-items:center; justify-content:center; font-family:Consolas,monospace;
      font-size:6.8pt; letter-spacing:.14em; color:#7F93B5; text-align:center; line-height:1.5; }}
"""


def front():
    skills = ('SQL &middot; PYTHON &amp; PANDAS &middot; EXCEL, SHEETS &amp; BI &middot; STATISTICS<br>'
              'MACHINE LEARNING &middot; DATA ENGINEERING &middot; DSA &middot; GENAI &amp; MLOPS<br>'
              'BUSINESS ANALYSIS &middot; PRODUCT SENSE &middot; <b>BEHAVIOURAL, HR &amp; OFFERS</b>')
    pg = f'PART 8 &middot; {PAGES} PAGES' if PAGES else 'PART 8'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="page"><div class="texture">{TEXTURE}</div><div class="inner">
  <div class="rule"></div>
  <div class="top"><span>Analyst to Architect</span><span>Book Four</span></div>
  <div class="spacer" style="flex:1.15"></div>
  <h1>Be Interview<br><span class="amber">Ready</span></h1>
  <div class="hairline"></div>
  <div class="badge">
    <div class="big">{TOTAL:,}</div>
    <div><div class="bword">Questions</div>
         <div class="bsub">Across sixteen banks &middot; levels and roles on every one</div></div>
  </div>
  <div class="spacer" style="flex:0.5"></div>
  <div class="skills">{skills}</div>
  <div class="hairline" style="margin:7mm 0 5mm"></div>
  <div class="foot"><span>Every output was run.<br>Nothing was typed by hand.</span>
    <span class="r">{pg}</span></div>
</div></div></body></html>"""


def back():
    rows = ''
    for num, name in BANKS:
        rows += (f'<tr><td class="c">{num}</td><td>{name}</td>'
                 f'<td class="n">{CNT.get(num, 0)}</td></tr>')
    rows += (f'<tr class="tot"><td class="c"></td><td>Total</td>'
             f'<td class="n">{TOTAL:,}</td></tr>')
    built = [
        '<b>A one-line answer</b> you can recall under pressure, then a tier table: what passes, '
        'what is strong, and what earns the extra points.',
        '<b>A level and the roles</b> that ask it &mdash; Fresher, Mid or Senior, for analyst, '
        'scientist, engineer, BA and architect tracks.',
        '<b>The likely follow-ups</b> and the <b>red flag</b> that loses the room.',
        '<b>Where to learn it</b>, naming the chapter and section that teaches the idea.',
        '<b>Take-home assignments and mock interviews</b> to run end to end.',
    ]
    bks = [('One', 'Theory'), ('Two', 'Practical'), ('Three', 'Implementation'), ('Four', 'Be Interview Ready')]
    series = ''.join(
        f'<div class="bk{" on" if n == "Four" else ""}"><span>Book {n}</span>{t}</div>'
        for n, t in bks)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}{BACK_CSS}</style></head><body>
<div class="page"><div class="texture">{TEXTURE}</div>
<div class="inner" style="padding:17mm 18mm 15mm">
  <div class="rule"></div>
  <div class="top" style="margin-bottom:7mm"><span>Analyst to Architect &middot; Book Four</span>
    <span>Part 8</span></div>

  <h2>{TOTAL:,} questions.<br>Worked answers.<br><span class="amber">Nothing typed by hand.</span></h2>

  <p class="lede">Most interview books give you a question and a paragraph. This one gives you the
  answer at three levels &mdash; what gets you through, what makes you strong, and what earns the
  extra point &mdash; because the gap between a pass and an offer is usually not knowledge, it is
  how the answer is built. <b>Every code output in this book was produced by running it.</b></p>

  <div class="cols" style="flex:0 1 auto">
    <div class="card" style="flex:1.04">
      <h3>What is inside</h3>
      <table>{rows}</table>
    </div>
    <div class="card" style="flex:1; display:flex; flex-direction:column">
      <h3>Every question gives you</h3>
      <ul>{''.join(f'<li>{b}</li>' for b in built)}</ul>
      <div class="note" style="margin-top:auto">
        <b>Who it is for.</b> Anyone preparing for a data interview in India &mdash; analyst, data
        scientist, data engineer, analytics engineer or business analyst &mdash; from a first job to
        a senior move.<br><br>
        <b>What it does not do.</b> It makes no promise about salaries, placements or outcomes, and
        it names no employer. It is a question bank and a method, and the work is still yours.
      </div>
    </div>
  </div>

  <div class="series">{series}</div>

  <div class="isbn">
    <div style="font-family:Consolas,monospace; font-size:7.6pt; letter-spacing:.12em; color:#7F93B5; line-height:1.85">
      ANALYST TO ARCHITECT &middot; BOOK FOUR OF FOUR<br>
      PART 8 &middot; CHAPTERS 68&ndash;83{f' &middot; {PAGES} PAGES' if PAGES else ''}
    </div>
    <div class="ph">ISBN / BARCODE<br>PLACEHOLDER</div>
  </div>
</div></div></body></html>"""


def render(html, stem):
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / f'{stem}.html'
    src.write_text(html, encoding='utf-8')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=3)
        pg.goto(src.resolve().as_uri())
        pg.wait_for_timeout(450)
        pg.pdf(path=str(OUT / f'{stem}.pdf'), width='210mm', height='297mm',
               print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        pg.screenshot(path=str(OUT / f'{stem}.png'), clip={'x': 0, 'y': 0, 'width': 794, 'height': 1123})
        b.close()
    print(f'  {stem}.pdf / {stem}.png')


IG_CSS = f"""
@page {{ size: 1080px 1350px; margin:0; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:{INK}; }}
.ig {{ width:1080px; height:1350px; position:relative; overflow:hidden; display:flex;
      flex-direction:column; padding:84px 76px 72px;
      background:
        radial-gradient(130% 80% at 100% 0%, rgba(244,165,42,.18) 0%, rgba(244,165,42,0) 55%),
        radial-gradient(90% 60% at 0% 100%, rgba(80,130,220,.13) 0%, rgba(80,130,220,0) 60%),
        linear-gradient(170deg, {INK2} 0%, {INK} 62%); }}
.ig .texture {{ position:absolute; left:-18%; top:-14%; width:136%; height:132%;
      font-family:Consolas,monospace; font-size:13px; line-height:2.5; color:#9FB4D8;
      opacity:.055; word-spacing:3px; letter-spacing:.5px; overflow:hidden;
      transform:rotate(-7deg); pointer-events:none;
      -webkit-mask-image: radial-gradient(120% 95% at 72% 8%, #000 0%, rgba(0,0,0,.55) 48%, rgba(0,0,0,.12) 82%); }}
.ig .rule {{ width:76px; height:5px; background:{AMBER}; border-radius:3px; }}
.ig .top {{ display:flex; justify-content:space-between; font-family:Consolas,monospace;
      font-size:16px; letter-spacing:4.4px; text-transform:uppercase; color:#C9D6EC;
      opacity:.8; margin-top:22px; }}
.ig h1 {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:700; color:#fff;
      font-size:163px; line-height:.88; letter-spacing:-3px; margin:0; }}
.ig h1 .amber {{ color:{AMBER}; }}
.ig .hairline {{ height:2px; margin-top:34px;
      background:linear-gradient(90deg,{AMBER} 0%, rgba(244,165,42,.08) 76%, transparent 100%); }}
.ig .badge {{ display:flex; align-items:baseline; gap:22px; margin-top:30px; }}
.ig .big {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:700; font-size:136px;
      color:{AMBER}; line-height:.84; letter-spacing:-5px; }}
.ig .bword {{ font-family:Bahnschrift,"Segoe UI",sans-serif; font-weight:600; font-size:34px;
      color:#fff; letter-spacing:7px; text-transform:uppercase; }}
.ig .bsub {{ font-family:Consolas,monospace; font-size:15px; letter-spacing:2.6px; color:#9FB4D8;
      text-transform:uppercase; margin-top:9px; }}
.ig .skills {{ font-family:Consolas,monospace; font-size:17px; line-height:2.0; letter-spacing:2.2px;
      color:#C9D6EC; opacity:.82; text-transform:uppercase; }}
.ig .skills b {{ color:{AMBER}; font-weight:400; }}
.ig .foot {{ display:flex; justify-content:space-between; align-items:flex-end;
      font-family:Consolas,monospace; font-size:15px; letter-spacing:2px; color:#8FA4C6;
      line-height:1.75; }}
.ig .sp {{ flex:1 1 auto; }}
"""


def instagram():
    skills = ('SQL &middot; PYTHON &middot; EXCEL &amp; BI &middot; STATISTICS &middot; ML<br>'
              'DATA ENGINEERING &middot; DSA &middot; GENAI &middot; BUSINESS ANALYSIS<br>'
              '<b>BEHAVIOURAL, HR &amp; OFFER CONVERSATIONS</b>')
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{CSS}{IG_CSS}</style></head><body>
<div class="ig"><div class="texture">{TEXTURE}</div>
  <div class="rule"></div>
  <div class="top"><span>Analyst to Architect</span><span>Book Four</span></div>
  <div class="sp" style="flex:.85"></div>
  <h1>Be Interview<br><span class="amber">Ready</span></h1>
  <div class="hairline"></div>
  <div class="badge">
    <div class="big">{TOTAL:,}</div>
    <div><div class="bword">Questions</div>
         <div class="bsub">Across sixteen banks</div></div>
  </div>
  <div class="sp" style="flex:.55"></div>
  <div class="skills">{skills}</div>
  <div class="hairline" style="margin-top:28px"></div>
  <div class="foot" style="margin-top:22px">
    <span>Every output was run.<br>Nothing was typed by hand.</span>
    <span style="text-align:right">PART 8<br>{PAGES} PAGES</span></div>
</div></body></html>"""


def render_ig():
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / 'instagram-front.html'
    src.write_text(instagram(), encoding='utf-8')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        pg.goto(src.resolve().as_uri())
        pg.wait_for_timeout(420)
        pg.screenshot(path=str(OUT / 'instagram-front.png'),
                      clip={'x': 0, 'y': 0, 'width': 1080, 'height': 1350})
        b.close()
    print('  instagram-front.png  1080x1350')


if __name__ == '__main__':
    print(f'counted {TOTAL:,} questions across {len(BANKS)} banks'
          + (f', Book 4 is {PAGES} pages' if PAGES else ''))
    render(front(), 'front-cover')
    render(back(), 'back-cover')
    render_ig()
    print('->', OUT)
