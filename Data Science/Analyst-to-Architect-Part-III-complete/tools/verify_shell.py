#!/usr/bin/env python3
"""
verify_shell.py - check that every terminal session printed in a chapter matches a real run.

Usage:  python3 verify_shell.py path/to/chapter.md [--cwd companion/ch34] [--fill]

Conventions (proposed as a companion to tools/verify_sql.py and tools/verify_python.py):
  A fenced block whose first line starts with "# terminal" is a terminal session. Inside it,
  lines starting with "$ " are commands; everything until the next "$ " line is that command's
  expected output (stdout and stderr together). Commands run in ONE bash session per chapter, so
  cd, variables and created files carry from block to block, with LC_ALL=C for stable sorting.
  --user NAME runs the session as that user (so permission demonstrations behave normally)
  <!-- run: none -->   before a block skips it (commands that need a real server, are slow, or destroy things)
  FILL as the whole output of a command  ->  with --fill, replaced by the real output (author's helper)
Exit code: 0 if every shown output matches, 1 otherwise.
"""
import argparse, os, re, subprocess, sys, uuid

ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--cwd', default='.')
ap.add_argument('--fill', action='store_true'); ap.add_argument('--user', default=None)
a = ap.parse_args()
md_path = os.path.abspath(a.path)
md = open(md_path, encoding='utf-8').read()

env = dict(os.environ, LC_ALL='C', LANG='C', TERM='dumb', COLUMNS='100')
cmd = ['su', a.user, '-c', 'bash --norc --noprofile'] if a.user else ['bash', '--norc', '--noprofile']
shell = subprocess.Popen(cmd, cwd=os.path.abspath(a.cwd), env=env,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
MARK = f'__done_{uuid.uuid4().hex}__'

def run(command):
    # Commands read from /dev/null, so an interactive program (ssh, less) can't swallow the rest of the session.
    plain = command.startswith(('cd ', 'export ', 'unset ')) or command.rstrip().endswith('&')
    wrapped = command if plain else '{ ' + command + ' ; } < /dev/null'
    shell.stdin.write(wrapped + f'\necho {MARK}\n'); shell.stdin.flush()
    lines = []
    for line in shell.stdout:
        if line.rstrip('\n') == MARK:
            break
        lines.append(line.rstrip('\n'))
    return '\n'.join(lines)

def norm(text):
    return [l.rstrip() for l in text.strip('\n').splitlines() if l.strip()]

block = re.compile(r'<!-- run: (none) -->|^```\w*\n(# terminal.*?)^```$', re.S | re.M)
pieces, pos, checked = [], 0, 0
mismatches = ran = filled = 0
skip = False
for m in block.finditer(md):
    if m.group(1):
        skip = True
        continue
    if skip:
        skip = False
        continue
    body = m.group(2)
    lines = body.split('\n')
    out_lines, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith('$ '):
            out_lines.append(line); i += 1; continue
        command = line[2:]
        expected, i = [], i + 1
        while i < len(lines) and not lines[i].startswith('$ ') and lines[i] != '':
            expected.append(lines[i]); i += 1
        actual = run(command); ran += 1
        shown = '\n'.join(expected)
        if a.fill and shown.strip() == 'FILL':
            out_lines.append(line)
            out_lines.extend(actual.splitlines() if actual.strip() else [])
            filled += 1
        else:
            out_lines.append(line); out_lines.extend(expected)
            checked += 1
            if norm(shown) != norm(actual):
                mismatches += 1
                print(f'MISMATCH at line {md[:m.start()].count(chr(10)) + 1}: $ {command}')
                print('  expected:', norm(shown)[:4]); print('  got     :', norm(actual)[:4])
        if i < len(lines) and lines[i] == '':
            out_lines.append(''); i += 1
    new_body = '\n'.join(out_lines)
    pieces.append(md[pos:m.start()]); pieces.append('```\n' + new_body + '```'); pos = m.end()
pieces.append(md[pos:])
shell.stdin.close()
try:
    shell.wait(timeout=10)
except subprocess.TimeoutExpired:      # a background job the chapter started is still running
    shell.kill()
if a.fill:
    open(md_path, 'w', encoding='utf-8').write(''.join(pieces))
    print(f'{a.path}: commands run {ran}, outputs filled {filled}, checked {checked}, mismatches {mismatches}')
else:
    print(f'{a.path}: commands run {ran}, outputs checked {checked}, mismatches {mismatches}')
sys.exit(1 if mismatches else 0)
