"""Export one section of a chapter as a DOCX and a PDF, for review.

The book's usual pipeline is pandoc to HTML then Playwright to PDF, and pandoc is not installed
here. This takes the narrower path: parse the section's Markdown directly, then render it twice,
to HTML (which Playwright prints to PDF) and to a Word document.

It handles only what the question banks actually use: headings, paragraphs with bold, italic and
inline code, fenced code blocks, pipe tables, bullet lists and horizontal rules. It is a review
exporter, not a replacement for the book build.

    python export_section.py <chapter.md> "## 71.11" "## Common mistakes" <out-stem>
"""
import pathlib
import re
import sys

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Inches

# ---------------------------------------------------------------- block parsing

def blocks(md):
    """Split Markdown into (kind, payload) blocks, in order."""
    lines = md.splitlines()
    i = 0
    out = []
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            lang = ln.strip()[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                body.append(lines[i])
                i += 1
            i += 1
            out.append(('code', (lang, '\n'.join(body))))
            continue
        if ln.startswith('#'):
            level = len(ln) - len(ln.lstrip('#'))
            out.append(('head', (level, ln.lstrip('#').strip())))
            i += 1
            continue
        if ln.strip() in ('---', '***', '___'):
            out.append(('rule', None))
            i += 1
            continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i])
                i += 1
            cells = []
            for r in rows:
                if re.fullmatch(r'\|[\s:\-|]+\|?', r.strip()):
                    continue
                parts = re.split(r'(?<!\\)\|', r.strip())
                parts = [p.replace('\\|', '|').strip() for p in parts]
                if parts and parts[0] == '':
                    parts = parts[1:]
                if parts and parts[-1] == '':
                    parts = parts[:-1]
                cells.append(parts)
            if cells:
                out.append(('table', cells))
            continue
        if re.match(r'^\s*[-*]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(re.sub(r'^\s*[-*]\s+', '', lines[i]))
                i += 1
                while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                    items[-1] += ' ' + lines[i].strip()
                    i += 1
            out.append(('list', items))
            continue
        if not ln.strip():
            i += 1
            continue
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('|', '#', '```')) \
                and lines[i].strip() not in ('---',) and not re.match(r'^\s*[-*]\s+', lines[i]) \
                and not lines[i].startswith('**'):
            # a line opening with a bold lead-in starts its own paragraph: the question banks put
            # Likely follow-ups, Red flag and Learn it in on consecutive lines, and running them
            # together loses the structure a reviewer is scanning for
            para.append(lines[i])
            i += 1
        out.append(('para', ' '.join(s.strip() for s in para)))
    return out


CODE = re.compile(r'`([^`]+)`')
EMPH = re.compile(r'(\*\*.+?\*\*|\*.+?\*)', re.S)
SENTINEL = '\u0000CODE%d\u0000'


def spans(text):
    """Split inline text into (style, text) where style is '', 'b', 'i' or 'code'.

    Code spans are lifted out first and replaced by sentinels, because the book's code contains
    asterisks -- `count(*)` and `SELECT *` -- and matching emphasis before protecting the code
    tears those apart. Emphasis is then matched on the protected text and the code put back.
    """
    held = []

    def hold(m):
        held.append(m.group(1))
        return SENTINEL % (len(held) - 1)

    protected = CODE.sub(hold, text)

    pieces = []
    for piece in EMPH.split(protected):
        if not piece:
            continue
        if piece.startswith('**') and piece.endswith('**') and len(piece) > 4:
            pieces.append(('b', piece[2:-2]))
        elif piece.startswith('*') and piece.endswith('*') and len(piece) > 2:
            pieces.append(('i', piece[1:-1]))
        else:
            pieces.append(('', piece))

    out = []
    for style, chunk in pieces:
        parts = re.split(r'\u0000CODE(\d+)\u0000', chunk)
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2:                      # the captured index of a held code span
                out.append(('code', held[int(part)]))
            else:
                out.append((style, part))
    return out


# ---------------------------------------------------------------- HTML

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def inline_html(text):
    bits = []
    for style, t in spans(text):
        t = esc(t)
        bits.append({'': t, 'b': f'<strong>{t}</strong>', 'i': f'<em>{t}</em>',
                     'code': f'<code>{t}</code>'}[style])
    return ''.join(bits)


CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm; }
body { font: 10.5pt/1.5 Georgia, 'Times New Roman', serif; color: #1a1a1a; }
h1 { font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 6pt; }
h2 { font-size: 15pt; margin-top: 22pt; page-break-after: avoid; }
h3 { font-size: 12pt; margin-top: 18pt; background: #f1f1f1; padding: 5pt 7pt;
     border-left: 3pt solid #555; page-break-after: avoid; }
p { margin: 7pt 0; }
code { font: 9pt 'Consolas', 'Courier New', monospace; background: #f4f4f4;
       padding: 0 2pt; border-radius: 2px; }
pre { font: 8.8pt/1.35 'Consolas', 'Courier New', monospace; background: #f7f7f7;
      border: 1px solid #ddd; border-left: 3pt solid #888; padding: 7pt 9pt;
      white-space: pre-wrap; page-break-inside: avoid; margin: 7pt 0; }
pre.out { background: #fcfcf6; border-left-color: #b8a355; }
table { border-collapse: collapse; width: 100%; margin: 9pt 0; font-size: 9pt; }
/* A row never splits, but a long table may continue on the next page with its header repeated:
   keeping whole tables together left half-empty pages wherever a big table followed text. */
tr { page-break-inside: avoid; }
thead { display: table-header-group; }
th, td { border: 1px solid #bbb; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #ececec; }
tr td:first-child { width: 14%; font-weight: bold; }
hr { border: 0; border-top: 1px solid #ccc; margin: 16pt 0; }
ul { margin: 7pt 0 7pt 16pt; }
li { margin: 3pt 0; }
.note { background: #f0f4f8; border-left: 3pt solid #5a7a99; padding: 8pt 10pt; margin: 10pt 0;
        font-size: 9.5pt; }
"""


def to_html(bs, title, note, show_h1=True):
    h = ['<!doctype html><html><head><meta charset="utf-8">',
         f'<title>{esc(title) or "Document"}</title><style>{CSS}</style></head><body>']
    if title and show_h1:
        h.append(f'<h1>{esc(title)}</h1>')
    if note:
        h.append(f'<div class="note">{inline_html(note)}</div>')
    for kind, payload in bs:
        if kind == 'head':
            lvl, t = payload
            h.append(f'<h{min(lvl, 4)}>{inline_html(t)}</h{min(lvl, 4)}>')
        elif kind == 'para':
            h.append(f'<p>{inline_html(payload)}</p>')
        elif kind == 'code':
            lang, body = payload
            cls = ' class="out"' if lang == '' else ''
            h.append(f'<pre{cls}>{esc(body)}</pre>')
        elif kind == 'table':
            rows = payload
            h.append('<table><thead><tr>'
                     + ''.join(f'<th>{inline_html(c)}</th>' for c in rows[0])
                     + '</tr></thead><tbody>')
            for r in rows[1:]:
                h.append('<tr>' + ''.join(f'<td>{inline_html(c)}</td>' for c in r) + '</tr>')
            h.append('</tbody></table>')
        elif kind == 'list':
            h.append('<ul>' + ''.join(f'<li>{inline_html(x)}</li>' for x in payload) + '</ul>')
        elif kind == 'rule':
            h.append('<hr>')
    h.append('</body></html>')
    return '\n'.join(h)


# ---------------------------------------------------------------- DOCX

def mono(run):
    run.font.name = 'Consolas'
    run.font.size = Pt(8.5)
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Consolas')


def add_inline(p, text):
    for style, t in spans(text):
        r = p.add_run(t)
        if style == 'b':
            r.bold = True
        elif style == 'i':
            r.italic = True
        elif style == 'code':
            mono(r)
            r.font.color.rgb = RGBColor(0x8B, 0x20, 0x20)


def to_docx(bs, title, note, path, show_h1=True):
    d = docx.Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(0.8)
    base = d.styles['Normal']
    base.font.name = 'Georgia'
    base.font.size = Pt(10.5)

    if title and show_h1:
        d.add_heading(title, 0)
    if note:
        n = d.add_paragraph()
        add_inline(n, note)
        n.paragraph_format.space_after = Pt(14)

    for kind, payload in bs:
        if kind == 'head':
            lvl, t = payload
            hp = d.add_heading('', min(lvl, 4))
            add_inline(hp, t)
        elif kind == 'para':
            add_inline(d.add_paragraph(), payload)
        elif kind == 'code':
            _lang, body = payload
            p = d.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.2)
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.space_after = Pt(5)
            mono(p.add_run(body))
        elif kind == 'table':
            rows = payload
            cols = max(len(r) for r in rows)
            t = d.add_table(rows=0, cols=cols)
            t.style = 'Table Grid'
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for ri, r in enumerate(rows):
                cells = t.add_row().cells
                for ci in range(cols):
                    txt = r[ci] if ci < len(r) else ''
                    para = cells[ci].paragraphs[0]
                    add_inline(para, txt)
                    para.paragraph_format.space_after = Pt(2)
                    if ri == 0:
                        for run in para.runs:
                            run.bold = True
        elif kind == 'list':
            for item in payload:
                p = d.add_paragraph(style='List Bullet')
                add_inline(p, item)
        elif kind == 'rule':
            p = d.add_paragraph('_' * 60)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.save(path)


# ---------------------------------------------------------------- main

if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser(
        description='Export a Markdown file, or one section of it, as HTML and DOCX.')
    ap.add_argument('source', help='the Markdown file')
    ap.add_argument('out_stem', help='output path without an extension')
    ap.add_argument('--start', default=None,
                    help='heading to start at, e.g. "## 71.11"; default is the top of the file')
    ap.add_argument('--stop', default=None,
                    help='heading to stop before; default is the end of the file')
    ap.add_argument('--title', default=None, help='document title')
    ap.add_argument('--note', default=None,
                    help='one paragraph shown in a tinted box under the title (Markdown allowed)')
    ap.add_argument('--no-title', action='store_true',
                    help="do not add a title; the file's own H1 is the title")
    a = ap.parse_args()

    text = pathlib.Path(a.source).read_text(encoding='utf-8')
    i = text.index(a.start) if a.start else 0
    j = text.index(a.stop, i) if a.stop else len(text)
    body = text[i:j]

    title = a.title or pathlib.Path(a.source).stem.replace('-', ' ')
    note = a.note or ''
    # --no-title means the file already opens with its own H1, so do not add a second one.
    # The title still names the document, for the browser tab and the PDF footer.
    show_h1 = not a.no_title

    bs = blocks(body)
    kinds = {}
    for k, _ in bs:
        kinds[k] = kinds.get(k, 0) + 1
    print('blocks parsed:', kinds)

    html_path = pathlib.Path(a.out_stem + '.html')
    html_path.write_text(to_html(bs, title, note, show_h1), encoding='utf-8')
    print('html ->', html_path)

    to_docx(bs, title, note, a.out_stem + '.docx', show_h1)
    print('docx ->', a.out_stem + '.docx')
