"""Print a local HTML file to PDF with Playwright, with page numbers in the footer."""
import pathlib
import sys

from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()

FOOTER = ('<div style="font:8pt Georgia,serif;color:#666;width:100%;padding:0 18mm;'
          'display:flex;justify-content:space-between;">'
          '<span>Analyst to Architect &middot; Ch 71 &sect;71.11 &middot; review copy</span>'
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
