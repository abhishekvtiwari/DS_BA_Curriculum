#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 58 · Intelligent Automation
File: erp.py - Riverstone's order book, as a system of record.
A small SQLite database with the three things any system you write to automatically must have:
  * a uniqueness rule, so the same email can never create two orders (idempotency);
  * a transaction, so an order and its lines are written together or not at all;
  * an audit log, so every write can be traced to what proposed it and who approved it.
Run: python3 erp.py   (rebuilds an empty erp.db and prints its schema)
Tested on: Python 3.12.3 (standard library only).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

DB = Path(__file__).parent / 'erp.db'

SCHEMA = """
DROP TABLE IF EXISTS order_lines;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS audit_log;

CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    po_number      TEXT    NOT NULL,
    customer       TEXT    NOT NULL,
    delivery_date  TEXT    NOT NULL,
    order_value    REAL    NOT NULL,
    source_email   TEXT    NOT NULL UNIQUE,   -- the idempotency key: one email, one order
    status         TEXT    NOT NULL,          -- loaded | awaiting_approval
    created_at     TEXT    NOT NULL
);

CREATE TABLE order_lines (
    line_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id     INTEGER NOT NULL REFERENCES orders(order_id),
    product_code TEXT    NOT NULL,
    quantity     INTEGER NOT NULL,
    unit_price   REAL    NOT NULL,
    line_value   REAL    NOT NULL
);

CREATE TABLE audit_log (
    entry_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    at           TEXT NOT NULL,
    source_email TEXT NOT NULL,
    action       TEXT NOT NULL,     -- proposed | loaded | held | rejected | approved
    actor        TEXT NOT NULL,     -- the pipeline's version, or a person's name
    detail       TEXT NOT NULL
);
"""

PRICES = {'101': 430, '102': 750, '103': 115, '104': 620, '105': 1400, '106': 1150, '107': 380, '108': 290}


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB)
    connection.execute('PRAGMA foreign_keys = ON')
    connection.row_factory = sqlite3.Row
    return connection


def rebuild() -> None:
    with connect() as connection:
        connection.executescript(SCHEMA)


def log(connection, source_email: str, action: str, actor: str, detail: str, at: str) -> None:
    connection.execute('INSERT INTO audit_log (at, source_email, action, actor, detail) VALUES (?,?,?,?,?)',
                       (at, source_email, action, actor, detail))


def order_value(items: list[dict]) -> float:
    return round(sum(PRICES[item['product_code']] * item['quantity'] for item in items), 2)


def write_order(connection, order: dict, source_email: str, status: str, actor: str, at: str) -> int | None:
    """Write an order and its lines in one transaction. Returns None if this email is already loaded."""
    already = connection.execute('SELECT order_id FROM orders WHERE source_email = ?', (source_email,)).fetchone()
    if already:
        log(connection, source_email, 'duplicate_ignored', actor, f'already order {already["order_id"]}', at)
        return None
    try:
        with connection:                       # one transaction: header and lines together, or neither
            cursor = connection.execute(
                'INSERT INTO orders (po_number, customer, delivery_date, order_value, source_email, status, created_at)'
                ' VALUES (?,?,?,?,?,?,?)',
                (order['po_number'], order['customer'], order['delivery_date'],
                 order_value(order['items']), source_email, status, at))
            order_id = cursor.lastrowid
            for item in order['items']:
                price = PRICES[item['product_code']]
                connection.execute(
                    'INSERT INTO order_lines (order_id, product_code, quantity, unit_price, line_value)'
                    ' VALUES (?,?,?,?,?)',
                    (order_id, item['product_code'], item['quantity'], price,
                     round(price * item['quantity'], 2)))
            log(connection, source_email, status, actor, f'order {order_id}, {len(order["items"])} lines', at)
        return order_id
    except sqlite3.IntegrityError as exc:      # a concurrent write got there first
        log(connection, source_email, 'rejected', actor, f'integrity error: {exc}', at)
        return None


if __name__ == '__main__':
    rebuild()
    with connect() as connection:
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    print('erp.db rebuilt with tables:', ', '.join(row['name'] for row in tables))
