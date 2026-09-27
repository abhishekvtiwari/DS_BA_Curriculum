#!/usr/bin/env python3
"""ch28_fill.py - author's helper: runs every sql/mysql block in a chapter draft exactly as verify_sql.py does
(db markers, stateful lab regions, run/out markers) and replaces output blocks that contain only FILL with the
real output. Output is copied verbatim from psql / mysql -t. Afterwards verify_sql.py must report 0 mismatches."""
import re, subprocess, sys
subprocess.run(["bash", "/home/claude/book/checks/up.sh"])
sys.path.insert(0, '/home/claude/book/tools')
from verify_sql import run_pg, run_my, DML

path = sys.argv[1]
md = open(path, encoding='utf-8').read()
token = re.compile(r'<!-- (db|run|out): ([\w]+) -->|<!-- lab:(start|end) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
db = 'riverstone'; in_lab = False; pending_run = None; pending_out = None; last = {}; labs_seen = False
pieces, pos, filled = [], 0, 0
def clean(s):
    lines = [l.rstrip() for l in s.strip('\n').splitlines()]
    return '\n'.join(l for l in lines if not l.startswith(('psql:', 'NOTICE:')))
for m in token.finditer(md):
    if m.group(1) == 'db': db = m.group(2); continue
    if m.group(1) == 'run': pending_run = m.group(2); continue
    if m.group(1) == 'out': pending_out = m.group(2); continue
    if m.group(3) == 'start':
        in_lab = True; last = {}
        if not labs_seen:
            labs_seen = True
            run_pg('DROP DATABASE IF EXISTS riverstone_lab;', 'postgres')
            subprocess.run(['mysql', '-uroot', '-e', 'DROP DATABASE IF EXISTS riverstone_lab;'])
        continue
    if m.group(3) == 'end': in_lab = False; last = {}; continue
    lang, body = m.group(4), m.group(5)
    if lang in ('sql', 'mysql'):
        engine = pending_run or ('mysql' if lang == 'mysql' else 'pg'); pending_run = None; last = {}
        if engine == 'none': continue
        if not in_lab and DML.search(body): continue
        use_db = 'riverstone_lab' if in_lab else db
        if engine in ('pg', 'both'): last['pg'] = run_pg(body, use_db)
        if engine in ('mysql', 'both'): last['mysql'] = run_my(body, use_db)
        last['_next'] = 'mysql' if engine == 'mysql' else 'pg'
        for k in ('pg', 'mysql'):
            if k in last and 'ERROR' in last[k] and 'FILL' not in md[m.end():m.end()+30]:
                print('ERROR in block at line', md[:m.start()].count('\n') + 1, last[k][:200])
        continue
    if lang == '' and last:
        target = pending_out or last.get('_next'); pending_out = None
        if body.strip() == 'FILL' and target in last:
            pieces.append(md[pos:m.start()]); pieces.append('```\n' + clean(last[target]) + '\n```'); pos = m.end(); filled += 1
        last['_next'] = None
        continue
    pending_out = None
pieces.append(md[pos:])
open(path, 'w', encoding='utf-8').write(''.join(pieces))
print('filled', filled)
