"""Assemble the review bundle: the books, the practice material, the guide, and the review state.

The bundle is built outside the repository, because it is roughly 300 MB and most of that is
copies of files the repository already holds. Nothing here is generated content: it is the
existing material, organised so one folder can be read top to bottom, and zipped so it can be
moved to another machine.

What goes in, and what does not:

- **The books.** The five PDFs from `fixed/Books`.
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

    # ---------------------------------------------------------------- 1. the books
    for p in sorted((ROOT / 'fixed' / 'Books').glob('*.pdf')):
        copy(p, dest / '01-Books' / p.name, 'book', log)
    readme = ROOT / 'fixed' / 'Books' / 'README.md'
    if readme.exists():
        copy(readme, dest / '01-Books' / 'README.md', 'book', log)

    # ---------------------------------------------------------------- 2. the guide
    for name in ['Where-Everything-Is.pdf', 'Where-Everything-Is.docx',
                 'Where-Everything-Is.xlsx', 'Where-Everything-Is.md']:
        p = ROOT / 'review' / 'for-abhishek' / name
        if p.exists():
            copy(p, dest / '02-Guide' / name, 'guide', log)

    # ---------------------------------------------------------------- 3. what is new
    for p in sorted((ROOT / 'review' / 'for-abhishek').glob('Ch71-section-71.11*')):
        if p.suffix in ('.pdf', '.docx'):
            copy(p, dest / '03-Whats-new' / p.name, 'what is new', log)
    for name in ['ch71.md', 'ch18.md']:
        p = ROOT / 'changelog' / name
        if p.exists():
            copy(p, dest / '03-Whats-new' / f'changelog-{name}', 'what is new', log)

    # ---------------------------------------------------------------- 4. the practice material
    for src in tracked(BOOK / 'companion'):
        if not src.exists():
            continue
        rel = src.relative_to(BOOK / 'companion')
        copy(src, dest / '04-Practice' / rel, 'practice', log)

    # ---------------------------------------------------------------- 5. the review state
    for name in ['TRACKER.md', 'DECISIONS.md', 'DECISIONS-BRIEFING.md',
                 'REVIEW-STATUS.md', 'REVIEW-GAPS.md', 'START-HERE.md']:
        p = ROOT / name
        if p.exists():
            copy(p, dest / '05-Review-state' / name, 'review state', log)
    reg = ROOT / 'review' / 'Book-Review-Action-Register.xlsx'
    if reg.exists():
        copy(reg, dest / '05-Review-state' / reg.name, 'review state', log)
    for p in sorted((ROOT / 'changelog').glob('*.md')):
        copy(p, dest / '05-Review-state' / 'changelog' / p.name, 'review state', log)

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
