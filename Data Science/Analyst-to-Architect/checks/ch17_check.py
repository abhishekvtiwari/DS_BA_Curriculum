#!/usr/bin/env python3
"""ch17_check.py - checks the parts of Chapter 17 that tools/verify_python.py and tools/verify_shell.py
can't run: the script built in stages (section 17.12), show_args.py, the exit codes, the REPL session,
the first notebook and the Jupyter traceback, requirements.txt, Figure 17.3's traceback, and the numbers
quoted in the answers.

Run it after `bash checks/ch17_setup_workdir.sh`, with the Python 3.14 environment it builds:
    /home/meera/analyst-to-architect/.venv/bin/python checks/ch17_check.py [--fill]
--fill replaces an output block that is exactly FILL with the real output (author's helper).
Exit code 0 when everything matches.
"""
import os, re, sys, subprocess, tempfile, shutil, pathlib, csv, statistics, collections

BOOK = pathlib.Path(__file__).resolve().parents[1]
CHAPTER = BOOK / "manuscript" / "ch17-python-from-zero.md"
WORK = pathlib.Path("/home/meera/analyst-to-architect/work/ch17")
VENV_PY = pathlib.Path("/home/meera/analyst-to-architect/.venv/bin/python")
FILL = "--fill" in sys.argv
md = CHAPTER.read_text(encoding="utf-8")
problems = []


def blocks_tagged(tag):
    """Bodies of the fenced blocks that follow <!-- check: tag --> (a run: none marker may sit between)."""
    pat = re.compile(r"<!-- check: " + re.escape(tag) + r" -->\n(?:<!-- run: none -->\n)?```\w*\n(.*?)^```$", re.S | re.M)
    return pat.findall(md)


def compare(label, expected, got):
    norm = lambda t: [l.rstrip() for l in t.strip("\n").splitlines() if l.strip()]
    if norm(expected) != norm(got):
        problems.append(label)
        print(f"MISMATCH {label}\n  expected: {norm(expected)[:6]}\n  got     : {norm(got)[:6]}")
    else:
        print(f"ok  {label}")


# ---- 1. the script, stage by stage -------------------------------------------------------------
final = (BOOK / "companion" / "ch17" / "summarize_exports.py").read_text(encoding="utf-8")
head, rest = final.split("\n\n\ndef read_rows", 1)
read_rows = "def read_rows" + rest.split("\n\n\ndef summarize", 1)[0]
summarize = "def summarize" + rest.split("\n\n\ndef summarize", 1)[1].split("\n\n\ndef main", 1)[0]
main_fn = "def main" + rest.split("\n\n\ndef main", 1)[1].split("\n\n\nif __name__", 1)[0]
guard = "if __name__" + rest.split("\n\n\nif __name__", 1)[1]
head_no_sys = head.replace("import sys\n", "")
test1 = 'rows = read_rows(Path("sales_exports/riverstone_2025_01.csv"))\nprint(len(rows))\n'
test2 = 'print(summarize(Path("sales_exports/riverstone_2025_01.csv")))\n'
test3 = 'main("sales_exports")\n'
stages = {
    1: f"{head_no_sys}\n\n\n{read_rows}\n\n\n{test1}",
    2: f"{head_no_sys}\n\n\n{read_rows}\n\n\n{summarize}\n\n\n{test2}",
    3: f"{head_no_sys}\n\n\n{read_rows}\n\n\n{summarize}\n\n\n{main_fn}\n\n\n{test3}",
    4: final,
}
for n, text in stages.items():
    for body in blocks_tagged(f"summarize_exports.py stage {n}"):
        if body.strip("\n") not in text:
            problems.append(f"stage {n} block not in stage file")
            print(f"MISMATCH stage {n}: a chapter block is not part of the stage-{n} file:\n{body[:200]}")
        else:
            print(f"ok  stage {n} block is in the stage-{n} file")
whole = [b for b in blocks_tagged("summarize_exports.py stage 4") if b.startswith('"""')]
if not whole or whole[0].strip("\n") != final.strip("\n"):
    problems.append("whole file differs from companion/ch17/summarize_exports.py")
    print("MISMATCH the whole-file block differs from companion/ch17/summarize_exports.py")

tmp = pathlib.Path(tempfile.mkdtemp(prefix="ch17stages"))
shutil.copytree(WORK / "sales_exports", tmp / "sales_exports")
outputs = {}
for n in (1, 2, 3):
    (tmp / "summarize_exports.py").write_text(stages[n], encoding="utf-8")
    r = subprocess.run([str(VENV_PY), "summarize_exports.py"], cwd=tmp, capture_output=True, text=True)
    outputs[f"summarize_exports.py stage {n} run"] = r.stdout + r.stderr


