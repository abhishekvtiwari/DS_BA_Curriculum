#!/usr/bin/env python3
"""ch33_timed_cells.py - runs every Python cell of Chapter 33 in order, INCLUDING the timed cells marked
<!-- run: none --> (their output depends on the machine, so verify_python.py skips them), and prints what
each timed cell printed. The chapter's timed outputs are pasted from this run.
How: cd companion/ch33 && python ../../checks/ch33_timed_cells.py ../../manuscript/ch33-*.md
Fragments containing a line that is just '...' are skipped."""
import contextlib, io, re, sys
md = open(sys.argv[1], encoding='utf-8').read()
token = re.compile(r'<!-- (py): reset -->|<!-- run: (none) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
ns = {'__name__': '__main__'}; timed = False
for m in token.finditer(md):
    if m.group(1): ns = {'__name__': '__main__'}; continue
    if m.group(2): timed = True; continue
    lang, body = m.group(3), m.group(4)
    if lang != 'python':
        timed = False; continue
    if re.search(r'^\s*\.\.\.\s*$', body, re.M):
        timed = False; continue
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(body, 'cell', 'exec'), ns)
    if timed:
        line = md[:m.start()].count('\n') + 1
        print(f'--- timed cell at line {line}:'); print(buf.getvalue(), end='')
    timed = False
