"""Chapter 46 companion: Riverstone's daily pipeline as one file, for Dagster's web interface.
The same assets, check, job, and schedule as the chapter's notebook, plus the two sensors of section 46.6.
Run it from work/ch46, with the notebook's kernel shut down and the environment active:
    terminal 1:  python mock_crm_api.py
    terminal 2:  dagster dev -f riverstone_pipeline.py      then open http://127.0.0.1:3000
Nothing runs when this file is loaded: no reset, no practice days, no API server.
Riverstone Supplies is fictional; every name and number is invented."""
import os, hashlib
import duckdb, requests
import dagster as dg
from dotenv import load_dotenv

load_dotenv()
import ingest

WAREHOUSE = "warehouse/riverstone_wh.duckdb"

def warehouse():
    """Open the warehouse for one step; each step closes it again when it finishes."""
    return duckdb.connect(WAREHOUSE)

daily = dg.DailyPartitionsDefinition(start_date="2026-01-01", end_date="2026-01-06", timezone="Asia/Kolkata")

# --- Ingestion ---

@dg.asset
def raw_orders(context):
    with warehouse() as wh:
        new, changed, deleted = ingest.sync_table(wh, "orders")
    context.log.info(f"raw_orders: {new} new, {changed} changed, {deleted} deleted")

@dg.asset
def raw_order_items(context):
    with warehouse() as wh:
        new, changed, deleted = ingest.sync_table(wh, "order_items")
    context.log.info(f"raw_order_items: {new} new, {changed} changed, {deleted} deleted")

@dg.asset(partitions_def=daily)
def raw_dispatch(context):
    day = context.partition_key
    with warehouse() as wh:
        outcome = ingest.load_dispatch(wh, day)
    context.log.info(f"[{day}] raw_dispatch: {outcome}")

@dg.asset(retry_policy=dg.RetryPolicy(max_retries=3, delay=1))
def raw_crm_leads(context):
    try:
        leads = ingest.fetch_leads()
    except requests.HTTPError as e:
        code = e.response.status_code
        if code in (400, 401, 403, 404):
            raise dg.Failure(description=f"CRM refused the request ({code})", allow_retries=False)
        raise
    with warehouse() as wh:
        n = ingest.load_leads(wh, leads)
    context.log.info(f"raw_crm_leads: {n} leads (attempt {context.retry_number + 1})")

# --- The Flash, its check, and delivery ---

FLASH_SQL = """
    SELECT COUNT(DISTINCT o.order_id) AS orders_booked,
           ROUND(COALESCE(SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100)), 0), 2)
               AS revenue_booked
    FROM {orders} AS o
    JOIN {items} AS i ON i.order_id = o.order_id
    WHERE o.order_date = {day}
      AND o.status <> 'Cancelled'"""

INSERT_FLASH = ("INSERT INTO mart.daily_flash SELECT CAST(? AS DATE), * FROM ("
                + FLASH_SQL.format(orders="raw.orders", items="raw.order_items", day="?") + ")")

@dg.asset(partitions_def=daily, deps=[raw_orders, raw_order_items])
def daily_flash(context):
    day = context.partition_key
    with warehouse() as wh:
        wh.execute("CREATE SCHEMA IF NOT EXISTS mart")
        wh.execute("""CREATE TABLE IF NOT EXISTS mart.daily_flash (
                          flash_date DATE, orders_booked INTEGER, revenue_booked DECIMAL(12,2))""")
        wh.execute("BEGIN")
        try:
            wh.execute("DELETE FROM mart.daily_flash WHERE flash_date = ?", [day])
            wh.execute(INSERT_FLASH, [day, day])
            wh.execute("COMMIT")
        except Exception:
            wh.execute("ROLLBACK")
            raise
        n, rev = wh.execute("SELECT orders_booked, revenue_booked FROM mart.daily_flash WHERE flash_date = ?",
                            [day]).fetchone()
    context.log.info(f"[{day}] daily_flash: orders={n}, revenue=Rs {rev:,.2f}")

