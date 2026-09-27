#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 28 · Advanced SQL, Performance & Data Modeling
File: migrate.py - a tiny versioned-migration runner, to show how tools like Flyway work (section 28.12).
How:  python3 migrate.py --db DATABASE MIGRATIONS_FOLDER      (add --user NAME if needed)
      Files named V<number>__<description>.sql are applied once each, in number order, each inside a
      transaction together with its row in schema_migrations. An applied file whose contents change is
      reported and nothing further runs. Uses the psql command-line client, so it needs no Python packages.
Tested on: Python 3.12.3, PostgreSQL 16 (Ubuntu 24.04). For learning only: use a real tool in production.
Riverstone Supplies is fictional; every name and number is invented.
"""
import argparse, hashlib, pathlib, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument('folder'); ap.add_argument('--db', required=True); ap.add_argument('--user', default=None)
a = ap.parse_args()
PSQL = ['psql', '-X', '-q', '-At', '-v', 'ON_ERROR_STOP=1', '-d', a.db] + (['-U', a.user] if a.user else [])

def psql(sql):
    r = subprocess.run(PSQL, input=sql, capture_output=True, text=True)
    if r.returncode:
        sys.exit('migration failed:\n' + r.stderr.strip())
    return r.stdout.strip()

psql("""CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY, description VARCHAR(100) NOT NULL,
    checksum CHAR(32) NOT NULL, applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);""")
applied = {int(v): c for v, c in (line.split('|') for line in psql(
    'SELECT version, checksum FROM schema_migrations;').splitlines() if line)}

files = []
for f in pathlib.Path(a.folder).glob('V*__*.sql'):
    m = re.fullmatch(r'V(\d+)__(.+)\.sql', f.name)
    if m: files.append((int(m.group(1)), m.group(2).replace('_', ' '), f))
files.sort()

ran = 0
for version, description, f in files:
    body = f.read_text()
    checksum = hashlib.md5(body.encode()).hexdigest()
    if version in applied:
        if applied[version] != checksum:
            sys.exit(f'checksum mismatch: {f.name} was changed after it was applied. Write a new migration instead.')
        continue
    psql('BEGIN;\n' + body + f"\nINSERT INTO schema_migrations (version, description, checksum) "
         f"VALUES ({version}, '{description}', '{checksum}');\nCOMMIT;\n")
    print(f'applied  {f.name}'); ran += 1

current = psql('SELECT COALESCE(MAX(version), 0) FROM schema_migrations;')
print(f'database is at version {current}' if ran else f'nothing to apply; database is at version {current}')
