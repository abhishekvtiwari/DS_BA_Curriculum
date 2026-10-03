"""Build the Practice Arena: the same practice material, arranged by tool instead of by chapter.

Why this exists. The companion folder is organised by chapter, because the book is, and every
chapter refers to its own folder by name. That is correct for the book and frustrating for a
learner: someone who wants to work on Excel has to already know that chapters 02, 04, 08, 09, 10,
11, 15, 19, 22 and 70 are the ones with workbooks in them, and open sixty-nine folders to find out.

The Arena is a second view of the same files, grouped by the tool you want to practise and ordered
from the smallest idea to the finished artifact. It is **additive**: nothing is moved or renamed in
`companion/`, so every reference in the book still resolves.

Three rules it follows.

1. **Generated, not curated by hand.** Rebuild it after any change to the companion material and it
   is current. The only hand-written part is the TOOLS map below, which says which chapters teach
   which tool, in what order, and in what words — that is editorial knowledge a script cannot infer.
2. **Complete.** Every tracked file under `companion/` must be claimed by a tool or matched by an
   EXCLUDE rule. The build fails and names the orphans otherwise, so material cannot go missing.
3. **The generators are out of the way, not thrown away.** Scripts whose job is to build practice
   data live in a `_build-scripts/` folder inside each stage rather than beside the files a learner
   is meant to open.

    python tools/review-export/make_practice_arena.py <destination>
"""
import argparse
import collections
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[2]
BOOK = ROOT / 'Data Science' / 'Analyst-to-Architect'
COMP = BOOK / 'companion'
MS = BOOK / 'manuscript'

# Files that are infrastructure rather than practice material.
EXCLUDE = [
    re.compile(r'/\.gitignore$'), re.compile(r'/\.gitkeep$'),
    re.compile(r'\.pyc$'), re.compile(r'__pycache__'),
]

# A script whose job is to generate practice data, not to be read as practice material.
GENERATOR = re.compile(r'/(build_|make_|generate_|prepare_)[\w]*\.py$')

