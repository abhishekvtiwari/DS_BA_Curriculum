#!/usr/bin/env python3
"""py_fill.py - author's helper: runs python blocks exactly like tools/verify_python.py and replaces output
blocks containing only FILL with the real printed output. verify_python.py must then report 0 mismatches."""
import re, sys, io, os, contextlib, subprocess, traceback
subprocess.run(["bash", "/home/claude/book/checks/up.sh"])
path, cwd = sys.argv[1], sys.argv[2]
md = open(path, encoding='utf-8').read(); path = os.path.abspath(path); os.chdir(cwd)
token = re.compile(r'<!-- (py): reset -->|<!-- run: (none) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
ns = {'__name__': '__main__'}; skip = False; last = None; out = []; pos = 0; n = 0
for m in token.finditer(md):
    line = md[:m.start()].count('\n') + 1
    if m.group(1): ns = {'__name__': '__main__'}; continue
    if m.group(2): skip = True; continue
    lang, body = m.group(3), m.group(4)
    if lang == 'python':
        if skip: skip = False; last = None; continue
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try: exec(compile(body, f'<block at line {line}>', 'exec'), ns)
            except Exception: print(traceback.format_exc().strip().splitlines()[-1])
        last = buf.getvalue(); continue
    if lang != 'python' and skip:
        skip = False        # the marker applied to a non-python block (a terminal session), so it is spent
    if lang == '' and last is not None:
        if body.strip() == 'FILL':
            out.append(md[pos:m.start()]); out.append('```\n' + '\n'.join(l.rstrip() for l in last.strip('\n').splitlines()) + '\n```'); pos = m.end(); n += 1
        last = None; continue
    if lang: last = None
out.append(md[pos:]); open(path, 'w', encoding='utf-8').write(''.join(out)); print('filled', n)
