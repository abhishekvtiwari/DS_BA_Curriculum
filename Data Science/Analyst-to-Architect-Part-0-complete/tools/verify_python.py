#!/usr/bin/env python3
"""
verify_python.py - check that every Python output printed in a chapter matches a real run.

Usage:  python3 verify_python.py path/to/chapter.md [--cwd companion/chNN]

Conventions (see planning/chapter-writing-instructions.md, section 9):
  ```python block  -> executed in order, in ONE shared namespace (like a notebook), with --cwd as the
                      working directory; the next plain ``` block is its expected printed output
                      (stdout, plus the last line of the traceback if the block raises).
  <!-- py: reset -->   -> start a fresh namespace for later blocks
  <!-- run: none -->   -> skip the next code block (e.g. a fragment, or code that needs the internet)
Comparison ignores trailing spaces and blank lines. Exit code: 0 if all outputs match, 1 otherwise.
Record the Python and library versions used in the chapter's "Tools" section.
"""
import re, sys, io, os, argparse, contextlib, traceback

def norm(s):
    return [l.rstrip() for l in s.strip('\n').splitlines() if l.strip()]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--cwd', default='.')
    a = ap.parse_args()
    md = open(a.path, encoding='utf-8').read()
    os.chdir(a.cwd)
    token = re.compile(r'<!-- (py): reset -->|<!-- run: (none) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
    ns = {'__name__': '__main__'}; skip = False; last = None; checked = bad = ran = 0
    for m in token.finditer(md):
        line = md[:m.start()].count('\n') + 1
        if m.group(1): ns = {'__name__': '__main__'}; continue
        if m.group(2): skip = True; continue
        lang, body = m.group(3), m.group(4)
        if lang == 'python':
            if skip: skip = False; last = None; continue
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                try:
                    exec(compile(body, f'<block at line {line}>', 'exec'), ns)
                except Exception:
                    print(traceback.format_exc().strip().splitlines()[-1])
            last = buf.getvalue(); ran += 1
            continue
        if skip:
            skip = False        # the marker applied to a non-python block, so it is spent here
        if lang == '' and last is not None:
            checked += 1
            if norm(body) != norm(last):
                bad += 1
                print(f'MISMATCH at line {line}'); print('  expected:', norm(body)[:6]); print('  got     :', norm(last)[:6])
            last = None
            continue
        if lang: last = None
    print(f'{a.path}: blocks run {ran}, outputs checked {checked}, mismatches {bad}')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
