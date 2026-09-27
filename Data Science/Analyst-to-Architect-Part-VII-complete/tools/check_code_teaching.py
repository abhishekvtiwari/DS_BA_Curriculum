#!/usr/bin/env python3
"""check_code_teaching.py - flags code that isn't taught line by line (instructions section 6.5).

Usage: python3 tools/check_code_teaching.py manuscript/ch18-....md [more files]

For every code block (sql, mysql, python, vba, javascript, dax, powerquery, excel, bash, and
unlabeled terminal sessions, recognized by their `$ ` prompt lines) it checks:
  1. a plan in words before the block (prose within the 8 lines above, not another code block);
  2. an explanation after it: "How it works", "What each line does", or a bullet list naming
     things from the code, within the 40 lines below (a long "Line by line" list counts);
  3. block length (long first-time blocks are hard to teach line by line);
  4. how much of the code is actually named in the explanation (identifiers and arguments);
  5. keyword arguments (settings passed into a call) that are never mentioned anywhere in the chapter;
  6. at least one "what if you change it" demonstration and one predict-before-running prompt
     per chapter with code.
It reports, it doesn't rewrite. Exit code 1 if anything is flagged.

A flag is a question, not a verdict: a later block that reuses an idea taught earlier in the same
chapter can be left as it is, but the first appearance of anything must be explained in full.
Record any deliberate exceptions in your chapter report."""
import re, sys, collections

LANGS = {'sql','mysql','python','py','vba','javascript','dax','powerquery','excel','bash','shell','r','terminal'}
PROMPT = re.compile(r'^\s*\$ ')
EXPLAIN = re.compile(r'how it works|what each line|line by line|reading it|what this does|step by step|breaking it down|what the code does', re.I)
WHATIF = re.compile(r'what happens if you change|if you change it|change it to|what if you change|try changing', re.I)
PREDICT = re.compile(r'before you run|predict|write down what you expect', re.I)
IDENT = re.compile(r'[A-Za-z_][A-Za-z_0-9]{2,}')
KEYWORDS = {'the','and','for','with','from','this','that','not','into','select','where','group','order','table','true','false','none','null'}

def blocks(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        m = re.match(r'^```(\w+)?\s*$', lines[i])
        if m:
            lang = (m.group(1) or '').lower(); start = i; i += 1
            body = []
            while i < len(lines) and not re.match(r'^```\s*$', lines[i]):
                body.append(lines[i]); i += 1
            if not lang and any(PROMPT.match(b) for b in body):
                lang = 'terminal'
            out.append((lang, start, i, body))
        i += 1
    return out, lines

def check(path):
    md = open(path, encoding='utf-8').read()
    bl, lines = blocks(md)
    issues = []
    code_blocks = [b for b in bl if b[0] in LANGS]
    prose_only = re.sub(r'^```.*?^```', '', md, flags=re.S | re.M)
    flagged_blocks = set()
    for lang, start, end, body in code_blocks:
        # in a terminal session only the typed commands are code; the rest is output
        code = [l for l in body if PROMPT.match(l)] if lang == 'terminal' else body
        n = len([l for l in code if l.strip() and not l.strip().startswith(('--', '#', "'"))])
        before = "\n".join(lines[max(0, start-8):start])
        # skip the output block that usually follows the code, then read the explanation
        j = end + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and re.match(r'^```\s*$', lines[j]):
            j += 1
            while j < len(lines) and not re.match(r'^```\s*$', lines[j]):
                j += 1
            j += 1
        after = "\n".join(lines[j:j+40])
        where = f"{path}:{start+1} ({lang}, {n} code lines)"
        if n == 0:
            continue
        if not re.search(r'[A-Za-z]{3,}', re.sub(r'^```.*$', '', before, flags=re.M)):
            issues.append(f"{where}: no plan in words before the block"); flagged_blocks.add(start)
        prose_after = re.sub(r'^```.*$', '', after, flags=re.M)
        has_prose = bool(re.search(r'[A-Za-z]{3,}', prose_after))
        names = {w.lower() for w in IDENT.findall("\n".join(code))} - KEYWORDS
        explained = {w.lower() for w in IDENT.findall(prose_after)}
        coverage = len(names & explained) / len(names) if names else 1.0
        need = 0.5 if n > 6 else 0.25
        if not has_prose:
            issues.append(f"{where}: nothing explains this block (no prose after it)"); flagged_blocks.add(start)
        elif coverage < need and not EXPLAIN.search(prose_after):
            missing = sorted(names - explained)
            issues.append(f"{where}: explanation covers {coverage:.0%} of the code's parts; unexplained: {', '.join(missing[:8])}"); flagged_blocks.add(start)
        if n > 25:
            issues.append(f"{where}: {n} lines is long to teach line by line; split it into steps"); flagged_blocks.add(start)
        if lang in {'python', 'py', 'dax', 'vba', 'javascript', 'r'}:
            # only keyword arguments inside a call, not ordinary variable assignments:
            # f(x, name=value) counts; name = value on its own line does not
            args = {a.lower() for a in re.findall(r'[(,]\s*([A-Za-z_][A-Za-z_0-9]*)=(?!=)', "\n".join(code))} - KEYWORDS
            prose_words = {w.lower() for w in IDENT.findall(prose_only)}
            never = sorted(a for a in args if a not in prose_words)
            if never:
                issues.append(f"{where}: settings never explained in the chapter's prose: {', '.join(never[:8])}"); flagged_blocks.add(start)
    if code_blocks:
        if not WHATIF.search(md):
            issues.append(f"{path}: no settings table column \"what happens if you change it\", and no what-if wording, in the chapter")
        if not PREDICT.search(md):
            issues.append(f"{path}: no 'predict before you run' prompt in the chapter")
    print(f"{path}: {len(code_blocks)} code blocks, {len(flagged_blocks)} flagged, {len(issues)} findings")
    for i in issues:
        print("  -", i)
    return len(issues)

if __name__ == '__main__':
    total = sum(check(p) for p in sys.argv[1:])
    sys.exit(1 if total else 0)
