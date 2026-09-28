#!/usr/bin/env python3
"""
verify_sql.py - check that every SQL result printed in a chapter matches what the database really returns.

Usage:  python3 verify_sql.py path/to/chapter.md [--db riverstone]

Conventions it understands (see planning/chapter-writing-instructions.md, section 9):
  ```sql      block  -> run in PostgreSQL (psql); the next plain ``` block is its expected output
  ```mysql    block  -> run in MySQL (mysql -t); the next plain ``` block is its expected output
  <!-- db: NAME -->  -> switch the database used for later blocks (both engines)
  <!-- lab:start --> ... <!-- lab:end -->
                     -> a stateful lab: every block runs in order in database riverstone_lab, including
                        CREATE/INSERT/UPDATE/ALTER/DROP. The lab is reset (dropped) at the FIRST lab region
                        of the file only; later lab regions (e.g. exercise answers) continue from its state.
     inside a lab:  <!-- run: pg|mysql|both|none --> before a code block chooses the engine(s);
                    <!-- out: mysql --> (or pg) before an output block says whose output it is.
Outside labs, blocks that change data or structure are skipped (they are not re-runnable).
Expected errors: an output block containing "ERROR" passes if the real error's first line matches.
Requires: psql as user postgres, and a mysql client with root access, on the same machine.
Exit code: 0 if everything matches, 1 otherwise.
"""
import re, subprocess, sys, argparse

def run_pg(sql, db):
    if re.search(r'\b(CREATE|DROP|ALTER) DATABASE\b', sql): db = 'postgres'
    r = subprocess.run(['su', 'postgres', '-c', f'psql -X -q -d {db}'], input=sql,
                       capture_output=True, text=True, cwd='/tmp')
    return r.stdout + r.stderr

def run_my(sql, db):
    args = ['mysql', '-uroot', '-t']
    if not re.search(r'^\s*(CREATE|DROP) DATABASE\b', sql, re.I | re.M) or re.search(r'\b(RENAME TABLE|SELECT|USE)\b', sql):
        args.append(db)
    r = subprocess.run(args, input=sql, capture_output=True, text=True)
    return r.stdout + re.sub(r' at line \d+', '', r.stderr)

def norm(s):
    out = []
    for l in s.strip().splitlines():
        l = re.sub(r'\s+', ' ', l).strip()
        if not l or re.fullmatch(r'[-+ |]+', l) or l.startswith(('NOTICE', 'LINE', 'HINT:')) or l == '^':
            continue
        out.append(l)
    return out

def compare(expected, got):
    e, g = norm(expected), norm(got)
    if not any(re.match(r'\(\d+ rows?\)', x) for x in e):
        g = [x for x in g if not re.match(r'\(\d+ rows?\)', x)]
    if 'ERROR' in expected:
        e1 = [x for x in e if 'ERROR' in x][:1]
        return bool(e1) and any(e1[0] in x for x in g)
    return e == g

DML = re.compile(r'^\s*(BEGIN|START TRANSACTION|CREATE|INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|RENAME)\b', re.I | re.M)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--db', default='riverstone')
    a = ap.parse_args()
    md = open(a.path, encoding='utf-8').read()
    token = re.compile(r'<!-- (db|run|out): ([\w]+) -->|<!-- lab:(start|end) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
    db = a.db; in_lab = False; pending_run = None; pending_out = None
    last = {}; checked = bad = ran = 0; labs_seen = False
    for m in token.finditer(md):
        line = md[:m.start()].count('\n') + 1
        if m.group(1) == 'db': db = m.group(2); continue
        if m.group(1) == 'run': pending_run = m.group(2); continue
        if m.group(1) == 'out': pending_out = m.group(2); continue
        if m.group(3) == 'start':
            in_lab = True; last = {}
            if labs_seen: continue
            labs_seen = True
            run_pg('DROP DATABASE IF EXISTS riverstone_lab;', 'postgres')
            subprocess.run(['mysql', '-uroot', '-e', 'DROP DATABASE IF EXISTS riverstone_lab; DROP DATABASE IF EXISTS archive;'])
            continue
        if m.group(3) == 'end': in_lab = False; last = {}; continue
        lang, body = m.group(4), m.group(5)
        if lang in ('sql', 'mysql'):
            engine = pending_run or ('mysql' if lang == 'mysql' else 'pg'); pending_run = None
            last = {}
            if engine == 'none': continue
            if not in_lab and DML.search(body): continue
            use_db = 'riverstone_lab' if in_lab else db
            if engine in ('pg', 'both'): last['pg'] = run_pg(body, use_db); ran += 1
            if engine in ('mysql', 'both'): last['mysql'] = run_my(body, use_db); ran += 1
            last['_next'] = 'mysql' if engine == 'mysql' else 'pg'
            for k in ('pg', 'mysql'):
                if k in last and 'ERROR' in last[k]:
                    print(f'  note: {k} raised an error at line {line}:', [x for x in last[k].splitlines() if 'ERROR' in x][0][:100])
            continue
        if lang == '' and last:
            target = pending_out or last.get('_next'); pending_out = None
            if target in last:
                checked += 1
                if not compare(body, last[target]):
                    bad += 1
                    print(f'MISMATCH at line {line} ({target})')
                    print('  expected:', norm(body)[:6]); print('  got     :', norm(last[target])[:6])
            last['_next'] = None
            continue
        pending_out = None
        # a "run:" marker belongs to the very next code block: if that block isn't SQL, drop it, or it
        # would leak to the next SQL block (reported by the Ch 32 build)
        if lang: pending_run = None
    print(f'{a.path}: statements run {ran}, outputs checked {checked}, mismatches {bad}')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