# ---------------------------------------------------------------------------------------------
# The editorial map: tool -> stages -> the chapters whose files belong in that stage.
# Order matters: stages run from the smallest idea to the finished artifact.
# ---------------------------------------------------------------------------------------------
TOOLS = [
 ('01-Excel-and-Google-Sheets', 'Excel & Google Sheets',
  'Spreadsheets, from your first formula to a working dashboard and a macro that runs itself.',
  [('01-First-steps', ['ch02', 'ch04'],
    'Reading a file, and doing arithmetic without fear. Open these before anything else.'),
   ('02-Foundations', ['ch10'],
    'The core grammar: references, formulas, formats, and a tracker you build and check.'),
   ('03-The-spreadsheet-mastered', ['ch11'],
    'Lookups, conditional logic, dynamic arrays, Power Query, and two full case workbooks with '
    'their solutions. This is the stage where a spreadsheet becomes a tool rather than a grid.'),
   ('04-Charts-and-dashboards', ['ch15'],
    'What to plot and what not to. The chart data here is the same data the Python charts use, '
    'so you can build the same picture in both and compare.'),
   ('05-Statistics-by-hand', ['ch22'],
    'The statistics worked in a spreadsheet first, so the formula is visible before a library '
    'hides it.'),
   ('06-Macros-VBA-and-scripts', ['ch19'],
    'Twelve branch workbooks and a practice file: the raw material for a macro that consolidates '
    'them. This is the automation payoff in spreadsheet form.'),
   ('07-Career-and-planning', ['ch08', 'ch09'],
    'The skills matrix and the practice log. Not analysis — the sheets you keep for yourself.'),
   ('08-Interview-drills', ['ch70'],
    'The practice workbook for the Excel, Sheets, VBA and BI question bank.')]),

 ('02-SQL', 'SQL',
  'Every query in the book, written for PostgreSQL and MySQL, against one database you load once.',
  [('00-Databases', ['(shared)'],
    'Load one of these first. riverstone_setup_mini is 24 customers for learning; '
    'riverstone_2025 is one year; the full setup is five thousand customers and a hundred '
    'thousand orders for when you want queries to take real time.'),
   ('01-Foundations', ['ch12'],
    'SELECT, WHERE, JOIN, GROUP BY. Both dialects, every query from the chapter.'),
   ('02-Real-analysis', ['ch13'],
    'CTEs, window functions, ranking, running totals, and the calendar tables that make date '
    'analysis work.'),
   ('03-Cleaning', ['ch14'],
    'The whole cleaning pipeline in SQL: load, clean, compare. The messy source is in the '
    'datasets folder.'),
   ('04-For-charts-and-BI', ['ch15', 'ch16'],
    'The queries that feed a chart and a Power BI model, including the checks that prove the '
    'model matches the source.'),
   ('05-In-a-real-project', ['ch26', 'ch27'],
    'SQL as it appears in version control: one query per file, reviewed in steps.'),
   ('06-Advanced-and-performance', ['ch28'],
    'Recursive CTEs, window frames, EXPLAIN, indexes and dimensional modelling.'),
   ('07-Analytics-engineering-dbt', ['ch32'],
    'A working dbt project: models, tests and schema files.'),
   ('08-Quality-and-activation', ['ch47', 'ch51', 'ch64'],
    'Data contracts, reverse ETL and the access-control queries.'),
   ('09-Interview-drills', ['ch71', 'ch77', 'ch82'],
    'The question banks, and the take-home SQL.')]),

 ('03-Python', 'Python',
  'From your first line to a program that runs itself on a schedule.',
  [('01-From-zero', ['ch17'],
    'The language itself, with the data files the chapter reads. Start here even if you have '
    'written code before — the folder conventions carry through everything else.'),
   ('02-pandas-and-automation', ['ch18'],
    'The analyst\'s toolkit, then the payoff: classes, an entry point, a .bat file and a '
    'scheduled monthly report that writes Excel and Markdown.'),
   ('03-Reports-and-delivery', ['ch20'],
    'Turning a notebook into something that lands in an inbox.'),
   ('04-Software-not-scripts', ['ch29'],
    'The same code as a package: modules, tests, configuration and a CLI. Sixteen files that '
    'make one project.'),
   ('05-Computer-science', ['ch33'],
    'Structures and algorithms, with the measurements.'),
   ('06-Interview-drills', ['ch72', 'ch72a'],
    'The Python, pandas and DSA question banks as runnable notebooks.')]),

 ('04-Statistics-and-experiments', 'Statistics & experiments',
  'Describing data, testing a claim, and arguing about cause.',
  [('01-Describing-data', ['ch21'], 'Distributions, spread, probability.'),
   ('02-Not-fooling-yourself', ['ch22'], 'Tests, intervals, and the traps. The spreadsheet '
    'version of this stage is in the Excel folder.'),
   ('03-Experiments', ['ch30'], 'Designing and reading an A/B test.'),
   ('04-Causal-inference', ['ch31'], 'When you cannot run the experiment.'),
   ('05-The-maths', ['ch35'], 'The mathematics under the models.'),
   ('06-Interview-drills', ['ch73'], 'The statistics and experimentation bank.')]),

 ('05-Machine-learning', 'Machine learning',
  'The workflow, the algorithms, and the honest evaluation of both.',
  [('01-Workflow-and-features', ['ch36'], 'The shape of every project.'),
   ('02-Algorithms', ['ch37', 'ch38'], 'Supervised and unsupervised.'),
   ('03-Evaluation-and-honesty', ['ch39'], 'Tuning, interpretation, and what not to claim.'),
   ('04-Specialised', ['ch40', 'ch41', 'ch42'], 'Time series, text, recommenders.'),
   ('05-Deep-learning', ['ch43', 'ch53'], 'A first look, then the depth.'),
   ('06-Capstone', ['ch44'], 'End to end, on your own data.'),
   ('07-Interview-drills', ['ch74'], 'The machine learning bank.')]),

 ('06-Data-engineering', 'Data engineering',
  'Moving data reliably, at a size where it stops being easy.',
  [('01-Ingestion', ['ch45'], 'Getting data in.'),
   ('02-Pipelines-and-orchestration', ['ch46'], 'Making it run on its own.'),
   ('03-Quality-and-observability', ['ch47'], 'Knowing when it did not.'),
   ('04-Scale-and-storage', ['ch48', 'ch49'], 'Distributed compute, warehouses and lakehouses.'),
   ('05-Streaming', ['ch50'], 'Real time.'),
   ('06-Activation-and-infrastructure', ['ch51', 'ch52'], 'Getting data back out, and the cloud '
    'it all runs on.'),
   ('07-Interview-drills', ['ch77', 'ch78'],
    'The data engineering bank, and the automation and integration bank — retries, webhooks, idempotency and rate limits, which are engineering questions wherever they are asked.')]),

 ('07-GenAI-and-production-AI', 'Generative AI & production ML',
  'Language models, retrieval, and keeping any of it alive in production.',
  [('01-LLM-foundations', ['ch54'], 'Tokens, embeddings, prompting.'),
   ('02-Building-AI-applications', ['ch55'], 'RAG, agents and evaluation — with a corpus of '
    'twenty-eight documents to retrieve from.'),
   ('03-MLOps', ['ch56'], 'Making models survive.'),
   ('04-LLMOps', ['ch57'], 'The same, for language models.'),
   ('05-Intelligent-automation', ['ch58'], 'Putting it to work.'),
   ('06-Interview-drills', ['ch79'], 'The GenAI and MLOps bank.')]),

 ('08-Command-line-and-tooling', 'Command line, Git & the toolkit',
  'The tools around the work: the shell, version control, and the files a project needs.',
  [('01-The-command-line', ['ch34'], 'Linux, networking, and sixty-four files to practise on.'),
   ('02-Git-and-documentation', ['ch26'], 'Version control, and the SQL that lives in it.'),
   ('03-Setup-checks', ['ch06'], 'Confirming your machine is ready.')]),

 ('09-Architecture-and-the-business', 'Architecture & the business',
  'The documents and models of someone who decides rather than builds.',
  [('01-Requirements-and-storytelling', ['ch24'], 'Turning a request into a specification.'),
   ('02-Business-metrics', ['ch23'], 'KPIs, unit economics, and the numbers behind them.'),
   ('03-Designing-systems', ['ch60', 'ch61', 'ch62'], 'Whole systems, trade-offs, patterns.'),
   ('04-Governance-and-cost', ['ch63', 'ch64', 'ch65'],
    'Automation governance, security and privacy, and what it all costs.'),
   ('05-Strategy-and-teams', ['ch66'], 'Maturity, and building the team.'),
   ('06-Interview-drills', ['ch80'], 'The architecture and leadership bank.')]),

 ('10-Take-home-assignments', 'Take-home assignments',
  'Timed, realistic briefs — the closest thing here to a real interview task.',
  [('01-Assignments', ['ch82'], 'The take-homes and mock interviews, with their data.')]),
]


