# Analyst to Architect - Chapter 47: re-run the optional Great Expectations and Soda cells (section 47.10).
# They are marked "run: none" so the plain verifier can run without those libraries. This script removes
# that marker from the Python blocks that import great_expectations or soda_core, then runs the whole
# chapter with tools/verify_python.py in the CURRENT interpreter, which must have duckdb, psycopg2,
# great_expectations==1.23.2 and soda-duckdb==4.25.0 installed.
# Run from the book root, PostgreSQL running:
#   SODA_CORE_TELEMETRY_ENABLED=false <venv>/bin/python checks/ch47_tools_check.py
# Riverstone Supplies is fictional; every name and number is invented.
import glob, os, re, subprocess, sys, tempfile
chapter = glob.glob('manuscript/ch47-*.md')[0]
text = open(chapter, encoding='utf-8').read()
pattern = r'<!-- run: none -->\n+(```python\n(?:(?!```).)*?(?:great_expectations|soda_core))'
unskipped, n = re.subn(pattern, r'\1', text, flags=re.S)
print(f'{n} optional tool blocks will run')
with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as f:
    f.write(unskipped)
rc = subprocess.call([sys.executable, 'tools/verify_python.py', f.name, '--cwd', 'companion/ch47'])
os.remove(f.name)
sys.exit(rc if n == 2 else 1)
