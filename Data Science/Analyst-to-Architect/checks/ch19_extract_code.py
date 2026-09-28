#!/usr/bin/env python3
"""ch19_extract_code.py - rebuilds companion/ch19/vba, office_scripts and apps_script from the chapter's
code blocks, so the companion files always match the book.  Run from the book folder:
    python3 checks/ch19_extract_code.py
Blocks that are not whole procedures (the recorded-vs-written fragment, a one-line Immediate window
call) are left out of the .bas file."""
import re, pathlib
BOOK = pathlib.Path(__file__).resolve().parent.parent
md = (BOOK / 'manuscript/ch19-spreadsheet-automation.md').read_text(encoding='utf-8')
comp = BOOK / 'companion/ch19'

def blocks(lang):
    return re.findall(r'^```' + lang + r'\n(.*?)^```$', md, re.S | re.M)

vba = [b for b in blocks('vb') if re.search(r'^(Public |Private )?(Sub|Function) |^Private Const', b, re.M)]
head = ("' Analyst to Architect, Chapter 19 - VBA procedures from the chapter, in the order they appear.\n"
        "' Import with File > Import File in the VBA editor (Alt+F11), or paste into a module.\n"
        "' Keep one Option Explicit and one set of Const lines per module if you paste several.\n"
        "' Riverstone Supplies is fictional; every name and number is invented.\n\n")
# one module: Option Explicit once, each Const once, at the top (VBA refuses duplicates)
consts, procs = [], []
for b in vba:
    for line in b.splitlines():
        if line.startswith('Private Const') and line not in consts:
            consts.append(line)
    body = '\n'.join(l for l in b.splitlines()
                     if not l.startswith('Private Const') and not l.startswith('Option Explicit')).strip('\n')
    if body:
        procs.append(body)
(comp / 'vba/ch19_modules.bas').write_text(
    head + 'Option Explicit\n\n' + '\n'.join(consts) + '\n\n' + '\n\n'.join(procs) + '\n', encoding='utf-8')

ts = blocks('ts')
head = ("// Analyst to Architect, Chapter 19 - Office Scripts (Excel on the web).\n"
        "// Each script is a separate main(): paste one at a time into Automate > New Script.\n\n")
(comp / 'office_scripts/ch19_office_scripts.ts').write_text(
    head + '\n// ---- next script ----\n\n'.join(ts), encoding='utf-8')

js = blocks('javascript')
head = ("// Analyst to Architect, Chapter 19 - Google Apps Script for Sheets.\n"
        "// Paste into Extensions > Apps Script. Set CRM_TOKEN in Project Settings > Script Properties,\n"
        "// and the project's time zone to India (Asia/Kolkata) before adding timed triggers.\n\n")
(comp / 'apps_script/ch19_apps_script.gs').write_text(head + '\n'.join(js), encoding='utf-8')
print(f'{len(vba)} VBA blocks, {len(ts)} Office Scripts, {len(js)} Apps Script blocks written')
