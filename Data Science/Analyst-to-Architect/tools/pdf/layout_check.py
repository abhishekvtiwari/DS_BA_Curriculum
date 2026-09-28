"""Page-quality checks for a built chapter PDF (visual review themes V2, V7, V8, V9, V11, V12).

    python tools/pdf/layout_check.py file.pdf [file2.pdf ...]      # one JSON line per file

Checks, per PDF (page 1 is the cover and is skipped):
  toc_numbers      contents entries that end in a page number / all contents entries (V2)
  map_numbers      the same for the chapter maps, "In this chapter" (D8)
  toc_wrong        contents or map entries whose page number does not show that heading (V2, D8)
  stranded_heads   a heading with no body text after it on its page (V7)
  stranded_leadins the last line on a page ends with ":" and the next page starts with a block (V7)
  sparse_pages     body text ends above 60% of the page, not counting the last page or a page
                   that precedes a new top-level section (V7)
  small_text       body/code/table text below 6.95 pt, outside figures (V12, V8)
  clipped_lists    list numbers starting within 1 pt of the left text edge or beyond it (V9)
  draft_labels     "Draft", "v1.1", "for review", "coordinator", "this chat" on the cover or anywhere (V1)
  tofu             replacement characters (V11)
"""
import sys, re, json, subprocess
import pymupdf

HEAD_FONTS = ('Poppins',)
BODY_LEFT_PT = 18 / 25.4 * 72          # @page left margin
FOOTER_TOP_FRAC = 0.93


def lines_of(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for l in b['lines']:
            spans = [s for s in l['spans'] if s['text'].strip()]
            if not spans:
                continue
            y0 = min(s['bbox'][1] for s in spans); y1 = max(s['bbox'][3] for s in spans)
            x0 = min(s['bbox'][0] for s in spans)
            out.append(dict(y0=y0, y1=y1, x0=x0, text=''.join(s['text'] for s in spans).strip(),
                            font=spans[0]['font'], size=max(s['size'] for s in spans)))
    return sorted(out, key=lambda l: (round(l['y0']), l['x0']))


def check(path):
    doc = pymupdf.open(path)
    H = doc[0].rect.height
    r = dict(file=path.split('/')[-1], pages=len(doc), toc_numbers=None, stranded_heads=[], stranded_leadins=[],
             sparse_pages=[], small_text=[], clipped_lists=[], draft_labels=[], tofu=0)
    body = []
    for i, page in enumerate(doc):
        ls = [l for l in lines_of(page) if l['y0'] < H * FOOTER_TOP_FRAC]
        body.append(ls)
        txt = page.get_text()
        r['tofu'] += txt.count('�')
        for m in re.findall(r'(?i)\b(draft( v?\d[\w.]*)?|v\d+\.\d+|for review|coordinator|this chat)\b', txt):
            r['draft_labels'].append((i + 1, m[0]))
    # contents and chapter maps ("In this chapter", D8): every entry should end in a page number, and
    # the page printed with that number should show the heading. Page numbers are read from each
    # page's footer, because a package numbers its front matter i, ii … and starts 1 at Part 0.
    squash = lambda s: re.sub(r'\s+', '', s)
    PG = r'(\d+|[ivxl]+)'
    printed = {}
    for i, page in enumerate(doc):
        foot = [l for l in lines_of(page) if l['y0'] >= H * FOOTER_TOP_FRAC]
        m = re.search(PG + r'(\s*/\s*\d+)?$', foot[-1]['text']) if foot else None
        if m: printed.setdefault(m.group(1), i)
    if not printed:                      # no footers: page n is the n-th page after the cover
        printed = {str(i): i for i in range(len(doc))}
    def verify(entries_text, kind):
        entries, withnum, wrong = 0, 0, []
        for line in entries_text:
            s = re.sub(r'^(START|LEARN|APPLY|REVIEW|PRACTISE|NEXT)\s+', '', line.strip())
            if not s or s in ('Contents', 'In this chapter') or s.startswith('Analyst to Architect'):
                continue
            entries += 1
            m = re.match(r'(.+?)\s{2,}' + PG + r'$', s)
            if not m:
                continue
            withnum += 1
            title, n = m.group(1), m.group(2)
            key = squash(title.split(' · ')[0])[:25]
            idx = printed.get(n)
            if idx is None or key not in squash(doc[idx].get_text()):
                wrong.append((kind, title[:40], n))
        return entries, withnum, wrong
    lay = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout.split('\f')
    toc_lines, in_toc = [], False
    for k, pg in enumerate(lay[1:6], start=1):
        body_lines = [l for l in pg.splitlines() if l.strip() and not l.strip().startswith('Analyst to Architect')]
        if not body_lines: continue
        if body_lines[0].strip() == 'Contents': in_toc = True
        elif in_toc and sum(bool(re.search(r'\s{2,}' + PG + r'$', l.strip())) for l in body_lines) < 0.7 * len(body_lines):
            break
        if in_toc: toc_lines += body_lines
    e, w, wrong = verify(toc_lines, 'contents')
    r['toc_numbers'] = f"{w}/{e}"
    maps = []
    for pg in lay:
        for part in pg.split('In this chapter')[1:]:
            ls = part.splitlines()
            first = next((l.strip() for l in ls if l.strip()), '')
            if not re.match(r'(START|LEARN)\b', first): continue      # prose that mentions the map
            block = []
            for l in ls:
                if not l.strip(): continue
                block.append(l)
                if l.strip().startswith('NEXT'): break
            maps += block
    me, mw, mwrong = verify(maps, 'map')
    r['map_numbers'] = f"{mw}/{me}"
    r['toc_wrong'] = wrong + mwrong
    for i in range(1, len(body)):
        ls = body[i]
        if not ls:
            continue
        last = ls[-1]
        nxt = body[i + 1] if i + 1 < len(body) else []
        if last['font'].startswith(HEAD_FONTS) and last['size'] >= 10.5 and i + 1 < len(body):
            r['stranded_heads'].append((i + 1, last['text'][:50]))
        if last['text'].endswith(':') and nxt and not nxt[0]['font'].startswith('Lora'):
            r['stranded_leadins'].append((i + 1, last['text'][-50:]))
        bottom = max(l['y1'] for l in ls)
        next_is_h1 = nxt and nxt[0]['font'].startswith(HEAD_FONTS) and nxt[0]['size'] >= 14
        if i > 1 and i + 1 < len(body) and bottom < H * 0.6 and not next_is_h1:
            r['sparse_pages'].append((i + 1, round(bottom / H, 2)))
        for l in ls:
            if l['size'] < 6.95 and not l['font'].startswith(HEAD_FONTS):
                r['small_text'].append((i + 1, round(l['size'], 1), l['text'][:30]))
            if re.match(r'^\d{2}\.(\s|$)', l['text']) and l['x0'] < BODY_LEFT_PT - 0.5:
                r['clipped_lists'].append((i + 1, l['text']))
    r['small_text'] = r['small_text'][:15]
    return r


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(json.dumps(check(f), ensure_ascii=False))
