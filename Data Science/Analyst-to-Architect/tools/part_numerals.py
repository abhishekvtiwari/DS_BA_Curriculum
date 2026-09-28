"""Write part numbers as ordinary numbers: Part 0 to Part 8 (decision D8, 28 Sep 2026).

    python tools/part_numerals.py --check manuscript/*.md     # list what would change
    python tools/part_numerals.py manuscript/*.md figures/*.svg figures/make_figs*.py tools/pdf/build.py

"Part II" becomes "Part 2", "Parts 0 and I" becomes "Parts 0 and 1", "Parts III to VII" becomes
"Parts 3 to 7". Only numerals that follow "Part" or "Parts" (directly, or in a list joined by
commas, "and", "or", "to", "through" or a dash) change; nothing inside code blocks changes.
"""
import re, sys, glob, pathlib

ROMAN = {'0': '0', 'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6', 'VII': '7', 'VIII': '8'}
NUM = r'(?:VIII|VII|VI|IV|V|III|II|I|0)'
JOIN = r'(?:,\s*|\s+and\s+|\s+or\s+|\s+to\s+|\s+through\s+|\s*[–—-]\s*)'
PAT = re.compile(r'\b(Parts?)(\s+|&nbsp;| )(' + NUM + r'\b(?:' + JOIN + NUM + r'\b(?![\'’]\w))*)')


def convert(text, report=None, name=''):
    def one(m):
        if report is not None and re.search(r'(and|or) I$', m.group(3)):
            report.append('check: %s: %s' % (name, m.string[m.start():m.end() + 14]))   # "and I" is always Part I in this book so far
        nums = re.sub(r'\b' + NUM + r'\b', lambda n: ROMAN[n.group()], m.group(3))
        return m.group(1) + m.group(2) + nums
    out, fence = [], False
    for line in text.split('\n'):
        if line.lstrip().startswith('```'):
            fence = not fence
        out.append(line if fence else PAT.sub(one, line))
    return '\n'.join(out)


if __name__ == '__main__':
    args = sys.argv[1:]
    check = '--check' in args
    total = 0
    for a in [x for x in args if x != '--check']:
        for f in sorted(glob.glob(a)):
            p = pathlib.Path(f)
            old = p.read_text(encoding='utf-8')
            rep = []
            new = convert(old, rep, p.name)
            n = sum(1 for x, y in zip(old.split('\n'), new.split('\n')) if x != y)
            total += n
            for r in rep: print(r)
            if n:
                print('%4d lines  %s' % (n, p.name))
                if not check: p.write_text(new, encoding='utf-8')
    print('total lines changed:', total)
