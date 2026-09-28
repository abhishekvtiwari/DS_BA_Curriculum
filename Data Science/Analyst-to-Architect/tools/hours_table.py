"""The book's honest hours table, computed from every teaching chapter's "Time needed" line.

    python tools/hours_table.py              # the two tables, as Markdown, ready to paste
    python tools/hours_table.py --chapters   # also list each chapter's hours

Chapter 6 section 6.1 and Chapter 83 section 83.1 (and Figure 83.1, through make_figs83.py) must
contain exactly what this script prints. Re-run it whenever a chapter's "Time needed" line changes,
and paste the result into both chapters (theme T12: one source for the hours).

How the lines are read (the rules Chapter 83 used for its 764–980 hours):
- The teaching chapters are 1 to 67. Part 8 (68–82) and the Closing (83) are not counted.
- Every "N–M hours" range in the line is added up. So Chapter 8's "3–4 hours, including the
  exercises. Allow another 2–3 hours for the project" counts as 5–7.
- Chapter 67 has no range ("Reading it once will take about two hours; living it will take
  years"). It counts as 2–4, as Chapter 83 counted it.
- Any other line without a range stops the script, so nothing is silently guessed.

Weeks are hours divided by the weekly hours, rounded to the nearest whole week (halves up);
months are weeks x 12 / 52; years are weeks / 52, to one decimal place.
"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MS = ROOT / 'manuscript'

PARTS = [('Part 0', 1, 6), ('Part 1', 7, 9), ('Part 2', 10, 27), ('Part 3', 28, 34),
         ('Part 4', 35, 44), ('Part 5', 45, 52), ('Part 6', 53, 59), ('Part 7', 60, 67)]
LAST_TEACHING = 67
RATES = (6, 8, 10)

RANGE = re.compile(r'(\d+)\s*[–-]\s*(\d+)\s+hours?\b')
SPECIAL = {67: (2, 4)}      # "about two hours" to read, counted as 2–4 (Chapter 83's rule)
# Lines whose later ranges break the first one down (sittings, sections) rather than add to it
# (Parts 2 and 3 build, 28 Sep 2026). Chapter 27 adds its two stated parts: reading and running the
# worked project (2–3 h) and the reader's own portfolio (20–30 h, which includes the deep project).
SPECIAL.update({11: (35, 45), 19: (25, 30), 26: (9, 11), 27: (22, 33), 29: (20, 24), 32: (18, 22)})


def chapter_file(n):
    files = sorted(MS.glob(f'ch{n:02d}-*.md'))
    if len(files) != 1:
        sys.exit(f'Chapter {n}: expected one manuscript file ch{n:02d}-*.md, found {len(files)}')
    return files[0]


def time_needed_line(n):
    for line in chapter_file(n).read_text(encoding='utf-8').splitlines():
        if '**Time needed:**' in line:
            return line.split('**Time needed:**', 1)[1].strip()
    sys.exit(f'Chapter {n}: no "Time needed" line in {chapter_file(n).name}')


def chapter_hours(n):
    line = time_needed_line(n)
    if n in SPECIAL:
        return SPECIAL[n] + (line,)
    ranges = RANGE.findall(line)
    if not ranges:
        sys.exit(f'Chapter {n}: no "N–M hours" range in its Time needed line: {line!r}')
    return sum(int(a) for a, _ in ranges), sum(int(b) for _, b in ranges), line


def half_up(x, places=0):
    k = 10 ** places
    return math.floor(x * k + 0.5) / k if places else int(math.floor(x + 0.5))


def weeks(h, rate):
    return half_up(h / rate)


def span(lo, hi, rate, unit):
    if unit == 'weeks':
        return f'{weeks(lo, rate)}–{weeks(hi, rate)} weeks'
    if unit == 'months':
        return f'{half_up(weeks(lo, rate) * 12 / 52)} to {half_up(weeks(hi, rate) * 12 / 52)} months'
    return f'{half_up(lo / rate / 52, 1):.1f} to {half_up(hi / rate / 52, 1):.1f} years'


def totals():
    """{'chapters': {n: (lo, hi, line)}, 'parts': [(name, first, last, lo, hi)], and the summary rows}."""
    ch = {n: chapter_hours(n) for n in range(1, LAST_TEACHING + 1)}

    def add(a, b):
        return (sum(ch[n][0] for n in range(a, b + 1)), sum(ch[n][1] for n in range(a, b + 1)))

    parts = [(name, a, b) + add(a, b) for name, a, b in PARTS]
    return {'chapters': ch, 'parts': parts,
            'foundations': add(1, 9), 'part2': add(10, 27), 'job_ready': add(1, 27),
            'after': add(28, LAST_TEACHING), 'all': add(1, LAST_TEACHING)}


def ch06_table(t):
    rows = [('Parts 0 and 1', '1–9', t['foundations'], 'weeks', False),
            ('Part 2', '10–27', t['part2'], 'weeks', False),
            ('Job-ready: Parts 0 to 2', '1–27', t['job_ready'], 'job', True),
            ('Parts 3 to 7', '28–67', t['after'], 'years', False),
            ('All of it', '1–67', t['all'], 'years', True)]
    out = ['| | Hours | 6 hours a week | 8 hours a week | 10 hours a week |',
           '|---|---|---|---|---|']
    for name, chs, (lo, hi), unit, bold in rows:
        cells = []
        for r in RATES:
            if unit == 'job':
                cells.append(f"{span(lo, hi, r, 'weeks')}, or {span(lo, hi, r, 'months')}")
            else:
                cells.append(span(lo, hi, r, unit))
        # the nobr span keeps a range such as 290–357 on one line in a narrow column (the
        # builder's table code doesn't yet keep number ranges together)
        row = [f'{name} (<span class="nobr">Chapters {chs}</span>)', f'<span class="nobr">{lo}–{hi}</span>'] + cells
        if bold:
            row = [f'**{c}**' for c in row]
        out.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(out)


LONG_NAMES = {'Part 2': 'Part 2, The Analyst', 'Part 3': 'Part 3, advanced analytics',
              'Part 4': 'Part 4, machine learning', 'Part 5': 'Part 5, data engineering',
              'Part 6': 'Part 6, production ML and GenAI', 'Part 7': 'Part 7, architecture and leadership'}


def ch83_table(t):
    out = ['| | Chapters | Hours | At 6 hours a week |', '|---|---|---|---|']
    lo, hi = t['foundations']
    out.append(f"| Parts 0 and 1, the foundations | 1–9 | {lo}–{hi} | {span(lo, hi, 6, 'weeks')} |")
    for name, a, b, lo, hi in t['parts'][2:]:
        row = [LONG_NAMES[name], f'{a}–{b}', f'{lo}–{hi}', span(lo, hi, 6, 'weeks')]
        if name == 'Part 2':
            out.append('| ' + ' | '.join(f'**{c}**' for c in row) + ' |')
            lo2, hi2 = t['job_ready']
            out.append(f"| **Parts 0 to 2: job-ready** | **1–27** | **{lo2}–{hi2}** | **{span(lo2, hi2, 6, 'months')}** |")
        else:
            out.append('| ' + ' | '.join(row) + ' |')
    lo, hi = t['all']
    out.append(f"| **All of it** | **1–67** | **{lo}–{hi}** | **{span(lo, hi, 6, 'years')}** |")
    return '\n'.join(out)


if __name__ == '__main__':
    t = totals()
    if '--chapters' in sys.argv:
        for n, (lo, hi, line) in t['chapters'].items():
            print(f'Ch {n:2}  {lo:3}–{hi:<3}  {line}')
        print()
    print('By part:')
    for name, a, b, lo, hi in t['parts']:
        print(f'  {name:9} Ch {a}–{b}: {lo}–{hi} hours')
    for key, label in [('foundations', 'Parts 0 and 1 (1–9)'), ('part2', 'Part 2 (10–27)'),
                       ('job_ready', 'Job-ready, Parts 0 to 2 (1–27)'), ('after', 'Parts 3 to 7 (28–67)'),
                       ('all', 'All teaching chapters (1–67)')]:
        print(f'  {label}: {t[key][0]}–{t[key][1]} hours')
    print('\nChapter 6, section 6.1:\n')
    print(ch06_table(t))
    print('\nChapter 83, section 83.1:\n')
    print(ch83_table(t))
