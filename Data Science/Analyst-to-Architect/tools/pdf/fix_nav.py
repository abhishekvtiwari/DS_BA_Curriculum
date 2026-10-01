"""Rebuild a book PDF's navigation from the pristine build, in one pass.

Three things are wrong in the built books and all three are fixed here together, from the
original file rather than by patching a patch:

1. "The whole book" map sits between the cover and the book's own contents. It lists every
   chapter of all four books and carries no links. It moves to the back.

2. Contents entries link by *named destination*. That is valid PDF, but many viewers refuse to
   follow one, so clicking did nothing. Each name is resolved to an explicit page.

3. The destination point is stored in PDF's native space (origin bottom-left, y upward), while
   insert_link expects page space (origin top-left, y downward). Copying it across unconverted
   sent a "top of page" destination to the bottom edge, so the viewer scrolled past onto the
   next page, or landed mid-page. y is converted against the target page's own height.

Link annotations are removed as annotations and re-inserted in one go per page, because deleting
and inserting inside a loop over get_links() invalidates the entries that follow and silently
drops them.

    python rebuild_links.py <original.pdf> <out.pdf>
"""
import sys
import fitz


def map_range(d):
    """0-based (first, last) pages of the whole-book map, or None if this file has none."""
    first = None
    for i in range(0, min(12, d.page_count)):
        line = next((l.strip() for l in d[i].get_text().splitlines() if l.strip()), '')
        if line.startswith('The whole book') and first is None:
            first = i
        elif line.startswith('Contents') and first is not None:
            return first, i - 1
    return None


def rebuild(src, dst):
    d = fitz.open(src)
    n0 = d.page_count
    names = d.resolve_names() or {}
    heights = [p.rect.height for p in d]

    rng = map_range(d)
    if rng:
        a, b = rng
        order = list(range(0, a)) + list(range(b + 1, n0)) + list(range(a, b + 1))
    else:
        order = list(range(n0))
    old_to_new = {o: i for i, o in enumerate(order)}
    moved = (rng[1] - rng[0] + 1) if rng else 0

    # Capture the wanted links per original page, with targets already resolved and converted.
    wanted = {}
    stats = dict(named=0, direct=0, uri=0, dropped=0)
    for i in range(n0):
        out = []
        for l in d[i].get_links():
            k = l['kind']
            if k == fitz.LINK_URI:
                out.append(dict(kind=k, frm=l['from'], uri=l['uri']))
                stats['uri'] += 1
                continue
            if k == fitz.LINK_NAMED:
                t = names.get(l.get('nameddest'))
                if not t:
                    stats['dropped'] += 1
                    continue
                tgt, pt = t['page'], t.get('to')
                stats['named'] += 1
            elif k == fitz.LINK_GOTO:
                tgt, pt = l['page'], (l['to'].x, l['to'].y) if l.get('to') else None
                stats['direct'] += 1
            else:
                stats['dropped'] += 1
                continue
            if not (0 <= tgt < n0):
                stats['dropped'] += 1
                continue
            H = heights[tgt]
            y = None if pt is None else max(0.0, min(H - 1.0, H - pt[1]))
            out.append(dict(kind=fitz.LINK_GOTO, frm=l['from'], tgt=tgt,
                            x=0.0 if pt is None else pt[0], y=y))
        wanted[i] = out

    toc = d.get_toc()

    if moved:
        d.select(order)

    written = 0
    for new_i in range(d.page_count):
        page = d[new_i]
        while True:                      # link annots are not returned by page.annots();
            ls = page.get_links()        # delete the first repeatedly so no handle goes stale
            if not ls:
                break
            page.delete_link(ls[0])
        for w in wanted[order[new_i]]:
            if w['kind'] == fitz.LINK_URI:
                page.insert_link({'kind': fitz.LINK_URI, 'from': w['frm'], 'uri': w['uri']})
                written += 1
                continue
            nt = old_to_new.get(w['tgt'])
            if nt is None:
                continue
            link = {'kind': fitz.LINK_GOTO, 'from': w['frm'], 'page': nt}
            if w['y'] is not None:
                link['to'] = fitz.Point(w['x'], w['y'])
            page.insert_link(link)
            written += 1

    if toc:
        new_toc = []
        for lvl, title, pg1 in toc:
            nt = old_to_new.get(pg1 - 1)
            if nt is not None:
                new_toc.append([lvl, title, nt + 1])
        new_toc.sort(key=lambda e: (e[2], e[0]))
        d.set_toc(new_toc)

    d.save(dst, garbage=0, deflate=True)
    expected = stats['named'] + stats['direct'] + stats['uri']
    d.close()
    return dict(pages=n0, map_moved=moved, expected=expected, written=written, **stats)


if __name__ == '__main__':
    r = rebuild(sys.argv[1], sys.argv[2])
    print(f"  pages {r['pages']}  map pages to the back: {r['map_moved']}")
    print(f"  links: {r['named']} named + {r['direct']} direct + {r['uri']} uri = {r['expected']} expected,"
          f" {r['written']} written, {r['dropped']} unresolvable")