def terminal_output(body):
    """The output part of a one-command terminal block."""
    lines = body.splitlines()
    cmd_at = [i for i, l in enumerate(lines) if l.startswith("$ ")]
    return "\n".join(lines[cmd_at[0] + 1:]) if cmd_at else ""


def fill_block(tag, real):
    global md
    pat = re.compile(r"(<!-- check: " + re.escape(tag) + r" -->\n(?:<!-- run: none -->\n)?```\w*\n# terminal\n\$ [^\n]*\n)FILL\n", re.M)
    md, k = pat.subn(lambda m: m.group(1) + real.rstrip("\n") + "\n", md)
    return k


for tag, real in outputs.items():
    if FILL and fill_block(tag, real):
        print(f"filled {tag}")
        continue
    for body in blocks_tagged(tag):
        compare(tag, terminal_output(body), real)

# ---- 2. show_args.py, the final runs and their exit codes (run in the reader's folder) -----------
for body in blocks_tagged("show_args.py"):
    compare("show_args.py matches the chapter", body, (WORK / "show_args.py").read_text())


def session(body, fill):
    """Run a multi-command terminal block in bash (in WORK, environment active); compare or fill."""
    parts = re.split(r"^\$ (.*)$", body, flags=re.M)
    cmds = parts[1::2]; shown = parts[2::2]
    script = "source /home/meera/analyst-to-architect/.venv/bin/activate\n"
    marks = []
    for i, c in enumerate(cmds):
        script += f"{c}\necho __MARK{i}__\n"
    r = subprocess.run(["bash", "--norc", "-c", script], cwd=WORK, capture_output=True, text=True)
    outs = re.split(r"__MARK\d+__\n?", r.stdout + r.stderr)
    new = "# terminal\n"
    for i, c in enumerate(cmds):
        got = outs[i].strip("\n")
        if fill and shown[i].strip() == "FILL":
            new += f"$ {c}\n{got}\n\n"
        else:
            compare(f"`{c}`", shown[i], got)
            new += f"$ {c}\n{shown[i].strip(chr(10))}\n\n" if shown[i].strip() else f"$ {c}\n\n"
    return new.rstrip("\n") + "\n"


for tag in ("show_args.py run", "final run 1", "final run 2"):
    for body in blocks_tagged(tag):
        fixed = session(body, FILL)
        if FILL and "FILL" in body:
            md = md.replace(body, fixed, 1)
            print(f"filled {tag}")

# ---- 3. the REPL session (a real interactive Python 3.14, through a pseudo-terminal) ---------------
import pty, select, time
repl = re.search(r"```text\n(>>> print\(\"Hello, Riverstone\"\).*?)^```$", md, re.S | re.M).group(1)
pid, fd = pty.fork()
if pid == 0:
    os.environ.update(TERM="dumb", PYTHON_BASIC_REPL="1")
    os.execv(str(VENV_PY), [str(VENV_PY)])
buf = b""
def read_for(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.1)
        if r:
            try: buf += os.read(fd, 4096)
            except OSError: return
read_for(2)
for line in [l[4:] for l in repl.splitlines() if l.startswith(">>> ")]:
    os.write(fd, (line + "\r").encode()); read_for(1)
got = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", buf.decode(errors="replace")).replace("\r", "")
got = got[got.index(">>> "):]
compare("REPL session", repl, got)

# ---- 4. the first notebook and the Jupyter traceback (a real kernel, via nbclient) ----------------
nb_code = r'''
import nbformat, re, sys
from nbclient import NotebookClient
def run(cells):
    nb = nbformat.v4.new_notebook(); nb.cells = [nbformat.v4.new_code_cell(c) for c in cells]
    NotebookClient(nb, kernel_name="python3", timeout=60, allow_errors=True).execute()
    out = []
    for c in nb.cells:
        t = ""
        for o in c.outputs:
            if o.output_type == "stream": t += o.text
            elif o.output_type == "execute_result": t += o.data["text/plain"] + "\n"
            elif o.output_type == "error": t += re.sub(r"\x1b\[[0-9;]*m", "", "\n".join(o.traceback)) + "\n"
        out.append(t)
    return out
a = run(['print("Hello, Riverstone")', '2 + 2 * 10'])
b = run(['values = [1, 2, 3]\nprint(values[5])'])
print("\x00".join(a + b))
'''
subprocess.run([str(VENV_PY), "-m", "ipykernel", "install", "--sys-prefix", "--name", "python3"], capture_output=True)
r = subprocess.run([str(VENV_PY), "-c", nb_code], capture_output=True, text=True, cwd=WORK)
nb_out = r.stdout.rstrip("\n").split("\x00")
def after_cell(code):
    m = re.search(r"```python\n" + re.escape(code) + r"\n```\n\n```\n(.*?)^```$", md, re.S | re.M)
    return m.group(1) if m else ""
