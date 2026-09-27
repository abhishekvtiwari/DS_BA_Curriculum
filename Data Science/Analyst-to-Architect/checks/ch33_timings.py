#!/usr/bin/env python3
"""ch33_timings.py - every timing quoted in Chapter 33, measured. Writes ch33_timings_log.txt.
Machine: sandbox, 1 vCPU, 3 GB RAM, Ubuntu 24.04, Python 3.12.3."""
import csv, random, statistics, sys, time, tracemalloc
from bisect import bisect_left
from collections import deque
sys.setrecursionlimit(10000)
LOG = open('/home/claude/book/checks/ch33_timings_log.txt', 'w')
def log(line):
    LOG.write(line + '\n'); LOG.flush(); print(line)

def median_time(fn, repeats=5):
    times = []
    for _ in range(repeats):
        started = time.perf_counter(); fn(); times.append(time.perf_counter() - started)
    return statistics.median(times)

def load(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

order_lines = load('/home/claude/book/companion/ch33/match_data/order_lines.csv')
invoices = load('/home/claude/book/companion/ch33/match_data/supplier_invoices.csv')

log('== naive matching grows with the square of the work')
for n in (250, 500, 1000, 2000):
    subset = invoices[:n]
    def naive():
        for invoice in subset:
            for line in order_lines:
                if line['order_id'] == invoice['order_id'] and line['product_id'] == invoice['product_id']:
                    break
    t = median_time(naive, repeats=1)
    log(f'{n:>5} invoices x 176,110 order lines: {t:6.2f} s')

index = {(l['order_id'], l['product_id']): l for l in order_lines}
log('')
log('== the same job with a dictionary index')
t_build = median_time(lambda: {(l['order_id'], l['product_id']): l for l in order_lines}, repeats=3)
def with_index():
    for invoice in invoices:
        index.get((invoice['order_id'], invoice['product_id']))
t_match = median_time(with_index, repeats=3)
log(f'build the index over 176,110 lines: {t_build:.3f} s')
log(f'look up all 20,000 invoices:        {t_match:.3f} s')

log('')
log('== membership: list vs set vs dict (1,000 lookups)')
keys = [(l['order_id'], l['product_id']) for l in order_lines]
key_set, key_list = set(keys), keys
needles = random.Random(33).sample(keys, 1000)
log(f'list  "in" : {median_time(lambda: [n in key_list for n in needles], repeats=1):8.3f} s')
log(f'set   "in" : {median_time(lambda: [n in key_set for n in needles]):8.5f} s')
log(f'dict  "in" : {median_time(lambda: [n in index for n in needles]):8.5f} s')

log('')
log('== queue: list.pop(0) vs deque.popleft (100,000 items)')
def with_list():
    items = list(range(100_000))
    while items: items.pop(0)
def with_deque():
    items = deque(range(100_000))
    while items: items.popleft()
log(f'list.pop(0)      : {median_time(with_list, repeats=1):.3f} s')
log(f'deque.popleft()  : {median_time(with_deque, repeats=3):.3f} s')

log('')
log('== searching a sorted list of 1,000,000 numbers (10,000 searches)')
numbers = list(range(0, 4_000_000, 4))
targets = random.Random(33).sample(numbers, 10_000)
def linear():
    for t in targets[:200]:
        numbers.index(t)
def binary():
    for t in targets:
        bisect_left(numbers, t)
log(f'list.index()  200 searches : {median_time(linear, repeats=1):.3f} s')
log(f'bisect     10,000 searches : {median_time(binary):.4f} s')

log('')
log('== recursion: fibonacci with and without memoization')
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
from functools import lru_cache
@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)
for n in (25, 30, 32):
    log(f'fib({n}) plain      : {median_time(lambda n=n: fib(n), repeats=1):7.3f} s')
log(f'fib(32) memoized   : {median_time(lambda: fib_memo.__wrapped__ and fib_memo(32), repeats=1):.6f} s')
log(f'fib(300) memoized  : {fib_memo(300)}')

log('')
log('== memory: a list of 1,000,000 rows vs a generator')
tracemalloc.start()
rows = [i * 2 for i in range(1_000_000)]
current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
log(f'list        : {peak / 1_000_000:.1f} MB peak, sum {sum(rows)}')
tracemalloc.start()
gen = (i * 2 for i in range(1_000_000))
total = sum(gen)
current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
log(f'generator   : {peak / 1_000_000:.4f} MB peak, sum {total}')
