#!/usr/bin/env python3
"""
build_chapter.py - turn a chapter manuscript (.md) into the book's styled PDF (cover + body).

Usage:
  python3 build_chapter.py ../../manuscript/ch03-how-a-business-runs-on-data.md \
      --figures ../../figures --out-dir ../../pdf-out \
      --name Ch03-How-a-Business-Runs-on-Data \
      --part "Part 0 — First Principles" \
      --title "Chapter 3. How a Business Runs on Data" \
      --sub "One-sentence description of the chapter for the cover." \
      --doc "Draft chapter" --meta "16 September 2026<br>Every number checked"

Needs: pandoc, Python packages playwright (with Chromium) and pypdf, and the three files next to this
script: book.css, template.html, cover.html. Chapter titles on the cover may use <br> to break lines.
```mysql fences are rendered with SQL highlighting. HTML comments (markers) are invisible in the PDF.
"""
import argparse, html, pathlib, re, shutil, subprocess, tempfile
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

HERE = pathlib.Path(__file__).resolve().parent

def render(pw, html_path, pdf_path, footer=None):
    b = pw.chromium.launch(); p = b.new_page()
    p.goto(f'file://{html_path}'); p.wait_for_load_state('networkidle'); p.evaluate('document.fonts.ready')
    kw = dict(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
    if footer:
        kw.update(display_header_footer=True, header_template='<div></div>',
                  footer_template=('<div style="width:100%;font-family:DejaVu Sans,sans-serif;font-size:7.5pt;color:#6b7383;'
                                   'padding:0 18mm;display:flex;justify-content:space-between;">'
                                   f'<span>{html.escape(footer)}</span><span><span class="pageNumber"></span> / '
                                   '<span class="totalPages"></span></span></div>'))
    try:
        p.pdf(outline=True, **kw)
    except TypeError:
        p.pdf(**kw)
    b.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('manuscript'); ap.add_argument('--figures', required=True); ap.add_argument('--out-dir', required=True)
    ap.add_argument('--name', required=True); ap.add_argument('--part', required=True); ap.add_argument('--title', required=True)
    ap.add_argument('--sub', required=True); ap.add_argument('--doc', default='Draft chapter'); ap.add_argument('--meta', default='')
    ap.add_argument('--toc-depth', default='2'); ap.add_argument('--author', default='Abhishek Tiwari')
    a = ap.parse_args()
    out = pathlib.Path(a.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    plain_title = re.sub(r'<br>', ' ', a.title).replace('&amp;', '&')
    with tempfile.TemporaryDirectory() as tmp:
        t = pathlib.Path(tmp)
        for f in ('book.css', 'template.html'): shutil.copy(HERE / f, t / f)
        (t / 'figures').symlink_to(pathlib.Path(a.figures).resolve())
        src = pathlib.Path(a.manuscript).read_text(encoding='utf-8')
        (t / 'chapter.md').write_text(re.sub(r'^```mysql$', '```sql', src, flags=re.M), encoding='utf-8')
        subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html5', '-s', '--template', str(t / 'template.html'), '--toc',
                        f'--toc-depth={a.toc_depth}', '-M', f'pagetitle={plain_title}', '-V', 'bodyclass=',
                        str(t / 'chapter.md'), '-o', str(t / 'body.html')], check=True)
        h = (t / 'body.html').read_text(encoding='utf-8')
        (t / 'body.html').write_text(re.sub(r'<blockquote>(\s*<p><strong>Watch out)', r'<blockquote class="warn">\1', h), encoding='utf-8')
        c = (HERE / 'cover.html').read_text(encoding='utf-8')
        for k, v in dict(KICKER=f'Analyst to Architect · {a.part}', TITLE=a.title, SUB=a.sub, DOC=a.doc, META=a.meta).items():
            c = c.replace('{{' + k + '}}', v)
        (t / 'cover.html').write_text(c, encoding='utf-8')
        footer = f'Analyst to Architect · {plain_title.replace(". ", " · ", 1)}'
        with sync_playwright() as pw:
            render(pw, t / 'cover.html', t / 'cover.pdf')
            render(pw, t / 'body.html', t / 'body.pdf', footer)
        w = PdfWriter(); w.append(str(t / 'cover.pdf')); w.append(str(t / 'body.pdf'))
        w.add_metadata({'/Title': plain_title, '/Author': a.author})
        target = out / f'{a.name}.pdf'
        with open(target, 'wb') as f: w.write(f)
    print(target, len(PdfReader(str(target)).pages), 'pages')

if __name__ == '__main__':
    main()
