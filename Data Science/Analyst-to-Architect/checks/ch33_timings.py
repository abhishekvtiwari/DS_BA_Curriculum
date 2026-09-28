#!/usr/bin/env python3
"""ch33_timings.py - every timing quoted in Chapter 33, measured. Writes checks/ch33_timings_log.txt.

How:  cd companion/ch33 && python generate_ch33_data.py && python ../../checks/ch33_timings.py
Timings vary by machine; the shapes (linear, quadratic, log) do not. The log records the machine.
"""
import csv, heapq, pathlib, platform, os, random, statistics, sys, time, tracemalloc
from bisect import bisect_left
from collections import deque
from functools import lru_cache

BOOK = pathlib.Path(__file__).resolve().parents[1]
DATA = BOOK / 'companion' / 'ch33' / 'match_data'
LOG = open(BOOK / 'checks' / 'ch33_timings_log.txt', 'w', encoding='utf-8')
sys.setrecursionlimit(10000)


def log(line=''):
    LOG.write(line + '\n'); LOG.flush(); print(line)


def median_time(fn, repeats=5):
    times = []
    for _ in range(repeats):
        started = time.perf_counter(); fn(); times.append(time.perf_counter() - started)
    return statistics.median(times)


def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


log(f'machine: {os.cpu_count()} CPU(s), {platform.processor() or platform.machine()}, '
    f'{platform.system()} {platform.release()}, Python {platform.python_version()}')
log()
log('== reading the order file once')
log(f'load order_lines.csv: {median_time(lambda: load(DATA / "order_lines.csv"), repeats=3):.3f} s')
order_lines = load(DATA / 'order_lines.csv')
invoices = load(DATA / 'carrier_invoice_lines.csv')

log()
log('== naive matching: every invoice against every order line (median of 3 runs)')
log('   (the chapter\'s cell, run at the top level of a notebook or script, as a reader runs it)')
CELL = """
matched = 0
for invoice in invoices[:N]:
    for line in order_lines:
        if (line["order_id"] == invoice["order_id"]
                and line["product_id"] == invoice["product_id"]):
            matched += 1
            break
"""
naive = {}
for n in (250, 500, 1000, 2000):
    code = compile(CELL.replace('N', str(n)), 'cell', 'exec')
    def run():
        exec(code, {'invoices': invoices, 'order_lines': order_lines})
    naive[n] = median_time(run, repeats=3)
    log(f'{n:>5} invoices x 176,110 order lines: {naive[n]:6.2f} s')
log(f'predicted for 20,000 invoices: {naive[2000] * 10:.0f} s')

index = {(l['order_id'], l['product_id']): l for l in order_lines}
log()
log('== the same job with a dictionary index (median of 5 runs)')
t_build = median_time(lambda: {(l['order_id'], l['product_id']): l for l in order_lines})
def with_index():
    for invoice in invoices:
        index.get((invoice['order_id'], invoice['product_id']))
t_match = median_time(with_index)
log(f'build the index over 176,110 lines: {t_build:.3f} s')
log(f'look up all 20,000 invoices:        {t_match:.3f} s')
log(f'build + match:                      {t_build + t_match:.3f} s')

log()
log('== queue: list.pop(0) vs deque.popleft (100,000 items)')
def with_list():
    items = list(range(100_000))
    while items: items.pop(0)
def with_deque():
    items = deque(range(100_000))
    while items: items.popleft()
log(f'list.pop(0)      : {median_time(with_list, repeats=3):.3f} s')
log(f'deque.popleft()  : {median_time(with_deque, repeats=3):.3f} s')

log()
log('== cycle check on a chain of 18 diamonds (a DAG with no cycle)')
def diamonds(k):
    g = {}
    for i in range(k):
        a, b, c, d = f'n{i}', f'l{i}', f'r{i}', f'n{i + 1}'
        g[a] = [b, c]; g[b] = [d]; g[c] = [d]
    g[f'n{k}'] = []
    return g
def has_cycle_paths(graph):                       # the first draft: re-walks every path
    def visit(node, path):
        if node in path:
            return True
        for neighbor in graph.get(node, []):
            if visit(neighbor, path | {node}):
                return True
        return False
    return any(visit(node, frozenset()) for node in graph)
def has_cycle(graph):                             # the chapter's version: each node checked once
    done, on_path = set(), set()
    def visit(node):
        if node in on_path:
            return True
        if node in done:
            return False
        on_path.add(node)
        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True
        on_path.remove(node)
        done.add(node)
        return False
    return any(visit(node) for node in graph)
g18 = diamonds(18)
log(f're-walking every path : {median_time(lambda: has_cycle_paths(g18), repeats=1):.2f} s')
log(f'remembering done nodes: {median_time(lambda: has_cycle(g18)):.6f} s')

log()
log('== searching a sorted list of 1,000,000 numbers')
numbers = list(range(0, 4_000_000, 4))
targets = random.Random(33).sample(numbers, 10_000)
def linear():
    for t in targets[:200]:
        numbers.index(t)
def binary():
    for t in targets:
        bisect_left(numbers, t)
log(f'list.index()  200 searches : {median_time(linear, repeats=3):.3f} s')
log(f'bisect     10,000 searches : {median_time(binary):.4f} s')

log()
log('== top 10 of 176,110 values: sorted vs heapq.nlargest (median of 5)')
values = [(float(row['net_revenue']), row['order_id']) for row in order_lines]
log(f'sorted(...)[:10]   : {median_time(lambda: sorted(values, reverse=True)[:10]):.3f} s')
log(f'heapq.nlargest(10) : {median_time(lambda: heapq.nlargest(10, values)):.3f} s')

log()
log('== distinct pairs in 20,000 rows: a list of seen pairs vs a set')
rows = order_lines[:20_000]
def with_seen_list():
    seen = []
    for row in rows:
        key = (row['order_id'], row['product_id'])
        if key not in seen:
            seen.append(key)
t_list = median_time(with_seen_list, repeats=1)
t_set = median_time(lambda: {(row['order_id'], row['product_id']) for row in rows})
log(f'list: {t_list:.2f} s   set: {t_set:.4f} s   ratio: {t_list / t_set:,.0f}x')

log()
log('== recursion: fibonacci with and without memoization')
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)
for n in (25, 30, 32):
    log(f'fib({n}) plain      : {median_time(lambda n=n: fib(n), repeats=3):7.3f} s')
fib_memo.cache_clear()
log(f'fib(32) memoized   : {median_time(lambda: fib_memo(32), repeats=1):.6f} s')
log(f'fib(300) memoized  : {fib_memo(300)}')

log()
log('== memory: a list of 1,000,000 numbers vs a generator')
tracemalloc.start()
big = [i * 2 for i in range(1_000_000)]
current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
log(f'list        : {peak / 1_000_000:.1f} MB peak, sum {sum(big)}')
del big
tracemalloc.start()
total = sum(i * 2 for i in range(1_000_000))
current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
log(f'generator   : {peak / 1_000_000:.4f} MB peak, sum {total}')
