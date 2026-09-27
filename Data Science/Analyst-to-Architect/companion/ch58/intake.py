#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 58 · the purchase-order intake pipeline, end to end.
Email in, order in the ERP or in a human's queue, every step recorded. Assembles Chapter 54's extraction,
Chapter 57's tolerant parsing and metering, and this chapter's writes to a system of record.
Run: python3 intake.py
"""
from __future__ import annotations

import datetime as dt
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'ch57'))
import erp
from pipeline import PROMPTS, load_emails, parse
from provider import Meter, call

PRODUCT_CODES = set(erp.PRICES)
APPROVAL_LIMIT = 100_000          # rupees: above this, a person signs it off (section 58.5)
PIPELINE_VERSION = 'intake-v1 (prompt v3, model v1)'


def validate(order: dict | None) -> list[str]:
    """Business rules, not formats. Anything here sends the order to a person rather than the ERP."""
    if order is None:
        return ['the reply could not be parsed']
    problems = []
    if not str(order.get('po_number') or '').startswith('PO-'):
        problems.append('missing or malformed PO number')
    if not order.get('customer'):
        problems.append('missing customer')
    delivery = order.get('delivery_date')
    try:
        parsed = dt.date.fromisoformat(delivery) if delivery else None
    except (TypeError, ValueError):
        parsed = None
        problems.append(f'delivery date not YYYY-MM-DD: {delivery!r}')
    if parsed and not (dt.date(2026, 1, 1) <= parsed <= dt.date(2027, 1, 1)):
        problems.append(f'delivery date outside the plausible window: {parsed}')
    items = order.get('items') or []
    if not items:
        problems.append('no order lines')
    for item in items:
        if str(item.get('product_code')) not in PRODUCT_CODES:
            problems.append(f'unknown product code {item.get("product_code")!r}')
        quantity = item.get('quantity')
        if not isinstance(quantity, int) or not 1 <= quantity <= 10_000:
            problems.append(f'implausible quantity {quantity!r}')
    return problems


def run(emails: dict, truth: dict | None = None, approval_limit: int = APPROVAL_LIMIT,
        meter: Meter | None = None, at: str = '2026-03-02T06:00:00') -> dict:
    """One morning's intake run. Returns the counts a dashboard would show."""
    connection = erp.connect()
    outcome = Counter()
    queue = []
    for name, text in emails.items():
        reply = call(PROMPTS['v3'].format(name=name) + '\nEMAIL:\n' + text, model='v1', meter=meter)
        order = parse(reply)
        problems = validate(order)
        erp.log(connection, name, 'proposed', PIPELINE_VERSION,
                'clean' if not problems else '; '.join(problems[:2]), at)
        if problems:
            outcome['held_for_review'] += 1
            queue.append({'email': name, 'reasons': problems})
            connection.commit()
            continue
        value = erp.order_value(order['items'])
        if value > approval_limit:
            erp.write_order(connection, order, name, 'awaiting_approval', PIPELINE_VERSION, at)
            outcome['awaiting_approval'] += 1
            queue.append({'email': name, 'reasons': [f'order value Rs {value:,.0f} is above the '
                                                     f'Rs {approval_limit:,} approval limit']})
        else:
            written = erp.write_order(connection, order, name, 'loaded', PIPELINE_VERSION, at)
            outcome['loaded' if written else 'duplicate_ignored'] += 1
    connection.commit()
    connection.close()
    return {'counts': dict(outcome), 'queue': queue}


if __name__ == '__main__':
    erp.rebuild()
    truth, emails = load_emails()
    meter = Meter()
    result = run(emails, truth, meter=meter)
    total = sum(result['counts'].values())
    loaded = result['counts'].get('loaded', 0)
    print(f'{total} emails: ' + ', '.join(f'{k.replace("_", " ")} {v}' for k, v in sorted(result['counts'].items())))
    print(f'straight-through rate: {loaded / total:.0%}')
    print(f'model cost for the run: Rs {meter.cost_rupees():.2f}')
