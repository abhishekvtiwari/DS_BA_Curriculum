"""Write the book overview (the internal introduction volume) from the chapters themselves.

    python tools/make_overview.py      # writes manuscript/book-overview.md and figures/fig-overview-flow.svg

Nothing in the overview is typed by hand that the chapters already say: each chapter's title, its
"You will learn to", "Before you start" and "Time needed" lines come from the chapter's own
"Chapter at a glance" box; part totals come from tools/hours_table.py (theme T12, one source);
the routes by role come from Chapter 8, section 8.7. Parts 2 and 3 are listed in their approved
reading order (chapter numbers stay as they are until the renumbering pass).
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MS = ROOT / 'manuscript'
sys.path.insert(0, str(ROOT / 'tools'))
import hours_table          # noqa: E402

PARTS = [
    ('0', 'First Principles: Data from Zero', [1, 2, 3, 4, 5, 6],
     'What data is, how computers store and move it, how a business runs on it, numbers without fear, '
     'thinking like an analyst, and planning your learning. No software needed.'),
    ('1', 'The Map', [7, 8, 9],
     'The data jobs, how skills unlock them, and how expertise forms. No software needed.'),
    ('2', 'The Analyst', [10, 11, 19, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27],
     'Spreadsheets, SQL, cleaning data, charts, Power BI, Python, statistics, business skills and a portfolio: '
     'the skills of a first analyst job. The end of Part 2 is "job-ready".'),
    ('3', 'Advanced Analytics & Analytics Engineering', [28, 34, 29, 32, 33, 30, 31],
     'Advanced SQL and data modelling, the command line, Python as software, dbt, the computer science behind '
     'fast code, experiments, and causal inference.'),
    ('4', 'Machine Learning & Data Science', list(range(35, 45)),
     'The maths under the models, the machine-learning workflow, supervised and unsupervised learning, honest '
     'evaluation, forecasting, text, recommenders, a first look at deep learning, and a capstone.'),
    ('5', 'Data Engineering, Integration & Scale', list(range(45, 53)),
     'Ingestion, pipelines and orchestration, data quality, big data, warehouses and lakehouses, streaming, '
     'data activation, and the cloud.'),
    ('6', 'Production ML, Generative AI & MLOps', list(range(53, 60)),
     'Deep learning in depth, generative AI and large language models, building AI applications, MLOps, LLMOps, '
     'intelligent automation, and industry case studies.'),
    ('7', 'Architecture, Governance & Leadership', list(range(60, 68)),
     'Designing whole systems, distributed systems, data architecture patterns, automation architecture, '
     'security and responsible AI, FinOps, data strategy, and the architect as leader.'),
    ('8', 'The Interview Playbook', [68, 69, 70, 71, 72, '72a', 73, 74, 75, '76a', '76b', 77, 78, 79, 80, 81, 82],
     'How data hiring works, the extra-points method, and a question bank for each skill and role, with '
     'take-home assignments and mock interviews. Published as its own book.'),
    ('Closing', 'The Long Game', [83],
     'What the whole path costs in hours, and how to keep going after the book.'),
]


def chapter_file(n):
    pat = f'ch{n:02d}-*.md' if isinstance(n, int) else f'ch{n}-*.md'
    return sorted(MS.glob(pat))[0]


def glance(n):
    """Title and the glance-box lines of one chapter."""
    t = chapter_file(n).read_text(encoding='utf-8')
    num, title = re.match(r'# Chapter (\w+)\.\s*(.+)', t).groups()
    box = {}
    for key in ('You will learn to', 'Before you start', 'Time needed'):
        m = re.search(r'^>\s*\*\*' + re.escape(key) + r':\*\*\s*(.+)$', t, re.M)
        box[key] = m.group(1).strip() if m else ''
    sections = re.findall(r'^## (\d+[A-Z]?\.\d+ .+)$', t, re.M)
    return num, title.strip(), box, sections


def hours(n):
    if not isinstance(n, int) or n > hours_table.LAST_TEACHING:
        return None
    lo, hi, _ = hours_table.chapter_hours(n)
    return lo, hi


def part_hours(chapters):
    hs = [hours(n) for n in chapters]
    if any(h is None for h in hs):
        return None
    return sum(h[0] for h in hs), sum(h[1] for h in hs)


def skills(line):
    """'a · b · c' → markdown bullets; long lines stay readable."""
    items = [s.strip().rstrip('.') for s in line.split(' · ') if s.strip()]
    return '\n'.join(f'- {s[0].upper() + s[1:]}' for s in items)


def routes():
    """The routes table from Chapter 8, section 8.7, with the Part 8 bank numbers as they are now."""
    t = chapter_file(8).read_text(encoding='utf-8')
    sec = t[t.index('## 8.7'):]
    rows = [l for l in sec.split('\n\n')[2].splitlines() if l.startswith('|')]
    return '\n'.join(rows)


def flow_svg(path):
    """Parts as boxes, arrows for 'builds on'. 700 px wide; text is 14 px or more (≥ 9.8 pt in print)."""
    W, H = 700, 520
    boxes = {  # key: (x, y, w, h, title, sub)
        '0': (30, 20, 200, 58, 'Part 0', 'First principles'),
        '1': (250, 20, 200, 58, 'Part 1', 'The map'),
        '2': (470, 20, 200, 58, 'Part 2', 'The analyst (job-ready)'),
        '3': (250, 120, 200, 58, 'Part 3', 'Advanced analytics'),
        '4': (30, 230, 200, 58, 'Part 4', 'Machine learning'),
        '5': (470, 230, 200, 58, 'Part 5', 'Data engineering'),
        '6': (30, 340, 200, 58, 'Part 6', 'Production ML & GenAI'),
        '7': (250, 340, 200, 58, 'Part 7', 'Architecture & leadership'),
        'C': (250, 440, 200, 58, 'Closing', 'The long game'),
        '8': (470, 440, 200, 58, 'Part 8 (own book)', 'Interview playbook'),
    }
    edges = [('0', '1'), ('1', '2'), ('2', '3'), ('3', '4'), ('3', '5'), ('4', '6'), ('5', '7'), ('6', '7'),
             ('7', 'C'), ('2', '8')]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           'font-family="DejaVu Sans, sans-serif">',
           '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#44506a"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']

    def anchor(k, towards):
        x, y, w, h = boxes[k][:4]
        cx, cy = x + w / 2, y + h / 2
        tx, ty = towards
        if abs(tx - cx) * h > abs(ty - cy) * w:        # leave by the left or right side
            return (x + w if tx > cx else x, cy)
        return (cx, y + h if ty > cy else y)            # or by the top or bottom
    for a, b in edges:
        xa, ya, wa, ha = boxes[a][:4]
        xb, yb, wb, hb = boxes[b][:4]
        p = anchor(a, (xb + wb / 2, yb + hb / 2))
        q = anchor(b, (xa + wa / 2, ya + ha / 2))
        dash = ' stroke-dasharray="6 4"' if (a, b) == ('2', '8') else ''
        out.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#44506a" '
                   f'stroke-width="2"{dash} marker-end="url(#a)"/>')
    for k, (x, y, w, h, t, s) in boxes.items():
        fill = '#eef2f8' if k not in ('8', 'C') else '#ffffff'
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#44506a" '
                   f'stroke-width="1.5"/>')
        out.append(f'<text x="{x + w / 2}" y="{y + 25}" text-anchor="middle" font-size="17" font-weight="bold" '
                   f'fill="#1c2433">{html.escape(t)}</text>')
        out.append(f'<text x="{x + w / 2}" y="{y + 46}" text-anchor="middle" font-size="14" fill="#1c2433">{html.escape(s)}'
                   '</text>')
    out.append(f'<text x="480" y="{H - 8}" font-size="14" fill="#44506a">dashed: use when you apply</text>')
    out.append('</svg>')
    path.write_text('\n'.join(out) + '\n', encoding='utf-8')


def main():
    fig = ROOT / 'figures' / 'fig-overview-flow.svg'
    flow_svg(fig)
    job = hours_table.PARTS
    total_lo = sum(part_hours(p[2])[0] for p in PARTS if p[0] in '01234567' and len(p[0]) == 1)
    total_hi = sum(part_hours(p[2])[1] for p in PARTS if p[0] in '01234567' and len(p[0]) == 1)
    ready = [part_hours(p[2]) for p in PARTS if p[0] in ('0', '1', '2')]
    md = ['# About this overview', '',
          'This is the internal overview of *Analyst to Architect*: every part and chapter, the skills each one '
          'covers, how long it takes, what it builds on, and how the parts lead into each other. It is generated '
          'from the chapters themselves (`tools/make_overview.py`), so it always matches them.', '',
          'The book is published as two books:', '',
          '- **Analyst to Architect**, the main book, in two volumes with one page count. Volume 1, *From Zero '
          'to Job-Ready*: How to Use This Book and Parts 0 to 2. Volume 2, *From Analyst to Architect*: Parts 3 '
          'to 7 and the closing chapter.',
          '- **The Interview Playbook**, its own book: Part 8, the question banks and interview practice.', '',
          '## The whole path at a glance', '',
          '![The parts as boxes with arrows showing what builds on what. Part 0 First principles leads to Part 1 '
          'The map, then Part 2 The analyst, which is job-ready. Part 2 leads to Part 3 Advanced analytics, which '
          'leads to Part 4 Machine learning and Part 5 Data engineering. Part 4 leads to Part 6 Production ML and '
          'GenAI; Parts 5 and 6 lead to Part 7 Architecture and leadership, and Part 7 leads to the Closing. A '
          'dashed arrow from Part 2 goes to Part 8, the Interview playbook, used when you apply for a job.]'
          '(figures/fig-overview-flow.svg)', '',
          '*How the parts build on each other. Parts 0 to 2 are one path everyone follows; Parts 3 to 7 are '
          'branches you choose by the role you want.*', '',
          '| Part | Chapters | Time needed | What it covers |', '|---|---|---|---|']
    for key, title, chs, about in PARTS:
        h = part_hours(chs)
        nums = ', '.join(glance(n)[0] for n in chs)
        md.append(f'| **{"Part " + key if key != "Closing" else "Closing"}** {title} | {nums} | '
                  f'{f"{h[0]}–{h[1]} h" if h else "reference"} | {about} |')
    md += ['', f'**Job-ready** (Parts 0 to 2) takes {sum(r[0] for r in ready)}–{sum(r[1] for r in ready)} hours. '
           f'**The teaching chapters** (Parts 0 to 7) take {total_lo}–{total_hi} hours. Chapter 6 turns these hours '
           'into a weekly plan, and Chapter 83 into the long view.', '',
           '## How the parts flow', '',
           '- **Parts 0 and 1** need no software. They teach how data and businesses work, and map the jobs.',
           '- **Part 2** is the analyst core, and the end of it is "job-ready". Tools arrive one at a time: the '
           'spreadsheet in Chapter 10, databases in Chapter 12, Power BI in Chapter 16, Python and Jupyter in '
           'Chapter 17, the terminal and Git in Chapter 26.',
           '- **Part 3** deepens it: advanced SQL, the command line, Python as software, dbt, computer science, '
           'experiments and causal inference.',
           '- **Parts 4 to 7 are branches.** Machine learning (4) and data engineering (5) both build on Part 3; '
           'production ML and generative AI (6) build on Part 4; architecture and leadership (7) draw on all of them.',
           '- **Part 8** is for the job search, and can be used any time after Part 2.',
           '- **Reading order.** Parts 2 and 3 are read in this order: Part 2: 10, 11, 19, 12, 13, 14, 15, 16, 17, '
           '18, 20–27; Part 3: 28, 34, 29, 32, 33, 30, 31. Chapter numbers will be changed to match the reading '
           'order in the final pass; this overview lists the chapters in reading order.', '',
           '## Routes by role', '',
           'From Chapter 8, section 8.7. "Read fully" means the chapters, exercises and projects; "skim" means the '
           'ideas and worked examples.', '',
           routes(), '']
    for key, title, chs, about in PARTS:
        h = part_hours(chs)
        head = f'Part {key} — {title}' if key != 'Closing' else 'Closing — The Long Game'
        md += [f'# {head}', '', about + (f' Time needed: {h[0]}–{h[1]} hours.' if h else ''), '']
        for n in chs:
            num, t, box, secs = glance(n)
            md += [f'## Chapter {num}. {t}', '']
            if box['Time needed']:
                md += [f'**Time needed:** {box["Time needed"]}', '']
            if box['You will learn to']:
                md += ['**Skills covered:**', '', skills(box['You will learn to']), '']
            if box['Before you start']:
                md += [f'**Builds on:** {box["Before you start"]}', '']
            if secs:
                md += ['**Sections:** ' + ' · '.join(secs), '']
    (MS / 'book-overview.md').write_text('\n'.join(md), encoding='utf-8')
    print('manuscript/book-overview.md', sum(len(p[2]) for p in PARTS), 'chapters;',
          f'teaching {total_lo}–{total_hi} h')


if __name__ == '__main__':
    main()
