"""Write the opening page of a part PDF (Parts 2 and 3) from the chapters themselves.

    python tools/make_part_intro.py            # writes the opening page of Parts 2 to 8 (manuscript/partN-*.md)

Each opening page has the part's title, one sentence about the part, and a table of its chapters in the
approved reading order (decision of 28 Sep 2026: Part 2 reads 10, 11, 19, 12–18, 20–27; Part 3 reads 28, 34,
29, 32, 33, 30, 31; Parts 4 to 8 read in chapter-number order), with each chapter's own "Time needed" range and
the total. Part 2's sentence is the one the front section ("How the parts climb") already uses. Part 8's
chapters are question banks without a "Time needed" range, so its page lists the chapters only.
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
    'part4-machine-learning.md': dict(
        title='Part 4 — Machine Learning & Data Science',
        about="Part 4 teaches machines to learn from Riverstone's data: the maths under the models, the "
              "machine-learning workflow, supervised and unsupervised learning, honest evaluation, forecasting, "
              "text, recommenders, a first look at deep learning, and a capstone project.",
        order=list(range(35, 45))),
    'part5-data-engineering.md': dict(
        title='Part 5 — Data Engineering, Integration & Scale',
        about="Part 5 builds the plumbing that moves data reliably: ingestion, pipelines and orchestration, data "
              "quality, big data, warehouses and lakehouses, streaming, data activation, and the cloud.",
        order=list(range(45, 53))),
    'part6-production-ml-genai.md': dict(
        title='Part 6 — Production ML, Generative AI & MLOps',
        about="Part 6 takes models into production: deep learning in depth, generative AI and large language "
              "models, building AI applications, MLOps, LLMOps, intelligent automation, and industry case studies.",
        order=list(range(53, 60))),
    'part7-architecture-leadership.md': dict(
        title='Part 7 — Architecture, Governance & Leadership',
        about="Part 7 steps back to see the whole: designing systems, distributed systems, data architecture "
              "patterns, automation architecture, security and responsible AI, FinOps, data strategy, and the "
              "architect as leader.",
        order=list(range(60, 68))),
    'part8-interview-playbook.md': dict(
        title='Part 8 — The Interview Playbook',
        about="How data hiring works, and question banks for each role. Use Part 8 when you apply for a job: "
              "read Chapters 68 and 69 first, then the banks for the role you want.",
        order=[68, 69, 70, 71, 72, '72a', 73, 74, 75, '76a', '76b', 77, 78, 79, 80, 81, 82]),
}


def chapter(n):
    f = sorted(MS.glob(f'ch{n:02d}-*.md' if isinstance(n, int) else f'ch{n}-*.md'))[0]
    t = f.read_text(encoding='utf-8')
    num, title = re.match(r'# Chapter (\w+)\.\s*(.+)', t).groups()
    if not isinstance(n, int) or n > hours_table.LAST_TEACHING:
        return f.name, num, title.strip(), None     # Part 8: no hours range
    lo, hi, _ = hours_table.chapter_hours(n)
    return f.name, num, title.strip(), (lo, hi)


def write(name, spec):
    rows, lo, hi = [], 0, 0
    chapters = [chapter(n) for n in spec['order']]
    if all(h is None for *_, h in chapters):
        rows = [f'| **{num}. {title}** |' for _, num, title, _ in chapters]
        md = (f"# {spec['title']}\n\n{spec['about']}\n\n| Chapter |\n|---|\n" + '\n'.join(rows) + '\n')
        (MS / name).write_text(md, encoding='utf-8')
        return 0, 0
    for _, num, title, h in chapters:
        rows.append(f'| **{num}. {title}** | {h[0]}–{h[1]} hours |' if h else f'| **{num}. {title}** | see the chapter |')
        if h: lo += h[0]; hi += h[1]
    md = (f"# {spec['title']}\n\n{spec['about']}\n\nRead the chapters in this order:\n\n"
          "| Chapter | Time needed |\n|---|---|\n" + '\n'.join(rows) +
          f"\n\nIn total, allow {lo}–{hi} hours, including the exercises and projects.\n")
    (MS / name).write_text(md, encoding='utf-8')
    return lo, hi


if __name__ == '__main__':
    for name, spec in PARTS.items():
        print(name, '%d–%d hours' % write(name, spec))
