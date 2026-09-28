"""Chapter 20 checks: the parts verify_python.py can't run on its own.

    python3 checks/ch20_check.py            # from the book folder (Data Science/Analyst-to-Architect)

1. Makes companion/ch20/.env from .env.example if it is missing, with RIVERSTONE_DB taken from the
   environment (default: the verification login book:book on localhost).
2. Starts the aiosmtpd test mail server on localhost:8025, runs every Python block of the chapter in
   order (including the "run: none" send cell of section 20.6), and checks that the send cell prints
   the output shown in the chapter and that the server's first lines match the chapter's excerpt
   (the boundary numbers and the client port change every run, so those two are compared by shape).
3. Runs daily_flash.py with --send twice (one email, then "already sent"), and checks the exit codes.
4. Checks that the main() shown in section 20.11 is exactly the one in companion/ch20/daily_flash.py.
Exit code 0 if everything passes.
"""
import contextlib, io, os, re, shutil, subprocess, sys, time
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
MD = next((BOOK / "manuscript").glob("ch20-*.md"))
C20 = BOOK / "companion" / "ch20"
DB = os.environ.get("RIVERSTONE_DB", "postgresql+psycopg://book:book@localhost:5432/riverstone_full")
ok = True

def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))

env_file = C20 / ".env"
if not env_file.exists():
    text = (C20 / ".env.example").read_text(encoding="utf-8")
    env_file.write_text(re.sub(r"^RIVERSTONE_DB=.*$", "RIVERSTONE_DB=" + DB, text, flags=re.M), encoding="utf-8")
for d in ("out", "logs", "runs"):
    shutil.rmtree(C20 / d, ignore_errors=True)

server_log = C20 / "logs_smtp_server.txt"
server = subprocess.Popen([sys.executable, "-u", "-m", "aiosmtpd", "-n", "-l", "localhost:8025"],
                          stdout=open(server_log, "w"), stderr=subprocess.STDOUT)
time.sleep(1.5)
try:
    md = MD.read_text(encoding="utf-8")
    os.chdir(C20); sys.path.insert(0, str(C20))
    token = re.compile(r'<!-- (py): reset -->|<!-- run: (none) -->|^```(\w*)\n(.*?)^```$', re.S | re.M)
    ns, pending, last_label = {"__name__": "__main__"}, False, None
    send_output = None; expect_send = None; expect_server = None
    for m in token.finditer(md):
        if m.group(1): ns = {"__name__": "__main__"}; continue
        if m.group(2): pending = True; continue
        lang, body = m.group(3), m.group(4)
        if lang == "python":
            if pending and not body.startswith("import smtplib"):
                pending = False; last_label = None; continue      # other run-none cells: excerpt, webhooks
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                exec(compile(body, "<ch20>", "exec"), ns)
            last_label = "send" if pending else "cell"
            if pending: send_output = buf.getvalue()
            pending = False
            continue
        if last_label == "send" and lang == "":
            expect_send = body; last_label = "server"; continue
        if last_label == "server" and lang == "text":
            expect_server = body; last_label = None; continue
        if lang: last_label = None if last_label != "server" else last_label
    time.sleep(1)
    check("send cell output matches the chapter", send_output is not None and
          send_output.strip() == (expect_send or "").strip(), repr(send_output))
    got = server_log.read_text(encoding="utf-8").splitlines()
    shape = lambda s: re.sub(r"={15}\d+==", "=BOUNDARY=", re.sub(r"\('127\.0\.0\.1', \d+\)", "(PEER)", s))
    want = (expect_server or "").strip("\n").splitlines()
    if os.environ.get("CH20_DUMP"): Path(os.environ["CH20_DUMP"]).write_text("\n".join(got[:40]), encoding="utf-8")
    check("server excerpt matches the first lines received", [shape(l) for l in got[:len(want)]] == [shape(l) for l in want],
          "\n".join(got[:len(want)]))

    first = subprocess.run([sys.executable, "daily_flash.py", "2025-12-18", "--send"], capture_output=True, text=True)
    second = subprocess.run([sys.executable, "daily_flash.py", "2025-12-18", "--send"], capture_output=True, text=True)
    check("first --send run exits 0 and sends", first.returncode == 0 and "sent to 1 recipient(s)" in first.stderr, first.stderr)
    check("second --send run sends nothing", second.returncode == 0 and "already sent; nothing to do" in second.stderr, second.stderr)
    time.sleep(1)
    check("the test server received two emails in all (the cell's and the script's)",
          server_log.read_text(encoding="utf-8").count("---------- MESSAGE FOLLOWS ----------") == 2)

    # Answer 14: the per-product 10th-percentile rule on 18 and 17 December 2025.
    import pandas as pd
    from datetime import date, timedelta
    from sqlalchemy import create_engine, text
    engine = create_engine(DB)
    q = text("""SELECT s.order_date, p.product_name, SUM(s.quantity) AS quantity
                FROM sales_lines s JOIN products p ON p.product_id = s.product_id
                WHERE s.order_date BETWEEN :start AND :end GROUP BY s.order_date, p.product_name""")
    flagged = {}
    for d in (date(2025, 12, 18), date(2025, 12, 17)):
        p10 = pd.read_sql(q, engine, params={"start": d - timedelta(days=90), "end": d - timedelta(days=1)}
                          ).groupby("product_name")["quantity"].quantile(0.10)
        today = pd.read_sql(q, engine, params={"start": d, "end": d}).set_index("product_name")["quantity"]
        flagged[d.day] = sorted((name, int(today[name]), float(p10[name])) for name in today.index if today[name] < p10[name])
    check("answer 14, 17 December: only Food Container Set (960 against 990)",
          flagged[17] == [("Food Container Set", 960, 990.0)], flagged[17])
    check("answer 14, 18 December: six products, not Industrial Crate",
          len(flagged[18]) == 6 and "Industrial Crate" not in [f[0] for f in flagged[18]], flagged[18])

    shown = re.search(r'<!-- run: none -->\n```python\n(def main\(.*?)```', md, re.S).group(1)
    real = re.search(r'^def main\(.*?^        return 2\n', (C20 / "daily_flash.py").read_text(), re.S | re.M).group(0)
    check("main() in section 20.11 matches daily_flash.py", shown == real)
finally:
    server.terminate(); server.wait()
    server_log.unlink(missing_ok=True)
    for d in ("out", "logs", "runs"):
        shutil.rmtree(C20 / d, ignore_errors=True)
print("all checks passed" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