def chapter_titles():
    out = {}
    for p in MS.glob('ch*.md'):
        k = p.name.split('-')[0]
        first = p.read_text(encoding='utf-8').splitlines()[0]
        out[k] = re.sub(r'^Chapter [\w]+\.\s*', '', first.lstrip('# ').strip())
    return out


def tracked():
    out = subprocess.run(['git', 'ls-files', 'Data Science/Analyst-to-Architect/companion'],
                         cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    keep = []
    for f in out:
        if any(rx.search(f) for rx in EXCLUDE):
            continue
        keep.append(f)
    return keep


def owner(relpath):
    """Which chapter folder a companion path belongs to, or '(shared)' for the top level."""
    m = re.match(r'(ch\d+[a-z]?)/', relpath)
    return m.group(1) if m else '(shared)'


def folder_name(title):
    """A readable folder name from a chapter title: no numbers, no punctuation, no surprises."""
    s = re.sub(r'[^\w\s&-]', '', title).strip()
    s = re.sub(r'\s*&\s*', ' and ', s)
    s = re.sub(r'\s+', '-', s)
    return s[:52].rstrip('-')


def human(n):
    for u in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or u == 'GB':
            return f'{n:.0f} {u}' if u == 'B' else f'{n:.1f} {u}'
        n /= 1024


def build(dest):
    dest = pathlib.Path(dest).resolve()
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    titles = chapter_titles()
    files = tracked()
    by_owner = collections.defaultdict(list)
    for f in files:
        rel = f.split('companion/', 1)[1]
        by_owner[owner(rel)].append((f, rel))

    claimed, copied, stage_rows, collisions = set(), 0, [], []
    kept_readmes = {}

    for tool_dir, tool_name, tool_blurb, stages in TOOLS:
        tdir = dest / tool_dir
        stage_lines = []
        tool_files = 0
        for stage_dir, chapters, blurb in stages:
            sdir = tdir / stage_dir
            n_here = 0
            chapter_notes = []
            # Chapter numbers are the book's filing system, not the learner's. When a stage draws
            # on one chapter the files sit directly in it; when it draws on several they are
            # separated by a readable name taken from the chapter title, never "ch42".
            present = [c for c in chapters if by_owner.get(c)]
            split = len(present) > 1
            for ch in present:
                entries = by_owner[ch]
                claimed.add(ch)
                learner, gens = [], []
                for src, rel in entries:
                    (gens if GENERATOR.search('/' + rel) else learner).append((src, rel))
                group = folder_name(titles.get(ch, 'Shared data')) if split else ''
                for src, rel in learner + gens:
                    # Strip the chapter folder, because a chapter number means nothing here. For
                    # the shared data there is no chapter folder to strip: its first component is
                    # a real folder (full/, mysql/, postgresql/) and removing it would collide
                    # postgresql/riverstone_2025_setup.sql with the one at the root.
                    inner = rel.split('/', 1)[1] if ch != '(shared)' and '/' in rel else rel
                    parts = [sdir]
                    if group:
                        parts.append(group)
                    if GENERATOR.search('/' + rel):
                        parts.append('_build-scripts')
                    target = pathlib.Path(*parts) / inner
                    # Some chapters ship their own README.md. The stage's generated README is
                    # written afterwards and would silently destroy it, so the book's one is
                    # kept under a name that cannot clash and is linked from the generated one.
                    if target.name == 'README.md' and target.parent in (sdir, sdir / group
                                                                        if group else sdir):
                        target = target.with_name('README-from-the-book.md')
                        kept_readmes.setdefault(str(sdir), []).append(target.name)
                    if target.exists():
                        collisions.append((str(target.relative_to(dest)), src))
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT / src, target)
                    n_here += 1
                    copied += 1
                title = titles.get(ch, 'The Riverstone data and its database setup scripts')
                chapter_notes.append((group or '(here)', title, len(learner), len(gens)))
            if n_here:
                sdir.mkdir(parents=True, exist_ok=True)
                write_stage_readme(sdir, tool_name, stage_dir, blurb, chapter_notes,
                                   kept_readmes.get(str(sdir), []))
                stage_lines.append((stage_dir, blurb, n_here, chapter_notes))
                tool_files += n_here
        if stage_lines:
            write_tool_readme(tdir, tool_name, tool_blurb, stage_lines)
            stage_rows.append((tool_dir, tool_name, len(stage_lines), tool_files))

    # ------------------------------------------------------------------ nothing overwritten
    if collisions:
        print('COLLISIONS: two sources wrote to the same place, so a file was lost:')
        for tgt, src in collisions[:20]:
            print(f'  {tgt}  <- {src}')
        raise SystemExit(f'{len(collisions)} collisions; the arena would be missing files')

    # ------------------------------------------------------------------ completeness
    orphans = sorted(set(by_owner) - claimed)
    if orphans:
        print('ORPHANED chapter folders, claimed by no tool:')
        for o in orphans:
            print(f'  {o:<8} {titles.get(o,"?")[:50]}  ({len(by_owner[o])} files)')
        raise SystemExit('every companion folder must be claimed by a tool; fix the TOOLS map')

    # ------------------------------------------------------------------ prove it landed
    # Counting what was written is not the same as checking it is there. Every source file must
    # be byte-for-byte present somewhere in the arena, or the build says so and stops.
    import hashlib

    def digest(f):
        h = hashlib.sha256()
        with open(f, 'rb') as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b''):
                h.update(chunk)
        return h.hexdigest()

    arena_hashes = collections.Counter()
    for f in dest.rglob('*'):
        if f.is_file():
            arena_hashes[digest(f)] += 1
    absent = [f for f in files if digest(ROOT / f) not in arena_hashes]
    if absent:
        print(f'{len(absent)} source files are not present in the arena:')
        for f in absent[:20]:
            print('  ', f)
        raise SystemExit('the arena is missing material; not writing it out as complete')
    print(f'verified: all {len(files)} tracked practice files are present, by content hash')

    write_chapter_lookup(dest, titles, by_owner)
    write_root_readme(dest, stage_rows, copied, len(files))
    total = sum(f.stat().st_size for f in dest.rglob('*') if f.is_file())
    print(f'\n{"tool":<34}{"stages":>8}{"files":>8}')
    for d, n, s, f in stage_rows:
        print(f'  {n:<32}{s:>8}{f:>8}')
    print(f'\n{copied} files copied from {len(files)} tracked, {human(total)}')
    print(f'arena -> {dest}')
    return dest


