"""Rebuild the collated part files (manuscript/part0-first-principles.md, part1-the-map.md) from the
chapter files, so a whole-part PDF always matches the chapters.

    python tools/collate_parts.py            # rewrites both files

Each part file keeps its own introduction (everything before the first "# Chapter" heading). In the
introduction's contents table, the "Time needed" column is refreshed from each chapter's own
"Time needed" line, and "In total, allow X–Y hours" is recomputed. The hours come from
tools/hours_table.py (one source, theme T12), so a line with a second range (Chapter 8's project)
counts it, as Chapter 6's and Chapter 83's tables do. Chapters are appended with their
"*Part …*" line removed (the part file already says which part it is).
"""
import re, pathlib, glob, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import hours_table          # one source for the hours (theme T12)

MS = pathlib.Path(__file__).resolve().parents[1] / 'manuscript'
PARTS = {'part0-first-principles.md': range(1, 7), 'part1-the-map.md': range(7, 10)}


def chapter_file(n):
    return sorted(MS.glob(f'ch{n:02d}-*.md'))[0]


def hours(text, n):
    if not re.search(r'\*\*Time needed:\*\*', text):
        return None
    lo, hi, _ = hours_table.chapter_hours(n)
    return lo, hi


def collate(name, nums):
    path = MS / name
    old = path.read_text(encoding='utf-8')
    intro = old[:old.index('\n# Chapter ')].rstrip() + '\n'
    lo = hi = 0
    body = []
    for n in nums:
        t = chapter_file(n).read_text(encoding='utf-8')
        h = hours(t, n)
        if h:
            lo += h[0]; hi += h[1]
            # refresh this chapter's row in the contents table: | **N. Title** | … | a–b hours |
            intro = re.sub(rf'^(\| \*\*{n}\. [^|]*\|[^|]*\|)\s*[^|]*\|$', rf'\g<1> {h[0]}–{h[1]} hours |', intro, flags=re.M)
        t = re.sub(r'^\*Part [^\n]*\*\n\n?', '', t, count=1, flags=re.M)
        body.append(t.strip() + '\n')
    intro = re.sub(r'In total, allow \d+–\d+ hours', f'In total, allow {lo}–{hi} hours', intro)
    path.write_text(intro + '\n\n' + '\n\n'.join(body), encoding='utf-8')
    return lo, hi


if __name__ == '__main__':
    for name, nums in PARTS.items():
        print(name, 'total hours %d–%d' % collate(name, nums))
