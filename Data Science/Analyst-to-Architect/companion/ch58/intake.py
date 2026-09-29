#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 58 · Intelligent Automation
File: intake.py - the purchase-order intake pipeline, end to end (sections 58.3 to 58.6).
What: email in; an order in the ERP, or a reason in a person's queue; every step in the audit log.
  validate() is Chapter 54's (section 54.7), with the processing day set to this chapter's run.
  decide(), write() and run() are written out in the chapter, cell by cell; this file keeps them
  together so exercises and scripts can import them. run() includes section 58.6's circuit breaker.
Needs: ../ch54 (mock_llm.py, extraction.py, order_data/ from generate_order_emails.py) and
  ../ch57 (pipeline.py, provider.py). No model account: provider.call answers with Chapter 54's stand-in.
How:  from intake import run;  import erp;  erp.rebuild();  result = run(emails)
Run:  python intake.py   (rebuilds erp.db and runs the 60 practice emails once)
Tested on: Python 3.11 and 3.12 (standard library only).
Riverstone Supplies is fictional; every name and number here is invented.
"""
import sqlite3
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "ch57"))       # Chapter 57's pipeline.py and provider.py
sys.path.insert(0, str(HERE.parent / "ch54"))       # Chapter 54's stand-in and the 60 emails
import erp
from pipeline import build_prompt, load_emails, tolerant_parse
from provider import PINNED_MODEL, Meter, call

PRODUCT_CODES = set(erp.PRICES)
TODAY = date(2026, 3, 2)          # the morning of this chapter's run; in production, date.today()
FIRST_RUN = "2026-03-02T06:00:00"


def validate(order):
    """Return a list of problems. An empty list means the order is safe to load."""
    problems = []
    if not order.get("po_number") or not str(order["po_number"]).startswith("PO-"):
        problems.append("po_number missing or malformed")
    if not order.get("customer"):
        problems.append("customer missing")
    delivery = order.get("delivery_date")
    try:
        parsed = date.fromisoformat(delivery) if delivery else None
    except (TypeError, ValueError):
        parsed = None
        problems.append(f"delivery_date not YYYY-MM-DD: {delivery!r}")
    if parsed and not (TODAY - timedelta(days=30) <= parsed <= TODAY + timedelta(days=365)):
        problems.append(f"delivery_date outside the plausible window: {parsed}")
    items = order.get("items") or []
    if not items:
        problems.append("no items")
    for item in items:
        if str(item.get("product_code")) not in PRODUCT_CODES:
            problems.append(f"unknown product code {item.get('product_code')!r}")
        quantity = item.get("quantity")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or not 1 <= quantity <= 10_000:
            problems.append(f"implausible quantity {quantity!r}")
    return problems


APPROVAL_LIMIT = 100_000          # rupees: above this, a person signs the order off
PIPELINE_VERSION = f"intake-v1 (prompt v3, {PINNED_MODEL})"

def decide(order, problems, approval_limit=APPROVAL_LIMIT):
    """Where one extracted order goes, and why: held, awaiting_approval, or loaded."""
    if problems:
        return "held", "; ".join(problems)
    rupees = erp.order_value_paise(order["items"]) / 100
    if rupees > approval_limit:
        return "awaiting_approval", f"value ₹{rupees:,.0f} is over the ₹{approval_limit:,} limit"
    return "loaded", ""


def write(connection, run_id, name, order, status, reason):
    """Write one order and its lines in one transaction. Returns (what happened, why)."""
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO orders (po_number, customer, delivery_date, order_value_paise, "
                "source_email, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (order["po_number"], order["customer"], order["delivery_date"],
                 erp.order_value_paise(order["items"]), name, status, run_id))
            order_id = cursor.lastrowid
            for item in order["items"]:
                connection.execute(
                    "INSERT INTO order_lines (order_id, product_code, quantity, unit_price_paise) "
                    "VALUES (?, ?, ?, ?)",
                    (order_id, item["product_code"], item["quantity"],
                     erp.PRICES[item["product_code"]] * 100))
            detail = f"order {order_id}, {len(order['items'])} lines"
            erp.log(connection, run_id, name, status, PIPELINE_VERSION, detail)
        return status, reason
    except sqlite3.IntegrityError:
        same_email = connection.execute(
            "SELECT order_id FROM orders WHERE source_email = ?", (name,)).fetchone()
        if same_email:
            status = "duplicate_ignored"
            reason = f"this email is already order {same_email['order_id']}"
        else:
            status = "duplicate_po"
            reason = f"{order['customer']} already has an order for {order['po_number']}"
        with connection:
            erp.log(connection, run_id, name, status, PIPELINE_VERSION, reason)
        return status, reason


QUEUED = ("held", "awaiting_approval", "duplicate_po")   # the outcomes a person must look at
BREAKER_SHARE = 0.2               # stop when more than 20% of the batch has failed validation...
BREAKER_MINIMUM = 10              # ...once at least 10 emails have been processed

class BatchAborted(Exception):
    """Raised when so much of a batch fails that the run should stop and a person should look."""


def run(emails, run_id=FIRST_RUN, approval_limit=APPROVAL_LIMIT, meter=None):
    """One intake run over a dictionary of emails. Returns the counts and the queue."""
    connection = erp.connect()
    counts = Counter()
    queue = []
    for name, text in emails.items():
        order = tolerant_parse(call(build_prompt("v3", text), meter=meter))
        problems = ["reply was not valid JSON"] if order is None else validate(order)
        status, reason = decide(order, problems, approval_limit)
        with connection:
            erp.log(connection, run_id, name, "proposed", PIPELINE_VERSION,
                    "; ".join(problems) or "clean")
        if status == "held":
            with connection:
                erp.log(connection, run_id, name, "held", PIPELINE_VERSION, reason)
        else:
            status, reason = write(connection, run_id, name, order, status, reason)
        counts[status] += 1
        if status in QUEUED:
            queue.append({"email": name, "status": status, "reason": reason})
        processed = sum(counts.values())
        if processed >= BREAKER_MINIMUM and counts["held"] > BREAKER_SHARE * processed:
            message = f"{counts['held']} of {processed} emails failed validation"
            with connection:
                erp.log(connection, run_id, "(batch)", "batch_aborted", PIPELINE_VERSION, message)
            connection.close()
            raise BatchAborted(message)
    connection.close()
    return {"counts": dict(counts), "queue": queue}


if __name__ == "__main__":
    erp.rebuild()
    truth, emails = load_emails()
    meter = Meter()
    result = run(emails, meter=meter)
    total = sum(result["counts"].values())
    for status, count in sorted(result["counts"].items()):
        print(f"{status.replace('_', ' '):<20}{count:>3}")
    print(f"straight-through rate: {result['counts'].get('loaded', 0) / total:.0%}")
    print(f"model cost of the run: ₹{meter.cost_rupees():.2f}")