@dg.asset_check(asset=daily_flash, blocking=True)
def flash_matches_erp(context):
    day = context.partition_key
    src_n, src_rev = ingest.fetch_rows(
        FLASH_SQL.format(orders="orders", items="order_items", day="%s"), [day])[0]
    with warehouse() as wh:
        rows = wh.execute("SELECT orders_booked, revenue_booked FROM mart.daily_flash WHERE flash_date = ?",
                          [day]).fetchall()
    passed = len(rows) == 1 and rows[0][0] == src_n and rows[0][1] == src_rev
    return dg.AssetCheckResult(passed=passed, metadata={"erp_orders": src_n, "erp_revenue": float(src_rev),
                                                        "warehouse_rows": len(rows)})

@dg.asset(partitions_def=daily, deps=[daily_flash])
def deliver_flash(context):
    day = context.partition_key
    with warehouse() as wh:
        n, rev = wh.execute("SELECT orders_booked, revenue_booked FROM mart.daily_flash WHERE flash_date = ?",
                            [day]).fetchone()
        body = (f"Riverstone Daily Sales Flash - {day}\n"
                f"Orders booked: {n}\n"
                f"Net bookings (excl. cancelled, net of discounts): Rs {rev:,.2f}\n")
        digest = hashlib.sha256(body.encode()).hexdigest()
        wh.execute("""CREATE TABLE IF NOT EXISTS mart.delivery_log (
                          flash_date DATE, delivery_no INTEGER, content_sha VARCHAR,
                          revenue DECIMAL(12,2), file_name VARCHAR)""")
        sent = wh.execute("""SELECT content_sha, revenue FROM mart.delivery_log
                             WHERE flash_date = ? ORDER BY delivery_no""", [day]).fetchall()
        if digest in [s[0] for s in sent]:
            context.log.info(f"[{day}] deliver_flash: already delivered, skipped")
            return
        if sent:
            old = sent[-1][1]
            body = (f"CORRECTION to the Flash sent earlier for {day}: "
                    f"revenue changed from Rs {old:,.2f} to Rs {rev:,.2f}.\n\n" + body)
            name = f"flash_{day}_correction_{len(sent)}.txt"
        else:
            name = f"flash_{day}.txt"
        with open(f"outbox/{name}", "w") as f:
            f.write(body)
        wh.execute("INSERT INTO mart.delivery_log VALUES (?, ?, ?, ?, ?)", [day, len(sent) + 1, digest, rev, name])
    context.log.info(f"[{day}] deliver_flash: wrote outbox/{name}")

# --- Jobs, schedule, and sensors ---

flash_job = dg.define_asset_job("daily_flash_job", selection=[raw_orders, raw_order_items, raw_dispatch,
                                                               raw_crm_leads, daily_flash, deliver_flash])
flash_schedule = dg.build_schedule_from_partitioned_job(flash_job, hour_of_day=6, minute_of_hour=30)
dispatch_job = dg.define_asset_job("dispatch_job", selection=[raw_dispatch])

@dg.sensor(job=dispatch_job, minimum_interval_seconds=300)
def dispatch_file_sensor(context):
    for name in sorted(os.listdir("exports")):
        if name.startswith("dispatch_"):
            yield dg.RunRequest(run_key=name, partition_key=name[9:19])

def send_message(to, subject, body):
    """Stand-in for email, Slack, or Teams: write the message to the alerts folder."""
    with open(f"alerts/{subject[:40].replace(' ', '_').replace(':', '')}.txt", "w") as f:
        f.write(f"To: {to}\nSubject: {subject}\n\n{body}\n")

@dg.run_failure_sensor(monitored_jobs=[flash_job])
def flash_failure_alert(context: dg.RunFailureSensorContext):
    run = context.dagster_run
    send_message(to="data-oncall@riverstone.example",
                 subject=f"Daily Sales Flash failed: run {run.run_id[:8]}",
                 body=f"Failed job: {run.job_name}\nError: {context.failure_event.message}\n"
                      f"Runbook: docs/runbooks/daily_flash.md")

defs = dg.Definitions(assets=[raw_orders, raw_order_items, raw_dispatch, raw_crm_leads, daily_flash, deliver_flash],
                      asset_checks=[flash_matches_erp], jobs=[flash_job], schedules=[flash_schedule],
                      sensors=[dispatch_file_sensor, flash_failure_alert],
                      executor=dg.in_process_executor)     # one step at a time: DuckDB allows one writer
