"""Print a local HTML file to PDF with Playwright, with page numbers in the footer.

    python tools/review-export/html_to_pdf.py <in.html> <out.pdf> ["footer text"]

The footer text defaults to the HTML file's <title>, so a document does not end up carrying
another document's footer.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

import html as _html
import re as _re

src = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()

if len(sys.argv) > 3:
    label = sys.argv[3]
else:
    m = _re.search(r'<title>(.*?)</title>', src.read_text(encoding='utf-8'), _re.S)
    label = _html.unescape(m.group(1)).strip() if m else src.stem.replace('-', ' ')

FOOTER = ('<div style="font:8pt Georgia,serif;color:#666;width:100%;padding:0 18mm;'
          'display:flex;justify-content:space-between;">'
          f'<span>{_html.escape(label)}</span>'
          '<span class="pageNumber"></span></div>')

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto(src.as_uri(), wait_until='load')
    page.pdf(path=str(out), format='A4', print_background=True,
             display_header_footer=True,
             header_template='<div></div>', footer_template=FOOTER,
             margin={'top': '18mm', 'bottom': '18mm', 'left': '16mm', 'right': '16mm'})
    browser.close()

import fitz
d = fitz.open(out)
print(f'pdf -> {out}  ({d.page_count} pages, {out.stat().st_size / 1024:.0f} KB)')
d.close()
