"""Assemble the review bundle: the books, the practice material, the guide, and the review state.

The bundle is built outside the repository, because it is roughly 300 MB and most of that is
copies of files the repository already holds. Nothing here is generated content: it is the
existing material, organised so one folder can be read top to bottom, and zipped so it can be
moved to another machine.

What goes in, and what does not:

- **The order.** Product order, not file type: 00 start here, 01 the interview book (the
  product), 02 the volumes with their practice files (first add-on), 03 projects (second add-on),
  04 material for review only.
- **The books.** The four books from `fixed/Books`, renamed to match that order.
- **The practice material.** Only what git tracks, about 92 MB. The other 317 MB in `companion/`
  is generated data — the large parquet and CSV files the data-engineering chapters build — and
  the chapter scripts rebuild it on demand, which is why the repository ignores it. Shipping it
  would triple the bundle to carry files the reader can make in a minute.
- **The guide and the review documents**, which are small.

    python tools/review-export/make_bundle.py <destination folder> [--zip]
"""
import argparse
import pathlib
import shutil
import subprocess
import sys
import zipfile

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[2]
BOOK = ROOT / 'Data Science' / 'Analyst-to-Architect'
sys.path.insert(0, str(HERE.parent))   # so the Arena builder can be imported


def tracked(path):
    """Files git tracks under `path`, relative to the repository root."""
    out = subprocess.run(['git', 'ls-files', str(path.relative_to(ROOT))],
                         cwd=ROOT, capture_output=True, text=True)
    return [ROOT / line for line in out.stdout.splitlines() if line.strip()]


def copy(src, dst, label, log):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    log.append((label, dst, src.stat().st_size))


def human(n):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB':
            return f'{n:.0f} {unit}' if unit == 'B' else f'{n:.1f} {unit}'
        n /= 1024


def build(dest, make_zip):
    dest = pathlib.Path(dest).resolve()
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    log = []

    # The bundle follows the product order (owner decision, 3 Oct 2026): the interview book is
    # the product; the volumes with their practice files are the first add-on; projects are the
    # second. Internal material is fenced off in a folder buyers never see.
    RV = ROOT / 'review' / 'for-abhishek'
    BOOKS = ROOT / 'fixed' / 'Books'

    def opt(src, dst, label):
        if src.exists():
            copy(src, dst, label, log)

    # ---------------------------------------------------------------- 00. start here
    for ext in ('.pdf', '.docx'):
        opt(RV / f'Bundle-start-here{ext}', dest / f'00-Start-here{ext}', 'start here')

    # ---------------------------------------------------------------- 01. the interview book
    ib = dest / '01-The-Interview-Book'
    opt(BOOKS / 'Analyst-to-Architect-Book-4-Be-Interview-Ready.pdf',
        ib / 'Be-Interview-Ready-Data-Science-and-Analytics.pdf', 'interview book')
    for name in ('front-cover.pdf', 'back-cover.pdf', 'front-cover.png', 'back-cover.png',
                 'instagram-front.png'):
        opt(RV / 'cover' / name, ib / 'Covers' / name, 'interview book')

    # ---------------------------------------------------------------- 02. add-on: the volumes
    vol = dest / '02-Add-on-The-Volumes'
    for n, stem, nice in [(1, 'Theory', 'Volume-1-Theory'), (2, 'Practical', 'Volume-2-Practical'),
                          (3, 'Implementation', 'Volume-3-Implementation')]:
        opt(BOOKS / f'Analyst-to-Architect-Book-{n}-{stem}.pdf', vol / f'{nice}.pdf', 'volumes')
    for name in ['Where-Everything-Is.pdf', 'Where-Everything-Is.xlsx']:
        opt(RV / name, vol / 'Topic-guide' / name, 'volumes')
    # The practice files, arranged by tool, not by chapter. The chapter view lives in the
    # repository and the volumes refer to it; WHERE-IS-MY-CHAPTER.md maps one onto the other.
    import make_practice_arena
    arena = vol / 'Practice-Files'
    make_practice_arena.build(arena)
    for f in sorted(arena.rglob('*')):
        if f.is_file():
            log.append(('practice files', f, f.stat().st_size))

    # ---------------------------------------------------------------- 03. add-on: projects
    pj = dest / '03-Add-on-Projects'
    for ext in ('.pdf', '.docx'):
        opt(RV / f'Product-ladder-and-project-catalogue{ext}', pj / f'Project-catalogue{ext}', 'projects')
    pj.mkdir(parents=True, exist_ok=True)
    note = pj / 'README.md'
    note.write_text('\n'.join([
        '# Projects: an add-on, sold one at a time',
        '',
        'Ready-made portfolio projects, each with a realistic brief, messy data, a runnable worked',
        'solution, the reasoning behind it, and how to talk about it in an interview.',
        '',
        '**None is built yet.** `Project-catalogue.pdf` is the design and the list. The first to',
        'build is P1, the daily report that sends itself.',
        '']), encoding='utf-8')
    log.append(('projects', note, note.stat().st_size))

    # ---------------------------------------------------------------- 04. for review only
    rv = dest / '04-For-review-only'
    opt(BOOKS / 'Analyst-to-Architect-Book-Overview.pdf', rv / 'Internal-overview-not-for-sale.pdf', 'review only')
    for stem in ['Ch72B-data-cleaning-and-wrangling-bank', 'Ch76B-business-analyst-bank',
                 'Part-VIII-predict-the-output-summary', 'Ch71-section-71.11-predict-the-output',
                 'Selling-the-books-strategy-and-red-team', 'Read-me-first']:
        for ext in ('.pdf', '.docx'):
            opt(RV / f'{stem}{ext}', rv / 'Whats-new-and-strategy' / f'{stem}{ext}', 'review only')
    for name in ['TRACKER.md', 'DECISIONS.md', 'DECISIONS-BRIEFING.md',
                 'REVIEW-STATUS.md', 'REVIEW-GAPS.md', 'START-HERE.md']:
        opt(ROOT / name, rv / 'Review-state' / name, 'review only')
    opt(ROOT / 'review' / 'Book-Review-Action-Register.xlsx',
        rv / 'Review-state' / 'Book-Review-Action-Register.xlsx', 'review only')
    for f in sorted((ROOT / 'changelog').glob('*.md')):
        copy(f, rv / 'Review-state' / 'changelog' / f.name, 'review only', log)

    # ---------------------------------------------------------------- the manifest
    groups = {}
    for label, path, size in log:
        g = groups.setdefault(label, [0, 0])
        g[0] += 1
        g[1] += size
    total = sum(s for _, _, s in log)

    print(f'{"what":<16}{"files":>7}{"size":>12}')
    for label, (n, s) in groups.items():
        print(f'{label:<16}{n:>7}{human(s):>12}')
    print(f'{"TOTAL":<16}{len(log):>7}{human(total):>12}')
    print(f'\nbundle -> {dest}')

    if make_zip:
        zpath = dest.with_suffix('.zip')
        print(f'zipping to {zpath} ...', flush=True)
        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for f in sorted(dest.rglob('*')):
                if f.is_file():
                    z.write(f, pathlib.Path(dest.name) / f.relative_to(dest))
        print(f'zip    -> {zpath}  ({human(zpath.stat().st_size)})')
    return dest, log, total


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dest')
    ap.add_argument('--zip', action='store_true')
    a = ap.parse_args()
    build(a.dest, a.zip)
