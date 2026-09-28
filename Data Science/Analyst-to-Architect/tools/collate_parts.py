"""Rebuild the collated part files (manuscript/part0-first-principles.md, part1-the-map.md) from the
chapter files, so a whole-part PDF always matches the chapters.

    python tools/collate_parts.py            # rewrites both files

Each part file keeps its own introduction (everything before the first "# Chapter" heading). In the
introduction's contents table, the "Time needed" column is refreshed from each chapter's own
"Time needed" line, and "In total, allow X–Y hours" is recomputed. Chapters are appended with their
"*Part …*" line removed (the part file already says which part it is).
"""
import re, pathlib, glob

MS = pathlib.Path(__file__).resolve().parents[1] / 'manuscript'
PARTS = {'part0-first-principles.md': range(1, 7), 'part1-the-map.md': range(7, 10)}


def chapter_file(n):
    return sorted(MS.glob(f'ch{n:02d}-*.md'))[0]


def hours(text):
    m = re.search(r'\*\*Time needed:\*\*\s*(\d+)–(\d+) hours', text)
    return (int(m.group(1)), int(m.group(2))) if m else None


def collate(name, nums):
    path = MS / name
    old = path.read_text(encoding='utf-8')
    intro = old[:old.index('\n# Chapter ')].rstrip() + '\n'
    lo = hi = 0
    body = []
    for n in nums:
        t = chapter_file(n).read_text(encoding='utf-8')
        h = hours(t)
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
