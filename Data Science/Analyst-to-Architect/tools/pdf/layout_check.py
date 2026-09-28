"""Page-quality checks for a built chapter PDF (visual review themes V2, V7, V8, V9, V11, V12).

    python tools/pdf/layout_check.py file.pdf [file2.pdf ...]      # one JSON line per file

Checks, per PDF (page 1 is the cover and is skipped):
  toc_numbers      contents entries that end in a page number / all contents entries (V2)
  toc_wrong        contents entries whose page number does not show that heading (V2)
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
    # contents: every entry should end in a page number, and that page should show the heading
    lay = subprocess.run(['pdftotext', '-layout', '-f', '2', '-l', '3', path, '-'], capture_output=True, text=True).stdout
    toc = lay.split('\f')[0] if 'Contents' in lay.split('\f')[0] else ''
    entries, withnum, wrong = 0, 0, []
    squash = lambda s: re.sub(r'\s+', '', s)
    for line in toc.splitlines():
        s = line.strip()
        if not s or s == 'Contents' or s.startswith('Analyst to Architect'):
            continue
        entries += 1
        m = re.match(r'(.+?)\s{2,}(\d+)$', s)
        if not m:
            continue
        withnum += 1
        title, n = m.group(1), int(m.group(2))
        if n >= len(doc) or squash(title)[:25] not in squash(doc[n].get_text()):
            wrong.append((title[:40], n))
    r['toc_numbers'] = f"{withnum}/{entries}"
    r['toc_wrong'] = wrong
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
            if re.match(r'^\d{2}\.$', l['text']) and l['x0'] < BODY_LEFT_PT - 0.5:
                r['clipped_lists'].append((i + 1, l['text']))
    r['small_text'] = r['small_text'][:15]
    return r


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print(json.dumps(check(f), ensure_ascii=False))