compare("notebook cell 1", after_cell('print("Hello, Riverstone")'), nb_out[0])
compare("notebook cell 2", after_cell("2 + 2 * 10"), nb_out[1])
compare("Jupyter traceback", after_cell("values = [1, 2, 3]\nprint(values[5])"), nb_out[2])

# ---- 5. requirements.txt: the lines shown are the first lines of a real freeze --------------------
req = re.search(r"```text\n(anyio.*?)^```$", md, re.S | re.M).group(1)
r = subprocess.run([str(VENV_PY), "-m", "pip", "freeze"], capture_output=True, text=True)
compare("requirements.txt first lines", req, "\n".join(r.stdout.splitlines()[:len(req.strip().splitlines())]))

# ---- 6. Figure 17.3: its traceback is a real one ---------------------------------------------------
notry = final.replace('''        try:
            if row["status"] != "Cancelled":
                values.append(float(row["net_revenue"]))
        except (ValueError, TypeError, KeyError):
            bad += 1
''', '''        if row["status"] != "Cancelled":
            values.append(float(row["net_revenue"]))
''')
target = WORK / "summarize_exports.py"
saved = target.read_text()
target.write_text(notry)
r = subprocess.run([str(VENV_PY), "summarize_exports.py", "."], cwd=WORK, capture_output=True, text=True)
target.write_text(saved)
sys.path.insert(0, str(BOOK / "figures"))
os.chdir(BOOK / "figures")
import make_figs17
compare("Figure 17.3 traceback", "\n".join(make_figs17.TRACE), r.stderr)

# ---- 7. numbers quoted in the answers and the timed challenge --------------------------------------
rows = []
for f in sorted((WORK / "sales_exports").glob("*.csv")):
    with open(f, encoding="utf-8", newline="") as fh:
        rows += [dict(r, file=f.name) for r in csv.DictReader(fh)]
live = [r for r in rows if r["status"] != "Cancelled"]
vals = [float(r["net_revenue"]) for r in live]
by_month = collections.Counter(); by_prod = collections.Counter(); by_cust = collections.Counter()
for r in live:
    by_month[r["file"]] += float(r["net_revenue"]); by_prod[r["product_name"]] += float(r["net_revenue"])
    by_cust[r["customer_name"]] += float(r["net_revenue"])
facts = {
    "rows 330": len(rows) == 330, "non-cancelled 326": len(live) == 326,
    "total 4335471.00": round(sum(vals), 2) == 4335471.00,
    "October 681070.75 highest": by_month.most_common(1)[0] == ("riverstone_2025_10.csv", 681070.75),
    "June 186928 lowest": min(by_month.items(), key=lambda kv: kv[1]) == ("riverstone_2025_06.csv", 186928.0),
    "top products": [(p, round(v, 2)) for p, v in by_prod.most_common(3)] == [("Storage Box 25L", 908212.5), ("Storage Box 10L", 860946.0), ("Industrial Crate", 795830.0)],
    "23 customers": len(by_cust) == 23,
    "top customers": [(c, round(v, 2)) for c, v in by_cust.most_common(2)] == [("Sharma Hardware", 502775.0), ("Harbour Traders", 412680.5)],
    "status counts": collections.Counter(r["status"] for r in rows) == {"Delivered": 322, "Cancelled": 4, "Shipped": 3, "Pending": 1},
    "mean 13298.99": round(statistics.mean(vals), 2) == 13298.99, "median 10212.50": statistics.median(vals) == 10212.5,
    "max 56700": max(vals) == 56700.0, "units 9475": sum(int(r["quantity"]) for r in live) == 9475,
    "largest line 85": max(int(r["quantity"]) for r in live) == 85, "16 cities": len({r["city"] for r in rows}) == 16,
    "attainment 102.3%": round(sum(vals) / 4240000 * 100, 1) == 102.3,
    "dates 2025-01-02..2025-12-23": (min(r["order_date"] for r in rows), max(r["order_date"] for r in rows)) == ("2025-01-02", "2025-12-23"),
}
targets = {r["target_month"]: float(r["target_revenue"]) for r in csv.DictReader(open(WORK / "targets_2025.csv"))}
beat = sum(1 for m, t in targets.items() if by_month[f"riverstone_{m.replace('-', '_')}.csv"] > t)
facts["6 months beat target"] = beat == 6
facts["targets sum 4240000"] = sum(targets.values()) == 4240000
for k, v in facts.items():
    print(("ok  " if v else "MISMATCH ") + k)
    if not v:
        problems.append(k)

if FILL:
    CHAPTER.write_text(md, encoding="utf-8")
print(f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
