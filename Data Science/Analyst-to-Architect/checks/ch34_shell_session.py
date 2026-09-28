#!/usr/bin/env python3
"""
ch34_shell_session.py - Chapter 34's version of tools/verify_shell.py (normally run through checks/ch34_run.sh).

Two differences from verify_shell.py, both needed by this chapter's typesetting:
  * a command's expected output is everything up to the next "$ " line, blank lines included (blank lines
    are ignored when comparing), so outputs that contain an empty line are checked in full;
  * a command whose line ends with " \\" continues on the next line(s), exactly as bash reads it, so a long
    command can be printed on several lines with an explicit continuation (finding 34.14).
Conventions otherwise as in verify_shell.py: a fenced block whose first line starts with "# terminal" is a
terminal session run in ONE bash session, in order, with LC_ALL=C; <!-- run: none --> skips the next fenced
block; FILL as a command's whole output is replaced by the real output with --fill.

Usage:  python3 ch34_shell_session.py path/to/chapter.md --cwd DIR [--fill]
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
    wrapped = command if plain else '{ ' + command + '\n} < /dev/null'
    # keep the command's exit code for the next command (a reader's `echo $?` on the next line sees it),
    # although the marker's own echo runs in between
    shell.stdin.write(wrapped + f'\n__rc=$?; echo {MARK}; ( exit $__rc )\n'); shell.stdin.flush()
    lines = []
    for line in shell.stdout:
        if line.rstrip('\n') == MARK:
            break
        lines.append(line.rstrip('\n'))
    return lines


def norm(lines):
    # the date and time in an `ls -l` line are when the reader (or this check) ran the command
    return [re.sub(r'\b[A-Z][a-z]{2} [ \d]\d \d\d:\d\d\b', 'MON DD HH:MM', l.rstrip()) for l in lines if l.strip()]


def interactive(lines):
    # bash reading commands from a pipe (as here) names the line in its own error messages
    # ("bash: line 75: ./run_export.sh: Permission denied"); a terminal you type into doesn't
    # ("bash: ./run_export.sh: Permission denied"), and the book shows what the reader sees.
    return [re.sub(r'^bash: line \d+: ', 'bash: ', l) for l in lines]


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
        cmd_lines = [line]
        i += 1
        while cmd_lines[-1].endswith(' \\') and i < len(lines):
            cmd_lines.append(lines[i]); i += 1
        command = '\n'.join([cmd_lines[0][2:]] + cmd_lines[1:])
        expected = []
        while i < len(lines) and not lines[i].startswith('$ '):
            expected.append(lines[i]); i += 1
        while expected and expected[-1] == '':
            expected.pop()
        actual = interactive(run(command)); ran += 1
        out.extend(cmd_lines)
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
