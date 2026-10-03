"""Structural checks on a Part 8 question bank after a new section is inserted.

Catches the things that are easy to get wrong when a long section is written in one go and are
invisible when reading: a duplicated or skipped question code, an unbalanced code fence, a table
whose rows do not all have the same number of cells, a question missing one of the parts every
other question has, and a cross-reference to a question code that does not exist.

    python tools/review-export/check_bank.py <chapter.md> [--section "## 72A.10"]
"""
import argparse
import collections
import pathlib
import re
import sys

PARTS = ['**Remember it as:**', '**Answer in one line:**', '| Tier | What to say |',
         '**Likely follow-ups:**', '**Learn it in:**']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('chapter')
    ap.add_argument('--section', help='heading of the new section, to check it on its own')
    a = ap.parse_args()

    p = pathlib.Path(a.chapter)
    text = p.read_text(encoding='utf-8')
    lines = text.splitlines()
    prefix = re.search(r'^### (Q[0-9A-Z]+)-\d+', text, re.M)
    if not prefix:
        raise SystemExit('no question codes found')
    pre = prefix.group(1)
    code_re = rf'{pre}-\d+'
    problems = []

    print(f'=== {p.name}  ({len(text.split()):,} words)')

    fences = [l for l in lines if l.strip().startswith('```')]
    print(f'code fences: {len(fences)} -> {"balanced" if len(fences) % 2 == 0 else "UNBALANCED"}')
    if len(fences) % 2:
        problems.append('unbalanced code fences')

    heads = re.findall(rf'^### ({code_re})', text, re.M)
    rows = re.findall(rf'^\| ({code_re})', text, re.M)
    allc = heads + rows
    dupes = [c for c, n in collections.Counter(allc).items() if n > 1]
    nums = sorted(int(c.split('-')[1]) for c in set(allc))
    gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
    print(f'questions: {len(heads)} core + {len(rows)} rapid-fire = {len(allc)}')
    print(f'  range {nums[0]:03d}-{nums[-1]:03d}, duplicates: {dupes or "none"}, '
          f'gaps: {[f"{pre}-{g:03d}" for g in gaps] or "none"}')
    if dupes:
        problems.append(f'duplicate codes: {dupes}')
    if gaps:
        problems.append(f'gaps in codes: {gaps}')

    # every code referenced anywhere must be defined somewhere
    referenced = set(re.findall(code_re, text))
    dangling = sorted(referenced - set(allc))
    print(f'  referenced but never defined: {dangling or "none"}')
    if dangling:
        problems.append(f'dangling references: {dangling}')

    body = text
    label = 'whole chapter'
    if a.section:
        i = text.index(a.section)
        nxt = re.search(r'^## (?!' + re.escape(a.section[3:].split()[0]) + r')', text[i + 10:], re.M)
        body = text[i:i + 10 + nxt.start()] if nxt else text[i:]
        label = a.section

    print(f'\n--- {label}  ({len(body.split()):,} words)')
    sec_heads = re.findall(rf'^### ({code_re})(.*)$', body, re.M)
    print(f'core questions: {len(sec_heads)}')
    for part in PARTS:
        n = body.count(part)
        flag = '' if n >= len(sec_heads) else '  <-- fewer than there are questions'
        print(f'  {part:<28} {n}{flag}')
        if n < len(sec_heads):
            problems.append(f'only {n} of {len(sec_heads)} questions have {part}')

    # tables: every row in a block should have the same cell count
    bad = 0
    block = []
    for ln in body.splitlines() + ['']:
        if ln.startswith('|'):
            block.append(ln)
        else:
            if len(block) >= 2:
                counts = {len(re.split(r'(?<!\\)\|', b)) for b in block}
                if len(counts) > 1:
                    bad += 1
                    print(f'  uneven table: {sorted(counts)} -> {block[0][:64]}')
            block = []
    print(f'uneven table blocks: {bad}')
    if bad:
        problems.append(f'{bad} uneven table blocks')

    print()
    if problems:
        print('PROBLEMS:')
        for x in problems:
            print('  -', x)
        sys.exit(1)
    print('all checks passed')


if __name__ == '__main__':
    main()
