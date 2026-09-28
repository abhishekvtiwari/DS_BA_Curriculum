#!/usr/bin/env python3
"""The same job, with an index: build a dictionary once, then look each invoice up.
Analyst to Architect · Chapter 33 · the "after" version (the chapter's project)."""
import csv, time


def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def build_index(order_lines):
    return {(line['order_id'], line['product_id']): line for line in order_lines}


def match(invoices, index):
    return [(invoice['invoice_line_id'],
             index.get((invoice['order_id'], invoice['product_id']), {}).get('net_revenue'))
            for invoice in invoices]


if __name__ == '__main__':
    order_lines = load('match_data/order_lines.csv')
    invoices = load('match_data/carrier_invoice_lines.csv')
    started = time.perf_counter()
    index = build_index(order_lines)
    built = time.perf_counter()
    results = match(invoices, index)
    elapsed = time.perf_counter() - started
    matched = sum(1 for _, value in results if value is not None)
    print(f'{len(invoices):,} invoices against {len(order_lines):,} order lines')
    print(f'matched {matched:,}, unmatched {len(results) - matched:,}')
    print(f'index built in {built - started:.2f} s, matching took {elapsed - (built - started):.3f} s, total {elapsed:.2f} s')
