#!/usr/bin/env python3
"""Riverstone's invoice matching, as it was first written: for each invoice, look through every order line.
Analyst to Architect · Chapter 33 · the "before" version (section 33.11's project)."""
import csv, sys, time


def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def match(invoices, order_lines):
    results = []
    for invoice in invoices:
        found = None
        for line in order_lines:                       # this loop is the problem
            if line['order_id'] == invoice['order_id'] and line['product_id'] == invoice['product_id']:
                found = line
                break
        results.append((invoice['invoice_line_id'], found['net_revenue'] if found else None))
    return results


if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    order_lines = load('match_data/order_lines.csv')
    invoices = load('match_data/supplier_invoices.csv')[:limit]
    started = time.perf_counter()
    results = match(invoices, order_lines)
    elapsed = time.perf_counter() - started
    matched = sum(1 for _, value in results if value is not None)
    print(f'{len(invoices):,} invoices against {len(order_lines):,} order lines')
    print(f'matched {matched:,}, unmatched {len(results) - matched:,}')
    print(f'took {elapsed:.2f} seconds')
