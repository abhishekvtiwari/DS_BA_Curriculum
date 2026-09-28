"""Write the opening page of a part PDF (Parts 2 and 3) from the chapters themselves.

    python tools/make_part_intro.py            # writes manuscript/part2-the-analyst.md and part3-advanced-analytics.md

Each opening page has the part's title, one sentence about the part, and a table of its chapters in the
approved reading order (decision of 28 Sep 2026: Part 2 reads 10, 11, 19, 12–18, 20–27; Part 3 reads 28, 34,
29, 32, 33, 30, 31), with each chapter's own "Time needed" range and the total. Part 2's sentence is the one
the front section ("How the parts climb") already uses.
"""
import re, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import hours_table          # one source for the hours (theme T12)

MS = pathlib.Path(__file__).resolve().parents[1] / 'manuscript'
PARTS = {
    'part2-the-analyst.md': dict(
        title='Part 2 — The Analyst',
        about="Spreadsheets, SQL (the language for asking a database questions), cleaning data, charts, Power BI "
              "dashboards, the Python programming language, statistics, business skills, and a portfolio. The end "
              "of Part 2 is where \"job-ready\" ends: it covers the skills of a first analyst job.",
        order=[10, 11, 19, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27]),
    'part3-advanced-analytics.md': dict(
        title='Part 3 — Advanced Analytics & Analytics Engineering',
        about="Part 3 takes the analyst's tools further: advanced SQL and data modelling, the command line, Python "
              "as software, analytics engineering with dbt, the computer science behind fast code, experiments, "
              "and causal inference.",
        order=[28, 34, 29, 32, 33, 30, 31]),
}


def chapter(n):
    f = sorted(MS.glob(f'ch{n:02d}-*.md'))[0]
    t = f.read_text(encoding='utf-8')
    title = re.match(r'# Chapter \d+\.\s*(.+)', t).group(1).strip()
    lo, hi, _ = hours_table.chapter_hours(n)
    return f.name, title, (lo, hi)


def write(name, spec):
    rows, lo, hi = [], 0, 0
    for n in spec['order']:
        _, title, h = chapter(n)
        rows.append(f'| **{n}. {title}** | {h[0]}–{h[1]} hours |' if h else f'| **{n}. {title}** | see the chapter |')
        if h: lo += h[0]; hi += h[1]
    md = (f"# {spec['title']}\n\n{spec['about']}\n\nRead the chapters in this order:\n\n"
          "| Chapter | Time needed |\n|---|---|\n" + '\n'.join(rows) +
          f"\n\nIn total, allow {lo}–{hi} hours, including the exercises and projects.\n")
    (MS / name).write_text(md, encoding='utf-8')
    return lo, hi


if __name__ == '__main__':
    for name, spec in PARTS.items():
        print(name, '%d–%d hours' % write(name, spec))
