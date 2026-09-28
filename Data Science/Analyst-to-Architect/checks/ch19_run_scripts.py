#!/usr/bin/env python3
"""ch19_run_scripts.py - runs chapter 19's Office Scripts (TypeScript) and Apps Script (JavaScript) blocks,
extracted from the manuscript, in Node with small mocks of the Excel and Google services they call.
Needs node and tsc on the PATH. Run from the book folder:  python3 checks/ch19_run_scripts.py
Data: the twelve companion branch files consolidated in Dir order (the Master sheet of section 19.6),
and companion/ch19/enquiries_sample.csv submitted through onFormSubmit at each row's own time (IST)."""
import json, os, re, subprocess, tempfile, pathlib
import pandas as pd
BOOK = pathlib.Path(__file__).resolve().parent.parent
tmp = pathlib.Path(tempfile.mkdtemp(prefix='ch19_js_'))
src = BOOK / 'companion/ch19/branch_files'
files = sorted([f for f in os.listdir(src) if f.lower().endswith('.xlsx')], key=str.upper)  # Windows Dir order
grid = None
for f in files:
    d = pd.read_excel(src / f, dtype={'customer_code': str})
    d['order_date'] = d['order_date'].dt.strftime('%Y-%m-%d')
    d = d.astype(object).where(d.notna(), '')
    if grid is None:
        grid = [list(d.columns) + ['source_file']]
    grid += [[x.item() if hasattr(x, 'item') else x for x in r] + [f] for r in d.itertuples(index=False)]
(tmp / 'master.json').write_text(json.dumps(grid))
env = dict(os.environ, BOOK=str(BOOK), MASTER_JSON=str(tmp / 'master.json'), TZ='Asia/Kolkata')
md = (BOOK / 'manuscript/ch19-spreadsheet-automation.md').read_text(encoding='utf-8')
(tmp / 'excelscript.d.ts').write_text('declare namespace ExcelScript { type Workbook = any; type Worksheet = any; }\n'
                                      'declare const console: { log(...a: any[]): void };\n')
for i, b in enumerate(re.findall(r'^```ts\n(.*?)^```$', md, re.S | re.M)):
    (tmp / f'os_{i}.ts').write_text(b)
    r = subprocess.run(['tsc', '--strict', '--target', 'es2020', '--lib', 'es2020', 'excelscript.d.ts', f'os_{i}.ts'],
                       cwd=tmp, capture_output=True, text=True)
    print(f'==== Office Script {i}: tsc --strict exit code {r.returncode} {r.stdout.strip()}')
    js = (tmp / f'os_{i}.js').read_text()
    mock = BOOK / 'checks/ch19_excelscript_mock.js'
    (tmp / f'run_{i}.js').write_text(f"const {{workbook}} = require({json.dumps(str(mock))});\n{js}\nmain(workbook);\n")
    out = subprocess.run(['node', f'run_{i}.js'], cwd=tmp, capture_output=True, text=True, env=env)
    print(out.stdout + out.stderr, end='')
out = subprocess.run(['node', str(BOOK / 'checks/ch19_run_apps_script.js')], capture_output=True, text=True, env=env)
print(out.stdout + out.stderr, end='')
