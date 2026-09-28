#!/usr/bin/env python3
"""Checks for the Chapter 18 blocks that tools/verify_python.py skips (<!-- run: none -->).

Run from the book folder, with RIVERSTONE_DB set (PostgreSQL) and MySQL reachable as root through its socket:
    python3 checks/ch18_extra_check.py [--fill]

1. The MySQL cell of section 18.13: runs the chapter's code with an engine on MySQL's riverstone_full and
   compares the printed output with the output block under it.
2. The terminal run of monthly_report.py in section 18.15: runs the command in companion/ch18 and compares the
   output, ignoring the HH:MM:SS at the start of each log line.
3. The six function cells of section 18.15: each must appear, character for character, in
   companion/ch18/monthly_report.py, so the finished file is exactly what the chapter taught.
4. The two timing cells of section 18.1: runs them and checks the printed lines have the shape shown
   (timings differ on every run, so only the non-timing text is compared).
--fill replaces the output blocks of 1, 2 and 4 with the real run (author's helper).
Exit code 0 if everything matches.
"""
import contextlib, io, os, re, subprocess, sys
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
CH = next((BOOK / "manuscript").glob("ch18-*.md"))
CWD = BOOK / "companion" / "ch18"
MYSQL_URL = "mysql+mysqlconnector://root@localhost/riverstone_full?unix_socket=/var/run/mysqld/mysqld.sock"
fill = "--fill" in sys.argv
md = CH.read_text(encoding="utf-8")
bad = 0

BLOCK = re.compile(r"^```(\w*)\n(.*?)^```$", re.S | re.M)


def block_after(pos, lang=None):
    m = BLOCK.search(md, pos)
    while m and lang is not None and m.group(1) != lang:
        m = BLOCK.search(md, m.end())
    return m


def compare(label, expected_match, got, norm=lambda s: s):
    global md, bad
    exp = [norm(l.rstrip()) for l in expected_match.group(2).strip("\n").splitlines() if l.strip()]
    act = [norm(l.rstrip()) for l in got.strip("\n").splitlines() if l.strip()]
    if exp == act:
        print(f"OK   {label}")
        return
    if fill:
        md = md[:expected_match.start(2)] + got.rstrip("\n") + "\n" + md[expected_match.end(2):]
        print(f"FILL {label}")
        return
    bad += 1
    print(f"MISMATCH {label}\n  expected: {exp[:6]}\n  got     : {act[:6]}")


os.chdir(CWD)
sys.path.insert(0, str(CWD))

# 1. MySQL cell
code_m = BLOCK.search(md, md.rfind("```python", 0, md.index("query_mysql = text(")))
out_m = block_after(code_m.end(), "")
import pandas as pd
from sqlalchemy import create_engine, text
pd.set_option("display.float_format", "{:,.2f}".format)
pd.set_option("display.width", 100)
pd.set_option("display.max_columns", 12)
ns = {"pd": pd, "text": text, "engine": create_engine(MYSQL_URL)}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(code_m.group(2), ns)
compare("MySQL cell, section 18.13", out_m, buf.getvalue())

# 2. terminal run of the script
term = BLOCK.search(md, md.index("$ python monthly_report.py 2025-12 --out reports") - 40)
body = term.group(2)
cmd_line = [l for l in body.splitlines() if l.startswith("$ ")][0][2:]
run = subprocess.run(cmd_line.replace("python ", sys.executable + " ", 1), shell=True, capture_output=True, text=True)
got = run.stderr + run.stdout
expected_out = "\n".join(l for l in body.splitlines()[1:] if not l.startswith("$ "))
stamp = lambda l: re.sub(r"^\d\d:\d\d:\d\d ", "HH:MM:SS ", l)
exp = [stamp(l) for l in expected_out.splitlines() if l.strip()]
act = [stamp(l) for l in got.splitlines() if l.strip()]
if exp == act:
    print("OK   terminal run, section 18.15")
elif fill:
    new_body = body.splitlines()[0] + "\n" + "$ " + cmd_line + "\n" + got.rstrip("\n") + "\n"
    md = md[:term.start(2)] + new_body + md[term.end(2):]
    print("FILL terminal run, section 18.15")
else:
    bad += 1
    print(f"MISMATCH terminal run\n  expected: {exp[:4]}\n  got     : {act[:4]}")

# 3. function cells are in the finished script
script = (CWD / "monthly_report.py").read_text(encoding="utf-8")
sec = md[md.index("## 18.15"):md.index("## 18.16")]
cells = [m.group(2) for m in BLOCK.finditer(sec) if m.group(1) == "python"]
pieces = 0
for cell in cells:
    for piece in re.split(r"\n\n\n", cell):
        piece = piece.strip("\n")
        if piece.startswith(("def ", "QUERY", "log = ")):
            pieces += 1
            if piece not in script:
                bad += 1
                print("NOT IN monthly_report.py:", piece.splitlines()[0])
print(f"OK   {pieces} pieces of section 18.15 checked against monthly_report.py" if not bad else "")

# 4. timing cells
import time
t0 = md.index("import time\n\nstart = time.perf_counter()")
c1 = BLOCK.search(md, md.rfind("```python", 0, t0)); o1 = block_after(c1.end(), "")
c2 = BLOCK.search(md, o1.end()); o2 = block_after(c2.end(), "")
COMPANION = Path("../../companion")
lines = pd.read_parquet(COMPANION / "full" / "order_items.parquet").merge(pd.read_parquet(COMPANION / "full" / "orders.parquet"), on="order_id")
ns = {"pd": pd, "lines": lines}
got = ""
for c, o, label in [(c1, o1, "timing cell 1"), (c2, o2, "timing cell 2")]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(c.group(2), ns)
    shape = lambda l: re.sub(r"[\d.,]+ (ms|times)", r"N \1", l)
    compare(f"{label}, section 18.1 (numbers masked)", o, buf.getvalue(), norm=shape)

if fill:
    CH.write_text(md, encoding="utf-8")
print("mismatches:", bad)
sys.exit(1 if bad else 0)
