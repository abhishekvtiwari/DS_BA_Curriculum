"""Every number Chapter 83 quotes, recomputed from tools/hours_table.py (theme T12, one source).

    python3 checks/ch83_numbers.py

Prints the totals, the sprinter-and-steady table of section 83.2, the shortfall of the sprinter,
the share of the book that is job-ready, and the cumulative hours per part used by Figure 83.1.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'tools'))
import hours_table as ht  # noqa: E402

t = ht.totals()
ch = t['chapters']
(jl, jh), (al, ah) = t['job_ready'], t['all']
print(f'Job-ready (Ch 1-27): {jl}-{jh} h; whole book (Ch 1-67): {al}-{ah} h')
print(f'  job-ready at 6 h/week: {ht.span(jl, jh, 6, "weeks")}, {ht.span(jl, jh, 6, "months")}')
print(f'  whole book at 6 h/week: {ht.span(al, ah, 6, "weeks")}, {ht.span(al, ah, 6, "years")}')
print(f'  job-ready share of the book: {jl / al:.1%} (low) and {jh / ah:.1%} (high)')

# Section 83.2: sprinter 25 h/week for 12 weeks; steady 6 h/week
sprint = 25 * 12
print(f'\nSprinter: 25 x 12 = {sprint} h; 25 / 6 = {25 / 6:.2f} times the steady weekly hours')
print(f'Steady: week 12 = {6 * 12} h; crossover week = {sprint / 6:g}')
wl, wh = ht.weeks(jl, 6), ht.weeks(jh, 6)
print(f'Steady reaches job-ready in weeks {wl}-{wh}: {6 * wl}-{6 * wh} h at those weeks')
bl, bh = ht.weeks(al, 6), ht.weeks(ah, 6)
print(f'Steady finishes the book in weeks {bl}-{bh}: {6 * bl}-{6 * bh} h')
print(f'Steady at year 3 (week 156): {6 * 156} h')

short_lo, short_hi = jl - sprint, jh - sprint
print(f'\nSprinter short of job-ready by {short_lo}-{short_hi} h; '
      f'at 6 h/week {ht.span(short_lo, short_hi, 6, "weeks")}, {ht.span(short_lo, short_hi, 6, "months")}')

# How many Part 2 chapters is that, counted back from the end of Part 2 in reading order?
PART2_READING = [10, 11, 19, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27]
for k, short in ((0, short_lo), (1, short_hi)):
    acc, n = 0, 0
    for c in reversed(PART2_READING):
        acc += ch[c][k]; n += 1
        if acc >= short:
            break
    print(f'  {"low" if k == 0 else "high"} estimates: the last {n} chapters of Part 2 add up to {acc} h (>= {short})')

# Figure 83.1: where each part ends, counted from the first page
print('\nCumulative hours at the end of each part (low-high):')
cl = chh = 0
for name, a, b, lo, hi in t['parts']:
    cl += lo; chh += hi
    print(f'  {name} (Ch {a}-{b}): +{lo}-{hi} -> {cl}-{chh}')
