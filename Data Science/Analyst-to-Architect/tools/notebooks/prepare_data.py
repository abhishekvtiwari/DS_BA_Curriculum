"""Build every practice dataset the chapters need, before the notebooks are run.

The book's design is that datasets are generated rather than shipped: each generator is seeded, so
it produces the same file every time, and the figures in the chapters match. The global generators
in companion/ build the Riverstone databases used across many chapters; each chapter that needs
something of its own carries its own builder.

Order matters: the globals first, because several chapter builders read from them.

    python tools/notebooks/prepare_data.py            # everything
    python tools/notebooks/prepare_data.py ch30 ch31   # just these chapters' builders
"""
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
COMP = ROOT / 'companion'

# Global Riverstone generators, in the order the book introduces them.
GLOBAL = ['generate_riverstone_full.py', 'generate_riverstone_2025.py',
          'generate_riverstone_crm.py', 'generate_riverstone_accounts.py',
          'generate_riverstone_baskets.py', 'generate_riverstone_demand.py',
          'generate_riverstone_sensors.py', 'generate_riverstone_tickets.py']

# A builder by name, but not actually one: a learner's environment check, a finished report that
# needs a live database, or a module the chapter imports rather than runs.
NOT_A_BUILDER = {'check_setup.py', 'daily_flash.py', 'format_test.py', 'retrieval.py',
                 'pipeline.py', 'questions_stream.py', 'lead_data.py', 'churn_data.py',
                 'match_fast.py', 'clean_orders_pandas.py', 'make_mysql_queries.py',
                 'build_ch14_sql.py', 'make_full_insert_scripts.py'}

BUILDER = re.compile(r'^(build_|make_|generate_|setup_ch)')


def run(script, label, timeout=900):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, script.name], cwd=script.parent,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return label, 'TIMED OUT', ''
    took = f'{time.time() - t0:.0f}s'
    if p.returncode == 0:
        last = [l for l in (p.stdout or '').strip().splitlines() if l.strip()]
        return label, f'ok {took}', (last[-1][:90] if last else '')
    err = (p.stderr or '').strip().splitlines()
    why = next((l for l in reversed(err) if l.strip() and not l.startswith(' ')), '')
    return label, 'failed', why[:110]


def chapter_builders(only=None):
    out = []
    for d in sorted(COMP.glob('ch*')):
        if not d.is_dir():
            continue
        if only and d.name not in only:
            continue
        for f in sorted(d.rglob('*.py')):
            if f.name in NOT_A_BUILDER or not BUILDER.match(f.name):
                continue
            out.append((f, f'{d.name}/{f.name}'))
    return out


def place_datasets():
    """Copy a dataset next to the chapter that reads it by a bare filename.

    Some chapters read "leads.csv" rather than "../crm/leads.csv", because the chapter expects the
    reader to be working in the folder that holds it. A copy beside the chapter lets the notebook
    run from the chapter's own folder, which is where a reader opens it. Without this, Chapter 36
    could run 3 of its 57 cells; with it, all 57.
    """
    import shutil
    index = {}
    for f in COMP.rglob('*'):
        if f.is_file() and f.suffix in {'.csv', '.parquet', '.xlsx', '.json'}:
            index.setdefault(f.name, f)
    pat = re.compile(r'read_(?:csv|parquet|excel|json)\(\s*["\']'
                     r'([A-Za-z0-9_.-]+\.(?:csv|parquet|xlsx|json))["\']')
    placed = []
    for md in sorted((ROOT / 'manuscript').glob('ch*.md')):
        key = md.name.split('-')[0]
        for m in pat.finditer(md.read_text(encoding='utf-8')):
            name = m.group(1)
            dest = COMP / key / name
            if dest.exists() or name not in index:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(index[name], dest)
            placed.append(f'{key}/{name}')
    return placed


if __name__ == '__main__':
    only = set(sys.argv[1:]) or None
    jobs = []
    if not only:
        jobs += [(COMP / g, g) for g in GLOBAL if (COMP / g).exists()]
    jobs += chapter_builders(only)

    print(f"{len(jobs)} builders to run\n")
    print(f"{'builder':<42}{'result':<12}note")
    ok = bad = 0
    failures = []
    for script, label in jobs:
        label, result, note = run(script, label)
        print(f"{label:<42}{result:<12}{note}")
        if result.startswith('ok'):
            ok += 1
        else:
            bad += 1
            failures.append((label, note))
    print(f"\n{ok} built, {bad} failed")

    placed = place_datasets()
    if placed:
        print(f"\ndatasets copied beside the chapter that reads them ({len(placed)}):")
        for x in placed:
            print(f"  {x}")

    if failures:
        print("\nfailed, and why:")
        for label, note in failures:
            print(f"  {label}: {note}")