def write_stage_readme(sdir, tool, stage, blurb, notes, kept=()):
    name = re.sub(r'^\d+-', '', stage).replace('-', ' ')
    L = [f'# {tool} — {name[0].upper()}{name[1:]}', '', blurb, '', '## What is in here', '',
         '| Where | Taught in | Files to work with | Build scripts |', '|---|---|---|---|']
    for group, title, nl, ng in notes:
        where = 'this folder' if group == '(here)' else f'`{group}/`'
        L.append(f'| {where} | {title} | {nl} | {ng if ng else "—"} |')
    if kept:
        L += ['', "## The chapter's own notes", '',
              'This folder also carries the notes the book ships with it. They are worth reading '
              'and they are not the same as this page:', '']
        L += [f'- **[{k}]({k})**' for k in sorted(set(kept))]
    L += ['', 'Anything under `_build-scripts/` generates the practice data rather than teaching '
          'you something. You do not need to run it — the data is already here — but it is '
          'included so you can see how the data was made, and rebuild it if you change something.',
          '']
    (sdir / 'README.md').write_text('\n'.join(L), encoding='utf-8')


def write_tool_readme(tdir, tool, blurb, stages):
    L = [f'# {tool}', '', blurb, '',
         'Work through the folders in order. Each one assumes the one before it.', '',
         '| Stage | What it covers | Files |', '|---|---|---|']
    for stage, sb, n, _ in stages:
        nm = re.sub(r'^\d+-', '', stage).replace('-', ' ')
        L.append(f'| **{stage}** | {sb} | {n} |')
    L += ['', '## Where this comes from', '',
          'These are the same files as the book\'s `companion/` folder, copied and regrouped by '
          'tool. The book refers to them by chapter — `companion/ch18/` and so on — and that '
          'folder is unchanged, so both views work. Each stage\'s README says which chapter its '
          'files came from.', '']
    (tdir / 'README.md').write_text('\n'.join(L), encoding='utf-8')


