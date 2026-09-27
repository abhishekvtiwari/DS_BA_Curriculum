#!/usr/bin/env python3
"""ch28_build.py - runs, in order, every sql block marked <!-- build: NAME --> in the chapter against
riverstone_2025 (PostgreSQL), so the star schema the chapter's SELECTs read is built from the exact code printed.
Usage: python3 ch28_build.py chapter.md [NAME]"""
import re, subprocess, sys
md = open(sys.argv[1]).read(); name = sys.argv[2] if len(sys.argv) > 2 else 'dw'
blocks = re.findall(r'<!-- build: ' + name + r' -->\n```sql\n(.*?)^```$', md, re.S | re.M)
sql = '\\set ON_ERROR_STOP 1\n' + '\n'.join(blocks)
r = subprocess.run(['su', 'postgres', '-c', 'psql -X -q -d riverstone_2025'], input=sql, capture_output=True, text=True, cwd='/tmp')
print(r.stderr.strip() or f'built {len(blocks)} blocks'); sys.exit(1 if 'ERROR' in r.stderr else 0)
