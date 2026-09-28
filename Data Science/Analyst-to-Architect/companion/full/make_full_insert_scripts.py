"""Writes DBeaver-runnable (INSERT-based, no \\copy / LOAD DATA) versions of companion/full's setup scripts.
Usage: python3 make_full_insert_scripts.py companion/full companion/full   (reads terminal/*.sql and the CSVs)"""
import csv, sys, re, pathlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
ORDER = ["employees", "customers", "products", "orders", "order_items", "sales_targets", "leads", "lead_stage_history"]
def lit(v):
    if v == "": return "NULL"
    return "'" + v.replace("'", "''") + "'"
def inserts(t, my):
    rows = list(csv.reader(open(src / f"{t}.csv", newline="", encoding="utf-8")))
    cols, rows = rows[0], rows[1:]
    o = []
    for s in range(0, len(rows), 1000):
        vals = ",\n".join("(" + ",".join(lit(v).replace("\\", "\\\\") if my else lit(v) for v in r) + ")" for r in rows[s:s+1000])
        o.append(f"INSERT INTO {t} ({', '.join(cols)}) VALUES\n{vals};")
    return "\n".join(o)
for eng, name in (("pg", "riverstone_full_setup_postgresql.sql"), ("my", "riverstone_full_setup_mysql.sql")):
    txt = (src / "terminal" / name).read_text(encoding="utf-8")   # the \copy / LOAD DATA versions are the template
    lines = txt.split("\n")
    body = []
    done = False
    for l in lines:
        if l.startswith("\\copy") or l.startswith("LOAD DATA"):
            if not done:
                body += [inserts(t, eng == "my") for t in ORDER]; done = True
            continue
        if l.startswith("-- Run from") or l.startswith("--   "):
            continue
        body.append(l)
    body.insert(2, "-- In DBeaver: open this file and choose Execute SQL Script (Alt+X)." + (" Make riverstone_full the active database first." if eng == "pg" else " It creates the database riverstone_full itself."))
    (out / name).write_text("\n".join(body), encoding="utf-8")
    print(name, (out / name).stat().st_size)