def write_chapter_lookup(dest, titles, by_owner):
    """A chapter-to-arena index, so a reference in the book still finds its files.

    The book says "see companion/ch18/". A reader holding the Arena needs one lookup to turn that
    into a folder, and this is it. It is generated from the same TOOLS map, so it cannot drift.
    """
    where = {}
    for tool_dir, tool_name, _b, stages in TOOLS:
        for stage_dir, chapters, _sb in stages:
            present = [c for c in chapters if by_owner.get(c)]
            split = len(present) > 1
            for ch in present:
                group = folder_name(titles.get(ch, 'Shared data')) if split else ''
                path = f'{tool_dir}/{stage_dir}' + (f'/{group}' if group else '')
                where.setdefault(ch, []).append((tool_name, path))

    def key(c):
        if c == '(shared)':
            return (999, '')
        m = re.match(r'ch(\d+)([a-z]?)', c)
        return (int(m.group(1)), m.group(2))

    L = ['# Where is my chapter?', '',
         '*The book refers to its practice files by chapter — "see `companion/ch18/`". '
         'This turns that into a folder in the Arena.*', '',
         'A chapter can appear in more than one place when its material serves two tools: '
         "Chapter 15's chart data is useful in Excel and in SQL, so it is in both.", '',
         '| Chapter | Title | Where it is in the Arena |', '|---|---|---|']
    for ch in sorted(where, key=key):
        name = 'Shared Riverstone data' if ch == '(shared)' else titles.get(ch, '')
        label = 'the shared data' if ch == '(shared)' else ch
        places = ' <br> '.join(f'**{t}** → `{p}/`' for t, p in where[ch])
        L.append(f'| `{label}` | {name} | {places} |')
    L += ['', 'Chapters not listed here have no practice files of their own — they are reading '
          "chapters, or they use another chapter's data and say so.", '']
    (dest / 'WHERE-IS-MY-CHAPTER.md').write_text(chr(10).join(L), encoding='utf-8')


