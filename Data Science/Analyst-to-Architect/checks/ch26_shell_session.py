#!/usr/bin/env python3
"""
ch26_shell_session.py - Chapter 26's version of tools/verify_shell.py.

Why a variant: Git prints blank lines inside its output (git status, git log), and verify_shell.py stops
reading a command's expected output at the first blank line. Here a command's expected output is
everything up to the next "$ " line, blank lines included (they are ignored when comparing).

Usage (normally through checks/ch26_run.sh, which builds the scratch environment):
    python3 ch26_shell_session.py path/to/ch26.md --cwd DIR [--fill]
Conventions, as in verify_shell.py:
  a fenced block whose first line starts with "# terminal" is a terminal session; "$ " lines are commands,
  run in ONE bash session in order; <!-- run: none --> skips the next fenced block; FILL as a command's
  whole output is replaced by the real output with --fill. A session block written inside an HTML
  comment is run but not printed: the book uses these for edits the reader makes in the editor.
Exit code: 0 if every shown output matches, 1 otherwise.
"""
import argparse, os, re, subprocess, sys, uuid

ap = argparse.ArgumentParser(); ap.add_argument('path'); ap.add_argument('--cwd', default='.')
ap.add_argument('--fill', action='store_true')
a = ap.parse_args()
md_path = os.path.abspath(a.path)
md = open(md_path, encoding='utf-8').read()

env = dict(os.environ, LC_ALL='C', LANG='C', TERM='dumb', COLUMNS='100')
shell = subprocess.Popen(['bash', '--norc', '--noprofile'], cwd=os.path.abspath(a.cwd), env=env,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
MARK = f'__done_{uuid.uuid4().hex}__'


def run(command):
    plain = command.startswith(('cd ', 'export ', 'unset ')) or command.rstrip().endswith('&')
    wrapped = command if plain else '{ ' + command + ' ; } < /dev/null'
    shell.stdin.write(wrapped + f'\necho {MARK}\n'); shell.stdin.flush()
    lines = []
    for line in shell.stdout:
        if line.rstrip('\n') == MARK:
            break
        lines.append(line.rstrip('\n'))
    return lines


def norm(lines):
    return [l.rstrip() for l in lines if l.strip()]


block = re.compile(r'<!-- run: (none) -->|^```\w*\n(# terminal.*?)^```$|^```\w*\n(?!# terminal).*?^```$', re.S | re.M)
pieces, pos = [], 0
ran = checked = mismatches = filled = 0
skip = False
for m in block.finditer(md):
    if m.group(1):
        skip = True
        continue
    if skip:
        skip = False
        continue
    body = m.group(2)
    if body is None:
        continue
    lines = body.rstrip('\n').split('\n')
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith('$ '):
            out.append(line); i += 1; continue
        command = line[2:]
        expected, i = [], i + 1
        while i < len(lines) and not lines[i].startswith('$ '):
            expected.append(lines[i]); i += 1
        while expected and expected[-1] == '':
            expected.pop()
        actual = run(command); ran += 1
        out.append(line)
        if a.fill and '\n'.join(expected).strip() == 'FILL':
            while actual and not actual[-1].strip():
                actual.pop()
            out.extend(actual); filled += 1
        else:
            out.extend(expected); checked += 1
            if norm(expected) != norm(actual):
                mismatches += 1
                print(f'MISMATCH at line {md[:m.start()].count(chr(10)) + 1}: $ {command}')
                print('  expected:', norm(expected)[:6]); print('  got     :', norm(actual)[:6])
        if i < len(lines):
            out.append('')
    pieces.append(md[pos:m.start()]); pieces.append('```\n' + '\n'.join(out) + '\n```'); pos = m.end()
pieces.append(md[pos:])
shell.stdin.close()
try:
    shell.wait(timeout=10)
except subprocess.TimeoutExpired:
    shell.kill()
if a.fill:
    open(md_path, 'w', encoding='utf-8').write(''.join(pieces))
    print(f'{a.path}: commands run {ran}, outputs filled {filled}, checked {checked}, mismatches {mismatches}')
else:
    print(f'{a.path}: commands run {ran}, outputs checked {checked}, mismatches {mismatches}')
sys.exit(1 if mismatches else 0)
