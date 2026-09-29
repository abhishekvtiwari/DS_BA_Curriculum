#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 58 · Intelligent Automation
File: erp.py - Riverstone's order book, as a system of record (section 58.4).
What: a small SQLite database, erp.db, next to this file, with three tables: orders, order_lines and
  audit_log. The schema carries the rules any table you write to automatically must have:
    * UNIQUE (source_email): re-reading the same email can never create a second order (idempotency);
    * UNIQUE (customer, po_number): a customer's resent PO is refused, so a person can look at it;
    * money as whole paise, and a CHECK on the status values;
    * an audit log naming the run and the pipeline version behind every step.
  The transaction that writes an order and its lines together is intake.py's write().
How:  import erp;  erp.rebuild();  connection = erp.connect()
Run:  python erp.py   (rebuilds an empty erp.db and lists its tables)
Tested on: Python 3.11 and 3.12 (standard library only).
Riverstone Supplies is fictional; every name and number here is invented.
"""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "erp.db"

SCHEMA = """
DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS audit_log;

CREATE TABLE orders (
    order_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    po_number          TEXT    NOT NULL,
    customer           TEXT    NOT NULL,
    delivery_date      TEXT    NOT NULL,
    order_value_paise  INTEGER NOT NULL,         -- money as whole paise
    source_email       TEXT    NOT NULL UNIQUE,  -- the idempotency key
    status             TEXT    NOT NULL
        CHECK (status IN ('loaded', 'awaiting_approval')),
    created_at         TEXT    NOT NULL,
    UNIQUE (customer, po_number)                 -- one PO, one order
);

CREATE TABLE order_lines (
    line_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id          INTEGER NOT NULL REFERENCES orders (order_id),
    product_code      TEXT    NOT NULL,
    quantity          INTEGER NOT NULL,
    unit_price_paise  INTEGER NOT NULL
);

CREATE TABLE audit_log (
    entry_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        TEXT NOT NULL,   -- which run: the second it started
    source_email  TEXT NOT NULL,   -- which input
    action        TEXT NOT NULL,   -- proposed, loaded, held, ...
    actor         TEXT NOT NULL,   -- pipeline version, or a person
    detail        TEXT NOT NULL    -- the reason, in words
);
"""

# Riverstone's list prices in rupees per unit: the products table of the riverstone_2025 database.
PRICES = {"101": 430, "102": 750, "103": 115, "104": 620,
          "105": 1400, "106": 1150, "107": 380, "108": 290}


def connect():
    connection = sqlite3.connect(DB)
    connection.execute("PRAGMA foreign_keys = ON")    # make SQLite check REFERENCES
    connection.row_factory = sqlite3.Row              # rows you can read by column name
    return connection


def rebuild():
    """Start again from an empty order book: drop the three tables and create them."""
    connection = connect()
    connection.executescript(SCHEMA)
    connection.close()


def log(connection, run_id, source_email, action, actor, detail):
    """One audit row. The caller decides which transaction it belongs to."""
    connection.execute(
        "INSERT INTO audit_log (run_id, source_email, action, actor, detail) "
        "VALUES (?, ?, ?, ?, ?)",
        (run_id, source_email, action, actor, detail))


def order_value_paise(items):
    """What an order is worth at list prices, in whole paise (100 paise = 1 rupee)."""
    return sum(PRICES[item["product_code"]] * 100 * item["quantity"] for item in items)


if __name__ == "__main__":
    rebuild()
    connection = connect()
    names = [row["name"] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    connection.close()
    print(f"{DB.name} rebuilt with tables: {', '.join(names)}")