def write_root_readme(dest, rows, copied, tracked_n):
    L = ['# The Practice Arena', '',
         '*Everything you practise with, arranged by the tool you want to use.*', '',
         'The book is organised by chapter, because a book has to be. This is the same material '
         'organised the way you would actually go looking for it: pick the tool, start at stage '
         '01, and work down. Each stage builds on the one before, from the smallest idea to a '
         'finished thing you can run.', '',
         'Reading the book and it says "see `companion/ch18/`"? '
         '**[Where is my chapter?](WHERE-IS-MY-CHAPTER.md)** turns any chapter reference into a '
         'folder here.', '',
         '| | Tool | What it is for | Stages | Files |', '|---|---|---|---|---|']
    blurbs = {t[1]: t[2] for t in TOOLS}
    for i, (d, n, s, f) in enumerate(rows, 1):
        L.append(f'| {i} | **[{n}]({d}/)** | {blurbs[n]} | {s} | {f} |')
    L += ['', '## How to use it', '',
          '- **Pick one tool and stay in it.** You do not need the others to make progress.',
          '- **Go in order within a tool.** Stage 03 assumes stage 02; the numbering is the '
          'teaching order, not a filing convention.',
          '- **Every stage has a README** saying what it covers, which chapter it came from, and '
          'how many files are yours to work with.',
          '- **`_build-scripts/` folders are optional.** They generate the practice data, which is '
          'already here. They are included so nothing is a black box.', '',
          '## Running things', '',
          '| Tool | What you need |', '|---|---|',
          '| Excel workbooks | Excel or Google Sheets. No macros are enabled in any file; the '
          'macro chapter asks you to write them yourself |',
          '| SQL | PostgreSQL (the book\'s primary) or MySQL. Load a database from '
          '`02-SQL/00-Databases/` first — that is the only setup step |',
          '| Python notebooks | Python 3.11 or newer, then `pip install jupyter pandas numpy '
          'matplotlib`. Outputs are saved, so you can read without running |',
          '| Everything else | Each stage\'s README says |', '',
          '## What is not here', '',
          'The large generated datasets — the ones the data-engineering chapters build, tens of '
          'gigabytes of them — are not included. The scripts in `_build-scripts/` rebuild them in '
          'about a minute, which is how the book is designed to work.', '',
          '## Keeping it current', '',
          'This folder is generated from the book\'s companion material by '
          '`tools/review-export/make_practice_arena.py`. Rebuild it after any change and it is '
          'back in step. The build refuses to finish if any practice file is left unclaimed by a '
          f'tool, so nothing can quietly go missing: {copied} of {tracked_n} tracked files are '
          'placed, and the remainder are the configuration files that are not practice material.',
          '']
    (dest / 'README.md').write_text('\n'.join(L), encoding='utf-8')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dest')
    a = ap.parse_args()
    build(a.dest)
