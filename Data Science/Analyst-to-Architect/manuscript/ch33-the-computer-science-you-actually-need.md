# Chapter 33. The Computer Science You Actually Need

*Part 3 — Advanced Analytics & Analytics Engineering*

> **Chapter at a glance**
>
> **You will learn to:** describe how long an algorithm takes in the language everyone uses (Big-O), and see the curves in measured times · choose between a list, a dictionary, a set, and a tuple for a reason · explain why a dictionary lookup is instant, and why the same trick powers a database hash join · use stacks and queues where they fit, including `deque` · write and read recursion without fear, and know when a loop is clearer · walk trees and graphs with depth-first and breadth-first search, and detect cycles · tell linear search from binary search, and know what `sorted()` costs · recognize memoization, dynamic programming, and greedy algorithms when you meet them · think about memory as well as speed · and talk through a coding problem the way interviewers expect.
>
> **Before you start:** Chapter 17 (Python: lists, dictionaries, sets, loops, functions, CSV files), Chapter 18 (NumPy and pandas, which you'll compare with plain loops, and `lambda`), Chapter 28 (indexes, hash joins, and recursive CTEs, the database version of several ideas here), Chapter 29 (tests and generators), and Chapter 32 (a dbt project as a DAG).
>
> **Time needed:** 14–18 hours, spread over three weeks, in four sittings: sections 33.1–33.4; recursion, trees and graphs (33.5–33.6); searching, sorting, memoization and dynamic programming (33.7–33.8); sections 33.9–33.10 and the project.
>
> **Tools:** Python 3.11 or later and its standard library. Nothing else.
>
> **Practice data:** `generate_ch33_data.py` in the companion folder builds 176,110 order lines and 20,000 invoice lines from Riverstone's logistics partner, which the chapter's project matches. This is a synthetic, scaled-up Riverstone: about 66,700 orders over 23 months, nearly 400 times the orders of the one-year database you've used since Chapter 12, so that the slow version is slow enough to measure. Its amounts are not Riverstone's real revenue. Every timing shown was measured on the author's test machine (an Intel Xeon at 2.1 GHz, Ubuntu 24.04, Python 3.11.15) and is reproduced by `ch33_timings.py`. **Timings vary by machine**: yours will differ, but the shapes (what happens when the data doubles) won't.

---

## Why this matters

You can have a long, well-paid career in data without knowing what a binary tree is. You cannot have one without meeting these three situations:

- **The script that got slower.** It ran in twenty seconds on last year's file. This year's file is ten times the size and it's been going for half an hour. Nothing changed except the data.
- **The interview.** Analytics engineering and data engineering interviews include a coding round, and the questions are all from this chapter's vocabulary: *"can you do this without a nested loop?"*, *"what's the complexity of your solution?"*
- **The conversation with engineers.** When a backend engineer says "that endpoint is O(n²) in the number of orders", you either know what that sentence claims or you nod.

This chapter is not a computer-science course. It's the subset that changes how you write Python next week, with every claim measured rather than asserted. One idea in it, the dictionary index in section 33.2, is worth the whole chapter: it turns the project's two-minute matching job into about 0.06 seconds (0.050 seconds to build the index, 0.007 seconds to match).

---

## In plain English

**Complexity is about how the work grows, not how long it takes today.**

Imagine finding one person in a hotel:

- You know the room number: walk there. One step, however big the hotel is. That's **constant time**.
- You must knock on every door: a hundred doors, a hundred knocks; a thousand doors, a thousand knocks. **Linear time**.
- The rooms are sorted and you can ask "higher or lower": a thousand rooms takes about ten questions, a million takes about twenty. **Logarithmic time**, and it barely notices when the hotel grows.
- You must introduce every guest to every other guest: a hundred guests is 4,950 introductions; a thousand is half a million. **Quadratic time**, and it's the reason most slow scripts are slow.

The point isn't the maths. It's that the hotel always gets bigger. A method that grows quadratically works fine on today's data, and the day the file doubles it takes four times as long. The way out is usually to build an index first, which is what a dictionary is, and what the database does when it builds a hash table for a join (Chapter 28).

---

## 33.1 Big-O: how work grows

**Big-O** describes how an algorithm's work grows with the size of its input, ignoring constants and small terms. It's a shape, not a stopwatch.

| Notation | Called | Work when the input doubles | Everyday example |
|---|---|---|---|
| O(1) | constant | unchanged | dictionary lookup, appending to a list (on average: the list occasionally grows its storage) |
| O(log n) | logarithmic | one more step | binary search, index lookup in a database |
| O(n) | linear | doubles | scanning a list, reading a file |
| O(n log n) | linearithmic | slightly more than doubles | sorting |
| O(n²) | quadratic | four times | a loop inside a loop over the same data |
| O(2ⁿ) | exponential | squares | trying every combination |

### The chapter's data

The chapter works on one job, from the project at the end: Riverstone's logistics partner bills Riverstone for every order line it delivered to customers, one invoice line per order line, and each invoice line has to be matched to the order line it bills. First build the two files. In a terminal, in the companion folder:

```
# terminal, in companion/ch33
$ python generate_ch33_data.py
wrote match_data/order_lines.csv: 176,110 order lines
wrote match_data/carrier_invoice_lines.csv: 20,000 invoice lines (19,500 should match, 500 should not)
```

The script writes a folder called `match_data` with two CSV files. Before you read on, predict: of the 20,000 invoice lines, how many will a correct matching script match? The script's own last line tells you what the answer should be, which is exactly what you want from test data.

Now load both files into Python, with Chapter 17's `csv.DictReader`, and look at one row of each:

```python
import csv

def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

order_lines = load("match_data/order_lines.csv")
invoices = load("match_data/carrier_invoice_lines.csv")
print(f"{len(order_lines):,} order lines, {len(invoices):,} invoice lines")
print(order_lines[0])
print(invoices[0])
```

```
176,110 order lines, 20,000 invoice lines
{'order_id': '100000', 'product_id': '103', 'quantity': '100', 'net_revenue': '38000', 'order_date': '2024-10-10'}
{'invoice_line_id': 'INV012129', 'order_id': '130195', 'product_id': '108', 'amount': '37240.0'}
```

How it works:

- **`load(path)`** opens a CSV file and returns a list of dictionaries, one per row, keyed by the header. `newline=""` and `encoding="utf-8"` are Chapter 17's settings for reading CSV files safely.
- **An order line** has `order_id`, `product_id`, `quantity`, `net_revenue` and `order_date`. **An invoice line** has its own `invoice_line_id`, the `order_id` and `product_id` of the order line it bills, and the `amount` billed.
- **Every value from `csv.DictReader` is text**, so ids are strings like `'100000'`, and amounts are strings like `'38000'` until you convert them with `float()`.

An invoice line matches an order line when both the `order_id` and the `product_id` agree.

### The slow way, measured

Here is the matching job as a careful person first writes it: for each invoice, look through the order lines until you find its match. Time it on the first 250 invoices:

<!-- run: none -->
```python
import time

started = time.perf_counter()
matched = 0
for invoice in invoices[:250]:
    for line in order_lines:
        if (line["order_id"] == invoice["order_id"]
                and line["product_id"] == invoice["product_id"]):
            matched += 1
            break
elapsed = time.perf_counter() - started
print(f"250 invoices: matched {matched}, took {elapsed:.2f} s")
```

```
250 invoices: matched 242, took 1.52 s
```

How it works:

- **`time.perf_counter()`** is Chapter 18's stopwatch: read it before and after, and subtract.
- **The outer loop** takes one invoice at a time (`invoices[:250]` is the first 250). **The inner loop** walks the order lines from the top.
- **The `if`** tests both columns; the brackets let the condition continue onto a second line.
- **`break`** stops the inner loop as soon as the match is found. So a matched invoice costs, on average, a scan of half the order lines, and an **unmatched** invoice costs a scan of all 176,110: the invoices that match nothing are the most expensive ones.

That's up to 250 × 176,110, or about 44 million comparisons, for 250 invoices. Now the same cell with 500, 1,000 and 2,000 invoices (the timing script runs each three times and keeps the middle value):

<!-- run: none -->
```
# terminal, in companion/ch33  (median of three runs, from ch33_timings.py)
  250 invoices x 176,110 order lines:   1.48 s
  500 invoices x 176,110 order lines:   3.07 s
 1000 invoices x 176,110 order lines:   5.71 s
 2000 invoices x 176,110 order lines:  11.62 s
```

Double the invoices, double the time: that's linear *in the number of invoices*, because the order lines stayed the same. The quadratic part appears when both grow together, which is what happens in real life: next year Riverstone has twice the invoices **and** twice the orders, so the job takes four times as long. Extrapolating the last row, the full 20,000-invoice file takes about **two minutes** today (11.62 × 10 = 116 seconds), and almost eight minutes when the business doubles (116 × 4 = 464 seconds).

![Five curves drawn to one scale, with ticked axes: constant and logarithmic stay near the floor, linear and n log n rise steadily, and quadratic leaves the top of the chart early; a side panel lists the measured matching times](figures/fig33-1-growth-curves.svg)

*Figure 33.1 — The five shapes (drawn to scale) and the matching job's measured times. Constant and logarithmic barely move; quadratic leaves the chart.*

**How to read your own code's complexity**, without any algebra:

1. **Count the loops over your data.** One loop over n items is O(n). A loop inside a loop over the same n is O(n²).
2. **A lookup inside a loop is the thing to watch.** `if x in some_list` is itself a loop, so putting it inside a loop makes the whole thing quadratic. `if x in some_set` is not.
3. **Sorting is O(n log n)**, which is close enough to linear that sorting once is almost always worth it.
4. **Constants don't matter to Big-O, but they matter to you.** O(n) that reads from disk can be slower than O(n²) in memory, for small n. Big-O tells you what happens as n grows; the stopwatch tells you what happens today.

> **Watch out: Big-O ignores exactly the things that make code fast.** Two O(n) algorithms can differ by a factor of fifty. pandas and NumPy are fast not because their complexity is better but because their constants are tiny: the work happens in compiled code over contiguous memory instead of in a Python loop (Chapter 18). Use Big-O to choose the approach, and a measurement to choose between two implementations of it.

---

## 33.2 The four structures you'll use every day

| Structure | Written | Keeps order? | Lookup by value | Good at | Bad at |
|---|---|---|---|---|---|
| **list** | `[1, 2, 3]` | yes | O(n) | keeping a sequence, appending | finding, removing from the front |
| **dict** | `{"a": 1}` | insertion order | O(1) by key | lookups, grouping, counting | memory; range questions ("everything between two values"); ordering by value |
| **set** | `{1, 2, 3}` | no | O(1) | membership, deduplication, difference | anything ordered |
| **tuple** | `(1, 2)` | yes | O(n) | fixed records, dictionary keys | changing anything |

Measure the difference yourself with **`timeit`**, the standard library's tool for timing small operations. It runs a piece of code many times and returns the total seconds:

<!-- run: none -->
```python
import timeit

keys = [(line["order_id"], line["product_id"]) for line in order_lines]
keys_set = set(keys)
wanted = keys[-1]                 # the last key: the worst case for a list

list_seconds = timeit.timeit(lambda: wanted in keys, number=1000)
set_seconds = timeit.timeit(lambda: wanted in keys_set, number=1000)
print(f"list 'in', 1,000 lookups: {list_seconds:.3f} s")
print(f"set  'in', 1,000 lookups: {set_seconds:.6f} s")
print(f"the set was about {list_seconds / set_seconds:,.0f} times faster")
```

```
list 'in', 1,000 lookups: 3.626 s
set  'in', 1,000 lookups: 0.000038 s
the set was about 96,354 times faster
```

How it works:

- **`keys`** is a list of 176,110 `(order_id, product_id)` tuples, and **`keys_set`** holds the same tuples in a set.
- **`timeit.timeit(code, number=1000)`** runs `code` 1,000 times and returns the total time. The code is passed as a `lambda` (Chapter 18): a one-line function with no name, so `timeit` can call it again and again. `number=` sets how many runs; more runs give a steadier total.
- **`wanted in keys`** must compare `wanted` with every element until it finds a match, and `wanted` is the last one. **`wanted in keys_set`** computes a hash and goes straight there (section 33.3 shows how).

That's not a small improvement, it's four orders of magnitude or more, and it comes from one keystroke: `set(...)` instead of `list(...)`. What happens if you change it? Make `wanted = keys[0]` and run the cell again: the list finds it at once and the gap almost disappears. A list is only slow when it has to look far, and in real data the key you want is rarely at the front.

### The dictionary index, which is most of this chapter's value

Any time you find yourself looking something up inside a loop, **build a dictionary first**. Here is the index for the matching job:

```python
# the index: one pass over the order lines, keyed by what the invoice knows
index = {(line["order_id"], line["product_id"]): line for line in order_lines}
print(f"index holds {len(index):,} keys")
```

```
index holds 176,110 keys
```

- **A dictionary comprehension** (Chapter 17) builds the whole dictionary in one pass over the order lines.
- **The key is a tuple**, `(order_id, product_id)`, because that pair is what an invoice line knows. The value is the whole order line.

176,110 keys for 176,110 lines proves that `(order_id, product_id)` is unique here. A dictionary silently keeps the **last** value when a key repeats, so if the key count were smaller than the line count, some lines would have been overwritten without a word; then you'd index into a list per key (`defaultdict(list)`), as the grouping section below does. And make both sides the same type: `'100001'` (text) and `100001` (a number) are different keys, so an index built from one file never matches ids read as numbers from another.

Now look each invoice up:

```python
matched = sum(1 for invoice in invoices
              if (invoice["order_id"], invoice["product_id"]) in index)
print(f"matched {matched:,}, unmatched {len(invoices) - matched:,}")
```

```
matched 19,500, unmatched 500
```

**`sum(1 for x in items if condition)`** is a **generator expression**: it looks like a list comprehension in round brackets, and it produces its values one at a time without building a list (section 33.9 explains why that saves memory). Adding up a 1 for every invoice that passes the test counts them. The test itself is one dictionary lookup.

One pass to build the index, one lookup per invoice: **O(n + m)** instead of **O(n × m)**. Measured by `ch33_timings.py`, that's 0.050 seconds to build and 0.007 seconds to match all 20,000 invoices, against about two minutes for the nested loop.

The same trick appears everywhere once you see it:

| Instead of | Do this |
|---|---|
| `for row in rows: if row["id"] in id_list` | make `id_set = set(id_list)` first |
| `for a in table_a: for b in table_b: if a.key == b.key` | index `table_b` by key, then loop `table_a` once |
| counting with `if key in counts: counts[key] += 1 else: ...` | `collections.Counter`, or `defaultdict(int)` |
| looking up a customer's name inside a loop | one dictionary built before the loop |

And the database does exactly this: Chapter 28's **hash join** builds a hash table of the smaller table, then scans the larger one once. When you build a dictionary index in Python, you are hand-writing a hash join.

### Grouping, counting, and the standard library

Chapter 17's `defaultdict` groups the order lines by product in one pass:

```python
from collections import Counter, defaultdict

by_product = defaultdict(list)
for line in order_lines:
    by_product[line["product_id"]].append(float(line["net_revenue"]))

revenue = {product: round(sum(values)) for product, values in by_product.items()}
for product in sorted(revenue, key=revenue.get, reverse=True)[:3]:
    print(f"product {product}: {len(by_product[product]):,} lines, revenue {revenue[product]:,}")
```

```
product 106: 22,084 lines, revenue 563,741,550
product 108: 22,042 lines, revenue 556,953,300
product 101: 22,075 lines, revenue 555,084,450
```

How it works:

- **`defaultdict(list)`** creates an empty list the first time a product appears, which removes the "is this key there yet?" dance.
- **`revenue`** adds up each product's list and rounds it.
- **`sorted(revenue, key=revenue.get, reverse=True)`** sorts the product ids by the value `revenue.get(id)` returns. Passing a function *without* brackets (`revenue.get`, not `revenue.get()`) hands it to `sorted`, which calls it on each item to get the value to sort by. `reverse=True` puts the largest first, and `[:3]` keeps the top three.

`Counter`, also from Chapter 17, counts in one line:

```python
invoiced_products = Counter(invoice["product_id"] for invoice in invoices)
print("most invoiced products:", invoiced_products.most_common(3))
```

```
most invoiced products: [('101', 2607), ('107', 2561), ('104', 2514)]
```

The argument to `Counter` is another generator expression, one product id per invoice line, and `.most_common(3)` returns the three most frequent with their counts. `defaultdict` and `Counter` are both O(n) with small constants, and both are the kind of thing that makes a script shorter *and* faster at once.

---

## 33.3 Hashing, and why dictionaries are instant

A **hash function** turns a value into a number. Python's `hash()` does it for any hashable value: numbers, strings, and tuples of those.

```python
for value in (100001, 100002, (100001, 101), (100002, 104), (100003, 108), (100004, 105)):
    print(f"{str(value):<15} hash {hash(value):>21} -> bucket {hash(value) % 8}")

print("same value, same hash:", hash((100001, 101)) == hash((100001, 101)))
print("lists are unhashable, which is why they can't be dictionary keys:")
try:
    hash([100001, 101])
except TypeError as exc:
    print("  TypeError:", exc)
```

```
100001          hash                100001 -> bucket 1
100002          hash                100002 -> bucket 2
(100001, 101)   hash  -5250647048266057633 -> bucket 7
(100002, 104)   hash    434502588224997158 -> bucket 6
(100003, 108)   hash   9115427311463621200 -> bucket 0
(100004, 105)   hash   2954519364476443151 -> bucket 7
same value, same hash: True
lists are unhashable, which is why they can't be dictionary keys:
  TypeError: unhashable type: 'list'
```

How it works:

- **`hash(value)`** returns the value's hash. A small whole number hashes to itself; a tuple's hash is computed from its parts.
- **`hash(value) % 8`** is the remainder after dividing by 8, always 0 to 7: the **bucket** the value would go in if the table had eight buckets.
- **`(100001, 101)` and `(100004, 105)` both land in bucket 7.** Two keys in the same bucket is a **collision**, and it's normal.
- **`try` / `except TypeError`** (Chapter 17) catches the error that hashing a list raises and prints its message.

(Strings hash differently in every Python process, deliberately, so the numbers above use integers to stay reproducible. The behavior is the same.)

A **hash table** (which is what a Python `dict` and `set` are) keeps an array of buckets. To store a key it hashes it, takes the remainder by the number of buckets, and puts the entry there. To find a key it does the same arithmetic and looks in one bucket. **That's why lookup doesn't get slower as the dictionary grows**: the work is one hash and one bucket, whatever the size.

![A hash table: four real keys pass through hash() % 8 into buckets 7, 6, 0 and 7; bucket 7 holds two entries and is labelled as a collision, and a lookup arrow goes straight to one bucket](figures/fig33-2-hash-table.svg)

*Figure 33.2 — Hash, take the remainder, look in one bucket. The bucket numbers are the real ones from the code above.*

This is the textbook "bucket" picture. Python's own `dict`, on a collision, tries another slot instead of stacking entries in one bucket, but the cost is the same: a few steps, not a scan. Two consequences worth carrying:

- **Keys must be immutable**, because a key that changed after being stored would hash to a different bucket and become invisible. That's why tuples work as keys and lists don't, and why the project's index is keyed by `(order_id, product_id)`.
- **Collisions** are normal and handled: Python finds another slot in a step or two. They only hurt if almost everything collides, which is a problem for adversarial input, not for order ids.

This is also what Chapter 28's **hash join** does: build a hash table from the smaller table, scan the larger one, and probe the table for each row. When PostgreSQL's plan says `Hash Join`, it is doing what section 33.2's dictionary index did.

---

## 33.4 Stacks and queues

Two structures with one rule each.

- A **stack** is last in, first out. Undo history, the call stack behind recursion (section 33.5), depth-first search.
- A **queue** is first in, first out. Job queues, retry backlogs, breadth-first search.

A Python list is already a fine stack: `append` and `pop` are both O(1). As a queue it is not, because `pop(0)` has to shift every remaining element along:

<!-- run: none -->
```
# terminal, in companion/ch33  (from ch33_timings.py, 100,000 items)
list.pop(0)      : 0.805 s
deque.popleft()  : 0.004 s
```

`collections.deque` is a double-ended queue: O(1) at both ends.

```python
from collections import deque

# a stack: the last invoice queried is the first one answered
stack = []
for invoice_id in ["INV000001", "INV000002", "INV000003"]:
    stack.append(invoice_id)
print("stack pops:", [stack.pop() for _ in range(3)])

# a queue: invoices are worked in the order they arrived
queue = deque(["INV000001", "INV000002", "INV000003"])
print("queue pops:", [queue.popleft() for _ in range(3)])

# a retry queue, which is where analysts meet this first
# pretend: invoices ending in 0 fail until their third attempt
retries = deque([("INV000010", 1), ("INV000011", 1)])
processed = []
while retries:
    invoice_id, attempt = retries.popleft()
    if attempt < 3 and invoice_id.endswith("0"):
        retries.append((invoice_id, attempt + 1))       # try again later, not immediately
    else:
        processed.append((invoice_id, attempt))
print("processed:", processed)
```

```
stack pops: ['INV000003', 'INV000002', 'INV000001']
queue pops: ['INV000001', 'INV000002', 'INV000003']
processed: [('INV000011', 1), ('INV000010', 3)]
```

How it works:

- **`stack.pop()`** removes and returns the last item, so the three come back in reverse order.
- **`for _ in range(3)`**: `_` is the conventional name for a loop variable you don't use. The comprehension just calls `pop()` three times.
- **`deque([...])`** builds a queue from a list, and **`popleft()`** removes from the front.
- **The retry queue** holds `(invoice_id, attempt)` pairs. A stand-in rule decides what fails: an id ending in `"0"` fails until its third attempt. A failure goes to the **back** of the queue with its attempt number raised, so `INV000011` is processed first, and `INV000010` succeeds on attempt 3.

That last pattern is a **retry queue**: failures go to the back, so one stubborn item doesn't block the rest. It complements Chapter 29's API client, which waits and retries the same request; a queue is what you use when you have many independent items.

---

## 33.5 Recursion

A **recursive** function calls itself on a smaller version of the problem. It needs two things: a **base case** that stops, and a **recursive case** that moves toward it.

Chapter 28 exploded the Garden Chair's bill of materials with a recursive CTE. Here is the same walk in Python, with the bill of materials as a dictionary: each assembly maps to a list of `(part, quantity)` pairs.

```python
parts = {                                    # Chapter 28's bill of materials, as a dictionary
    "Garden Chair": [("Seat shell", 1), ("Steel frame", 1),
                     ("Product label", 1), ("Shipping carton", 1)],
    "Seat shell": [("PP granules", 2.2), ("Masterbatch", 0.08)],
    "Steel frame": [("Leg assembly", 2), ("Steel tube", 1.0), ("Fastener pack", 1)],
    "Leg assembly": [("Steel tube", 1.2), ("Fastener pack", 1)],
}

def explode(part, quantity=1.0):
    if part not in parts:                                  # base case: a bought material
        return {part: quantity}
    totals = {}
    for child, child_quantity in parts[part]:              # recursive case: go one level down
        for material, amount in explode(child, quantity * child_quantity).items():
            totals[material] = totals.get(material, 0) + amount
    return totals

for material, amount in sorted(explode("Garden Chair").items()):
    print(f"{material:<16} {amount:>6.2f}")
```

```
Fastener pack      3.00
Masterbatch        0.08
PP granules        2.20
Product label      1.00
Shipping carton    1.00
Steel tube         3.40
```

How it works:

- **The base case**: a part that isn't in `parts` is a bought material, so `explode` returns it with the quantity needed, and stops.
- **The recursive case**: for each child, `explode` calls **itself** with the child and the multiplied quantity (`quantity * child_quantity`: two leg assemblies each needing 1.2 kg of tube is 2.4 kg). Every call is on a smaller piece of the tree, so the calls always reach materials in the end.
- **`totals.get(material, 0) + amount`** adds each child's materials into this part's totals, starting from 0 the first time a material appears.

Steel tube comes out at 3.4, matching Chapter 28's SQL exactly, because a recursive CTE and a recursive function are the same idea in two languages. Note that Steel tube and Fastener pack each arrive by two routes, and both must be counted.

**What if a part contains itself?** A data-entry mistake that makes the leg assembly contain the frame would send `explode` round in circles until Python stopped it. A **path** guard catches it: pass along the parts on the current route, and refuse to go down into one that is already on it.

```python
def explode_checked(part, quantity=1.0, path=()):
    if part in path:
        raise ValueError(f"cycle at {part}: {' -> '.join(path + (part,))}")
    if part not in parts:
        return {part: quantity}
    totals = {}
    for child, child_quantity in parts[part]:
        below = explode_checked(child, quantity * child_quantity, path + (part,))
        for material, amount in below.items():
            totals[material] = totals.get(material, 0) + amount
    return totals

parts["Leg assembly"].append(("Steel frame", 1))    # the mistake: the leg contains the frame
try:
    explode_checked("Garden Chair")
except ValueError as exc:
    print("ValueError:", exc)
parts["Leg assembly"].pop()                         # undo the mistake
print(f"fixed again, steel tube: {explode_checked('Garden Chair')['Steel tube']:.2f}")
```

```
ValueError: cycle at Steel frame: Garden Chair -> Steel frame -> Leg assembly -> Steel frame
fixed again, steel tube: 3.40
```

- **`path=()`** starts as an empty tuple. **`path + (part,)`** makes a new tuple with this part added: `(part,)` is a one-item tuple (the comma makes it a tuple).
- **`if part in path`** fires only when a part appears *on its own route*. Steel tube appearing twice, under two different parents, is fine; Steel frame inside its own leg assembly is not.
- **`raise ValueError(...)`** stops with a message that names the loop, which is what whoever fixes the data needs.

**The call stack.** Each call waits for the ones it makes, and Python keeps the waiting calls on a stack (section 33.4): the newest call is on top and finishes first. That stack has a limit (1,000 frames by default), so a walk over a deep structure can end in `RecursionError`. Compare a recursive count with a loop that does the same job:

```python
import sys

def depth(n):
    return 0 if n == 0 else 1 + depth(n - 1)

def depth_loop(n):
    count = 0
    while n > 0:
        n, count = n - 1, count + 1
    return count

print("limit:", sys.getrecursionlimit())
try:
    depth(5000)
except RecursionError as exc:
    print("RecursionError:", exc)
print("iterative version:", depth_loop(5000))
```

```
limit: 1000
RecursionError: maximum recursion depth exceeded
iterative version: 5000
```

- **`depth(n)`** counts down by calling itself: `depth(5000)` needs 5,000 calls waiting at once, more than the limit.
- **`depth_loop(n)`** does the same count with a `while` loop and two variables, so nothing waits and there is no limit.
- **`sys.getrecursionlimit()`** reports the limit. You can raise it with `sys.setrecursionlimit`, but a loop is usually the better fix.

**Recursion or a loop?** Use recursion when the data is itself nested: trees, bills of materials, folders, JSON (Chapter 17), nested comments. Use a loop when the problem is a straight sequence. Any recursion can be rewritten as a loop with an explicit stack, and sometimes should be, which is exactly what exercise 7 asks you to do.

---

## 33.6 Trees and graphs

You wrote recursive functions in section 33.5; walking a tree is the same idea.

A **tree** is data where each item has one parent: Riverstone's org chart, its bill of materials, a folder structure, a category hierarchy. A **graph** is the general case, where anything can connect to anything: customers and the orders they share, tables and their dependencies (Chapter 32's DAG is a graph), roads between cities. Each item is a **node**; each link between two nodes (reports to, contains, depends on) is an **edge**.

Chapter 28 walked these in SQL with recursive CTEs. In Python they're a dictionary of lists. Here is a slice of Chapter 28's staff table (the key accounts sales team, and the production branch down to the machine operator Chapter 28 traced), with each manager mapped to their direct reports:

```python
reports_to = {
    "Arvind Kapoor": ["Anita Rao", "Harpreet Sethi"],
    "Anita Rao": ["Vikram Singh", "Farah Khan"],
    "Harpreet Sethi": ["Ramesh Patil"],
    "Vikram Singh": ["Neha Kulkarni", "Rahul Mehta"],
    "Ramesh Patil": ["Ajay Kumar"],
    "Ajay Kumar": ["Gopal Sahu"],
}

def depth_first(person, level=0, seen=None):
    seen = seen if seen is not None else set()
    if person in seen:
        return []                       # already visited: don't walk it twice
    seen.add(person)
    result = [(level, person)]
    for report in reports_to.get(person, []):
        result += depth_first(report, level + 1, seen)
    return result

for level, person in depth_first("Arvind Kapoor"):
    print("    " * level + person)
```

```
Arvind Kapoor
    Anita Rao
        Vikram Singh
            Neha Kulkarni
            Rahul Mehta
        Farah Khan
    Harpreet Sethi
        Ramesh Patil
            Ajay Kumar
                Gopal Sahu
```

How it works:

- **`depth_first`** returns a list of `(level, person)` pairs: this person, then everyone below them, one branch at a time. It calls itself for each direct report with `level + 1`, exactly as `explode` called itself for each child part.
- **`reports_to.get(person, [])`** gives a person's direct reports, or an empty list for someone with none: that's the base case.
- **`seen=None`, then create the set inside.** A default like `seen=set()` would be created once, when the function is defined, and shared by every call, so a second walk would think everyone was already seen. `None` as the default, and a new set when it's `None`, gives each walk its own.
- **`result += ...`** adds the list the inner call returns onto this one.
- **`"    " * level + person`** repeats a four-space string `level` times, so each level is indented further.

Depth-first goes all the way down one branch before starting the next, which is why the output reads like an indented org chart. Breadth-first goes level by level, which is what you want for "who is two levels below the MD?" and for shortest paths:

```python
from collections import deque

def breadth_first(start):
    queue, seen, levels = deque([(start, 0)]), {start}, []
    while queue:
        person, level = queue.popleft()
        levels.append((level, person))
        for report in reports_to.get(person, []):
            if report not in seen:
                seen.add(report)
                queue.append((report, level + 1))
    return levels

walk = breadth_first("Arvind Kapoor")
for level in range(3):
    people = [p for lvl, p in walk if lvl == level]
    print(f"level {level}: {', '.join(people)}")
```

```
level 0: Arvind Kapoor
level 1: Anita Rao, Harpreet Sethi
level 2: Vikram Singh, Farah Khan, Ramesh Patil
```

- **The queue** starts with the MD at level 0. Each turn takes the person at the front, records them, and puts their reports at the **back**, one level deeper. So everyone at level 1 comes out before anyone at level 2.
- **`walk`** is computed once, before the loop; the loop then picks each level's people out of it. (Calling `breadth_first` inside the loop would walk the whole tree three times.)
- **`', '.join(people)`** (Chapter 17) joins the names with commas.

![The Riverstone org chart slice with each person labelled twice: purple D-badges give the depth-first order D1 to D10, green B-badges give the breadth-first order B1 to B10, with a key explaining each](figures/fig33-3-traversals.svg)

*Figure 33.3 — One tree, two orders. The only difference is whether the next node comes off a stack or a queue.*

**The two are the same algorithm with a different container.** Depth-first uses a stack (or recursion, which is a stack); breadth-first uses a queue. That single sentence answers a surprising number of interview questions.

### Cycles

Real data has loops in it: an employee whose manager reports to them, a part that contains itself, two dbt models that `ref` each other. There are two different guards, and it matters which one you use:

- A **seen** set skips anything already visited, anywhere. That's right for reachability ("who is below the MD?"), and it makes each node count once. Both walks above use one.
- A **path** set skips only what's on the current route. That's right for cycle detection, and for bills of materials, where one part can legitimately appear under two parents: a seen set would count Steel tube once and give 1.0 kg, not 3.4. It's the Python version of Chapter 28's `CYCLE` clause, and it's what `explode_checked`'s `path` did.

A good cycle check uses both: a path set to spot the loop, and a set of nodes already **done** (fully checked, with nothing below them looping), so no part of the graph is walked twice.

```python
broken = {"A": ["B"], "B": ["C"], "C": ["A"]}     # A -> B -> C -> A

def has_cycle(graph):
    done = set()        # nodes already proven to lead to no cycle
    on_path = set()     # nodes on the route being walked right now

    def visit(node):
        if node in on_path:
            return True               # back to a node on our own route: a cycle
        if node in done:
            return False              # checked before: nothing below it loops
        on_path.add(node)
        for neighbor in graph.get(node, []):
            if visit(neighbor):
                return True
        on_path.remove(node)
        done.add(node)
        return False

    return any(visit(node) for node in graph)

print("cycle in the org chart:", has_cycle(reports_to))
print("cycle in the broken data:", has_cycle(broken))
```

```
cycle in the org chart: False
cycle in the broken data: True
```

How it works:

- **`visit` is defined inside `has_cycle`**, a **nested function**. It can read and change `done`, `on_path` and `graph` from the function around it, so they don't have to be passed on every call.
- **`on_path`** gets a node when the walk goes down into it, and loses it when the walk comes back up. Meeting a node that is still on the path means the walk has come round in a circle.
- **`done`** gets a node once everything below it has been checked. A second route into that node stops at once, so every node and every edge is handled once: **O(V + E)**, for V nodes and E edges.
- **`any(...)`** is `True` as soon as one value is `True`, and stops there. Here it tries `visit` from each node in turn.

The remembered `done` set matters. A first version without it, which re-walks every route from every node, is exponential on graphs where routes split and rejoin, and dbt projects are full of those. On a chain of 18 such "diamonds" (no cycle at all), that version took 2.15 seconds on the test machine, and its time doubles with each diamond added; the version above took 0.00002 seconds. dbt runs this kind of check over a project's `ref`s, and refuses to run a project whose graph has a loop: Chapter 32's DAG has to stay acyclic, and this is how that is checked.

---

## 33.7 Searching and sorting

### Linear and binary search

Finding a value in an unsorted list means looking at every element until you find it: **linear search**, O(n). If the list is *sorted*, you can halve the search space with every comparison: **binary search**, O(log n). A million sorted values take about twenty comparisons.

<!-- run: none -->
```
# terminal, in companion/ch33  (from ch33_timings.py, a sorted list of 1,000,000 numbers)
list.index()  200 searches : 0.657 s
bisect     10,000 searches : 0.0070 s
```

Two hundred linear searches took 0.7 seconds; ten thousand binary searches took seven milliseconds. Python's `bisect` module does binary search on any sorted sequence. The everyday use is putting a value into sorted bands, such as Riverstone's loyalty rebate from Chapter 17: 0% as standard, 1% from ₹2,50,000 a year, 2% from ₹4,00,000:

```python
from bisect import bisect_right

thresholds = [0, 250_000, 400_000]      # where each band starts, sorted
rates = ["0%", "1%", "2%"]

def rebate_band(annual_value):
    if annual_value < thresholds[0]:
        raise ValueError(f"negative amount {annual_value}: credit notes need their own rule")
    return rates[bisect_right(thresholds, annual_value) - 1]

for value in (120_000, 250_000, 399_999, 400_000, 650_000):
    print(f"{value:>9,}: {rebate_band(value)}")
```

```
  120,000: 0%
  250,000: 1%
  399,999: 1%
  400,000: 2%
  650,000: 2%
```

How it works:

- **`bisect_right(thresholds, value)`** finds, by binary search, how many thresholds are less than or equal to `value`. For 120,000 that's 1 (only the 0), so `- 1` gives index 0, the first band.
- **A value equal to a threshold goes into the higher band**: 2,50,000 gets 1%, which is "from ₹2,50,000". That's the "right" in `bisect_right`.
- **The guard** at the top refuses a negative amount, for a reason the next cell shows.

Before you run the next cell, predict what band −500 would get without the guard:

```python
try:
    rebate_band(-500)
except ValueError as exc:
    print("ValueError:", exc)
print("without the guard:", rates[bisect_right(thresholds, -500) - 1])
```

```
ValueError: negative amount -500: credit notes need their own rule
without the guard: 2%
```

For −500, `bisect_right` returns 0, and index `0 - 1` is **−1**, which Python reads as "the last item": a credit note silently gets the top rebate. Negative indexes are the trap at the low end of any banding, so guard it. Bucketing a value into sorted bands is what a `CASE` statement does in SQL, done in log time instead of by checking every band.

`bisect` also keeps a list sorted as you add to it:

```python
from bisect import insort

prices = [290, 430, 750]
insort(prices, 620)                 # finds the place by binary search, and inserts there
print("prices:", prices)
```

```
prices: [290, 430, 620, 750]
```

`insort(prices, 620)` finds where 620 belongs by binary search (between 430 and 750) and inserts it there, so `prices` never needs sorting again. The search is O(log n); the insert still shifts the later items along, as `pop(0)` did in section 33.4.

### Sorting

`sorted()` and `list.sort()` use **Timsort**, which is O(n log n) and unusually fast on data that's already partly ordered, which real data usually is. Two habits are worth having: sorting by a computed value, and sorting by several columns. Start with three order lines:

```python
lines = [
    {"order_id": "100002", "product_id": "104", "net_revenue": "18600"},
    {"order_id": "100001", "product_id": "101", "net_revenue": "38000"},
    {"order_id": "100001", "product_id": "108", "net_revenue": "5800"},
]

def revenue_of(row):
    return float(row["net_revenue"])

by_revenue = sorted(lines, key=revenue_of, reverse=True)
print("largest first:", [row["net_revenue"] for row in by_revenue])

same = sorted(lines, key=lambda row: float(row["net_revenue"]), reverse=True)
print("the lambda gives the same:", same == by_revenue)
```

```
largest first: ['38000', '18600', '5800']
the lambda gives the same: True
```

- **`key=revenue_of`** tells `sorted` to call `revenue_of` on each row and sort by what it returns, the revenue as a number, without changing the rows. (Sorting the text `'5800'` against `'18600'` would put `'5800'` first, because text sorts character by character.)
- **`lambda row: float(row["net_revenue"])`** is exactly `revenue_of`, written inline without a name (Chapter 18). For a one-line key, most people write the `lambda`.

A **tuple key** sorts by several columns, exactly like SQL's `ORDER BY a, b` (Chapter 12):

```python
by_order_then_product = sorted(lines, key=lambda row: (row["order_id"], row["product_id"]))
print("by order, then product:", [(r["order_id"], r["product_id"]) for r in by_order_then_product])
```

```
by order, then product: [('100001', '101'), ('100001', '108'), ('100002', '104')]
```

Tuples compare item by item: the order ids first, and the product ids only when the order ids tie.

**Timsort is stable**: rows that tie keep the order they already had. So sorting twice, by the secondary key first and then by the primary key, gives the same answer as one tuple key:

```python
by_product = sorted(lines, key=lambda row: row["product_id"])
by_order = sorted(by_product, key=lambda row: row["order_id"])
print("two stable sorts:", [(r["order_id"], r["product_id"]) for r in by_order])
print("same as the tuple key:", by_order == by_order_then_product)
```

```
two stable sorts: [('100001', '101'), ('100001', '108'), ('100002', '104')]
same as the tuple key: True
```

The two 100001 lines tie on `order_id` in the second sort, so they stay in the product order the first sort gave them. That's what "stable" buys you.

For "the biggest three of a million", sorting everything to keep three is wasted work. **`heapq.nlargest(k, items, key=...)`** keeps only the best k seen so far in a small structure called a **heap** (a heap keeps its smallest item at the front, and can add or remove one item in log time), so it scans the data once: O(n log k).

```python
import heapq

top_two = heapq.nlargest(2, lines, key=lambda row: float(row["net_revenue"]))
print("largest two without sorting everything:", [row["net_revenue"] for row in top_two])
```

```
largest two without sorting everything: ['38000', '18600']
```

**When sorting is the algorithm.** Many problems get easy once the data is in order: finding duplicates (equal values sit together), finding the nearest match (binary search), merging two feeds (walk both in step), and grouping (Chapter 12's `GROUP BY` is a sort or a hash under the covers). Paying O(n log n) once to make everything after it linear is one of the most common good trades in data work.

---

## 33.8 Memoization, dynamic programming, and greedy

Three named ideas you'll meet in interviews and, occasionally, in real work.

### Memoization: remember what you already computed

The classic demonstration is Fibonacci (each number is the sum of the two before it), where the naive recursion recomputes the same values exponentially often:

<!-- run: none -->
```
# terminal, in companion/ch33  (from ch33_timings.py)
fib(25) plain      :   0.009 s
fib(30) plain      :   0.098 s
fib(32) plain      :   0.248 s
fib(32) memoized   : 0.000018 s
fib(300) memoized  : 222232244629420445529739893461909967206666939096499764990979600
```

Each step of five in `n` multiplies the plain version's time by about eleven: that's exponential growth, O(2ⁿ). Caching turns it linear, and Python has the cache built in:

```python
from functools import lru_cache

calls = {"plain": 0, "cached": 0}

def fib(n):
    calls["plain"] += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=None)
def fib_cached(n):
    calls["cached"] += 1
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)

fib(25)
fib_cached(25)
print(f"fib(25) plain  made {calls['plain']:,} calls")
print(f"fib(25) cached made {calls['cached']:,} calls")
print("same answer:", fib(25) == fib_cached(25))
```

```
fib(25) plain  made 242,785 calls
fib(25) cached made 26 calls
same answer: True
```

How it works:

- **`calls`** is a dictionary of two counters, raised by one on every call, so you can see how much work each version does.
- **`@lru_cache(...)`** on the line above `def` is a **decorator**: it wraps the function so each call first checks a dictionary of past arguments and their results, and only runs the function for an argument it hasn't seen. `maxsize=None` means never forget; a number such as `maxsize=1024` caps the memory by forgetting the least recently used results.
- **`fib_cached.cache_info()`** reports the cache's hits and misses, and `fib_cached.cache_clear()` empties it. Python also has `functools.cache`, the same thing with no size limit.

242,785 calls against 26. In analytics work, `@lru_cache` pays off on an expensive pure function called repeatedly with the same arguments: a currency conversion, a geocode, a parsed configuration.

### Dynamic programming

**Dynamic programming** is memoization turned into a table you fill in deliberately: solve the small subproblems once, in order, and build the answer from them. The question it answers is always "the best way to do X given a limit", and it appears in interviews far more often than in dashboards.

Take a small case by hand first: the fewest notes that make ₹60 exactly, with notes of ₹50, ₹20 and ₹10. Fill in a table from the bottom, one amount at a time. For each amount, try every note that fits, and look up the best answer for what's left:

| Amount (₹) | 0 | 10 | 20 | 30 | 40 | 50 | 60 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fewest notes | 0 | 1 | 1 | 2 | 2 | 1 | 2 |

For ₹60: a ₹10 note leaves ₹50 (best 1), a ₹20 note leaves ₹40 (best 2), a ₹50 note leaves ₹10 (best 1). So best[60] = min(1 + 1, 2 + 1, 1 + 1) = 2. Every entry is built from entries already in the table, and none is worked out twice. The code does exactly this, for every amount in steps of ₹1:

```python
def fewest_notes(amount, notes=(2000, 500, 200, 100, 50, 20, 10)):
    """The fewest notes that make an amount exactly, or None if it can't be made."""
    best = [0] + [None] * amount          # best[v]: fewest notes for v; None = can't be made
    for value in range(1, amount + 1):
        options = [best[value - note] + 1 for note in notes
                   if note <= value and best[value - note] is not None]
        best[value] = min(options) if options else None
    return best[amount]
```

How it works:

- **`best`** is the table, with one slot for every amount from 0 to `amount`. `best[0] = 0` (no notes make ₹0), and every other slot starts as `None`, meaning "can't be made".
- **For each `value`**, the comprehension tries every note that fits (`note <= value`) and whose remainder can be made (`best[value - note] is not None`), and counts one more note than the remainder needed.
- **`min(options)`** keeps the best; if no note works, the slot stays `None`.

Now run it:

```python
for amount in (760, 2750, 45, 0):
    answer = fewest_notes(amount)
    if answer is not None:
        print(f"₹{amount:>5}: {answer} notes")
    else:
        print(f"₹{amount:>5}: cannot be made exactly")
```

```
₹  760: 4 notes
₹ 2750: 4 notes
₹   45: cannot be made exactly
₹    0: 0 notes
```

The test is `answer is not None`, not `if answer`: 0 counts as false in Python, so `if answer` would call ₹0 impossible. Every amount below the target is solved once and reused, which is what makes this O(amount × notes) rather than exponential. (₹2000 notes were withdrawn from circulation in 2023, though they remain legal tender. Take 2000 out of `notes` and ₹2750 needs 7 notes instead of 4; the method doesn't change.)

### Greedy

A **greedy** algorithm takes the best-looking option at each step and never reconsiders. It's simpler and faster, and it's right only when the problem has the right shape.

```python
def greedy_notes(amount, notes=(2000, 500, 200, 100, 50, 20, 10)):
    count = 0
    for note in notes:
        count, amount = count + amount // note, amount % note
    return count if amount == 0 else None

odd_notes = (10, 6, 1)

print("Indian notes, ₹760:  greedy", greedy_notes(760), "vs best", fewest_notes(760))
print("made-up notes 10/6/1, 12: greedy", greedy_notes(12, odd_notes), "vs best", fewest_notes(12, odd_notes))
```

```
Indian notes, ₹760:  greedy 4 vs best 4
made-up notes 10/6/1, 12: greedy 3 vs best 2
```

- **`amount // note`** is how many of this note fit, and **`amount % note`** is what's left (Chapter 17). The line updates both at once: the count goes up, the amount goes down.
- **Largest note first**, always, and never reconsidered.

With real Indian notes, greedy is optimal, with or without the ₹2000 note (checked for every multiple of ₹10 up to ₹5,000). With notes of 10, 6 and 1, greedy takes 10 + 1 + 1 (three) where 6 + 6 (two) is better. **The lesson isn't about change:** it's that "take the biggest first" is a guess about the shape of the problem, and it needs checking. Greedy algorithms you'll actually meet: assigning leads to the rep with the fewest open ones, packing files into batches, picking the next job by earliest deadline.

---

## 33.9 Memory, and the other costs

Speed isn't the only resource. A list of a million rows holds a million objects; a **generator** produces them one at a time and holds one. That's **lazy evaluation**: values are produced only when something asks for them.

<!-- run: none -->
```
# terminal, in companion/ch33  (from ch33_timings.py, tracemalloc peak)
list        : 40.4 MB peak, sum 999999000000
generator   : 0.0005 MB peak, sum 999999000000
```

Same answer, 80,000 times less memory. Chapter 29's API client used the same idea with `yield from` to hand back leads page by page. Here is a generator function over the order file:

```python
import csv

def line_values(path):
    """Yields one value at a time; nothing is held except the current row."""
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield float(row["net_revenue"])

total = sum(line_values("match_data/order_lines.csv"))
biggest = max(line_values("match_data/order_lines.csv"))
print(f"total revenue {total:,.0f}, largest line {biggest:,.0f}")

squares_list = [n * n for n in range(5)]        # a list comprehension: builds everything
squares_gen = (n * n for n in range(5))         # a generator expression: builds nothing yet
print("list:", squares_list)
print("generator:", type(squares_gen).__name__, "->", list(squares_gen))
```

```
total revenue 4,421,366,900, largest line 140,000
list: [0, 1, 4, 9, 16]
generator: generator -> [0, 1, 4, 9, 16]
```

How it works:

- **`yield`** (Chapter 29) hands back one value and pauses the function until the next value is asked for. `sum` and `max` ask for values one at a time, so only one row is ever in memory.
- **The file is read twice**, once for `sum` and once for `max`, because a generator can be read only once.
- **`type(squares_gen).__name__`** is the name of the object's type, `generator`; `list(squares_gen)` then pulls all its values out.

**The trade-offs to keep in mind:**

| Choice | Costs | Saves |
|---|---|---|
| Generator instead of a list | can only be read once; no `len()` | memory, and time before the first result |
| A dictionary index | memory for the index | vastly more time |
| Caching (`lru_cache`) | memory, and staleness if inputs change | repeated computation |
| Sorting once | O(n log n) up front | linear scans afterwards |
| pandas instead of loops | memory (whole frame) and a dependency | a lot of time, through compiled code |

> **Watch out: the fastest fix is often not an algorithm at all.** Before rewriting a loop, ask whether the work should be happening in Python. Chapter 28's lesson applies: if the data is in a database, an indexed query moves the join to a system built for it. If it's in a DataFrame, a vectorized pandas operation runs in compiled code. A dictionary index is the right answer when the data is already in Python and has to stay there.

---

## 33.10 What coding interviews actually test

Analytics engineering and data engineering interviews include a coding round, usually 30 to 45 minutes on one or two problems. They are not testing whether you memorized quicksort.

**What they're looking for:**

| They want to see | How to show it |
|---|---|
| You clarify before coding | ask about size, duplicates, nulls, ordering, and what to return when nothing matches |
| You pick a sensible structure | "I'll index the orders by id in a dictionary, so the lookup is constant time" |
| You can state the complexity | "one pass to build the index, one pass over invoices: O(n + m) time, O(n) memory" |
| You write code that runs | small, named helpers; no clever one-liners |
| You test it | one normal case, one empty, one duplicate, one no-match |
| You improve it when prompted | "if the file didn't fit in memory, I'd stream it and index only the keys" |

**The patterns that come up most**, all of which are in this chapter: a hash map to avoid a nested loop; two pointers or a merge over sorted data; a set for deduplication; a counter for frequency; breadth-first or depth-first over a tree or graph; a sort followed by a linear pass.

**The sentence that earns marks:** after your first working version, say *"this is O(n²) because of the inner loop; I can make it O(n) with a dictionary"*, then do it. Interviewers care much more about that than about arriving at the optimal answer first.

Chapter 72A's Data Structures & Algorithms bank has the questions themselves (Chapter 72 has the Python ones), and Chapter 69 covers how to talk through a problem under pressure.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A lookup inside a loop (`x in a_list`) | The script slows down as the data grows, with no error | Build a `set` or `dict` before the loop |
| A loop inside a loop over the same data | Fine on a sample, hours on the real file | Index one side, then one pass over the other |
| `list.pop(0)` as a queue | Quietly quadratic | `collections.deque` |
| Re-reading or re-parsing the same file inside a loop | Disk time dominates everything | Read once into a structure |
| Recursion with no base case, or on cyclic data | `RecursionError`, or a hang | A base case, a path check, and a depth limit |
| Deep recursion on big structures | `RecursionError` at 1,000 frames | Rewrite with an explicit stack, or raise the limit deliberately |
| Mutable objects as dictionary keys | `TypeError: unhashable type` | Use tuples |
| Sorting inside a loop | O(n² log n) by accident | Sort once, before the loop |
| `sorted(...)[:3]` on millions of rows | Sorting everything to keep three | `heapq.nlargest` |
| Reading a huge file into a list | The process is killed for memory | A generator, or read in chunks |
| Caching a function whose inputs change | Stale results nobody can explain | Cache pure functions only; clear or bound the cache |
| Optimizing the wrong line | Hours spent, no change | Measure first: `time.perf_counter`, `timeit`, or a profiler |
| Reaching for an algorithm when the database should do it | A Python join over a million rows | Let SQL join, with the index from Chapter 28 |
| Quoting Big-O as if it were time | "It's O(n), so it's fast" | Big-O is growth; the stopwatch is speed |

---

## In the real world: the invoice match that ran all afternoon

Riverstone's accounts team gets one file a month from its logistics partner, which bills Riverstone for every order line it delivered to customers. Somebody has to check each billed line against the order line it bills. Priya Nambiar, an accounts executive, wrote the script two years ago, and it worked: twenty minutes, run over lunch. (The file covers the whole business, not the one-year teaching database's key accounts.)

This month it hasn't finished by four o'clock, and the month-end close needs it.

Meera reads the script. It does exactly what a careful person would write: for each invoice line, loop through the order lines until you find a match. Two years ago that was 3,000 invoices against 40,000 order lines. Today it's 20,000 against 176,000, and the work is the product of the two: **almost seven times the invoices, four and a half times the lines, about thirty times the work**.

She times the current version on a slice, rather than guessing: 2,000 invoices take about 12 seconds, so the full file is about two minutes of matching... and the script had been running for six hours. The nested loop wasn't the whole story. The script also re-read the order file *inside* the loop, so the real cost was 20,000 file reads.

The fix takes twenty minutes:

1. **Read each file once.** That alone takes the job from hours to about two minutes.
2. **Build a dictionary** keyed by `(order_id, product_id)` and look each invoice up: 0.050 seconds to build, 0.007 seconds to match all 20,000.
3. **A set of already-processed invoice ids**, so a re-sent file doesn't double-count.
4. **A generator** for reading, so next year's bigger file doesn't have to fit in memory.

The final run takes about **0.06 seconds** to index and match, inside a script that spends most of its time reading the files. Meera adds Chapter 29's tests (the counts, and one hand-checked match), and a line to the log saying how many matched and how many didn't, because the 500 unmatched invoices are the actual business output: those are the ones the logistics partner has to explain.

**What she tells the accounts manager:** *"It wasn't broken, it was written for a smaller file. It now finishes before you've finished reading the email, and it reports the 500 lines that don't match anything, which is the part you actually need."*

Notice the order she worked in: measure, find the real cost, fix the structure, then test. The clever algorithm was a dictionary, which is the first thing a Python programmer learns.

---

## Project: make the matching script fast, and prove it

**Goal:** take a working but slow script, make it fast by changing structures rather than cleverness, and measure every step.

### Tools you'll need

Versions used for this chapter, checked in September 2026:

- **Python 3.11 or later**, standard library only (outputs checked on Python 3.11.15, 3.12 and 3.13): `collections` (`deque`, `Counter`, `defaultdict`), `bisect`, `heapq`, `functools` (`lru_cache`), `time`, `timeit`, `tracemalloc`, `sys`.
- **Measuring**: `time.perf_counter()` for whole runs, `timeit` for small operations, `tracemalloc` for memory, and `cProfile` with `snakeviz` or `py-spy` when you need to find the slow line rather than confirm it.
- **When Python isn't the answer**: pandas and NumPy (Chapter 18) for vectorized work, the database (Chapter 28) for joins and aggregation over large tables, and Polars or DuckDB when a single machine has to chew through files.
- **Companion files** in `ch33/`: `generate_ch33_data.py` (176,110 order lines and 20,000 invoice lines from the logistics partner, seed 33), `match_slow.py` and `match_fast.py` (the project's before and after), and `ch33_timings.py`, which reproduces every timing in the chapter.

> **Tool note: profile before you optimize.** `python3 -m cProfile -s cumtime script.py | head -20` names the functions where the time actually goes. Analysts routinely discover that 90% of a "slow algorithm" is CSV parsing, date conversion, or a database round trip in a loop. The algorithm is what's left after the measurement, not before it.

**Option A: your own slow script.** Anything that loops over rows and looks something up. Time it before you touch it.

**Option B: Riverstone.** Start from `match_slow.py` and rebuild it yourself before comparing with `match_fast.py`. `match_slow.py` has the nested loop but reads the order file once; to see where the story's hours went, add the re-read inside the loop yourself, run it on 250 invoices, and profile it.

**Steps:**

1. **Measure first.** Time the original on 250, 500, 1,000 and 2,000 invoices. Plot or tabulate the four numbers and say what shape they are.
2. **Predict.** From those numbers, how long would the full 20,000-line file take? Write the prediction down before running it.
3. **Find the real cost.** Profile it (`cProfile`). Is the time in the comparison, in parsing, or in reading the file?
4. **Index it.** Build a dictionary keyed by `(order_id, product_id)`, and rerun. Report the build time and the match time separately.
5. **Dedupe with a set.** Ignore invoice lines you have already processed, and prove it works by running the file twice.
6. **Stream it.** Convert the reader to a generator so memory stays flat, and check with `tracemalloc`.
7. **Reconcile.** Matched plus unmatched must equal the invoice count, and the totals must agree with the slow version's. Write those as tests (Chapter 29).
8. **Report both numbers**: the time, and the 500 unmatched invoice lines, which is what the business wanted all along.

**Deliverables:** the before-and-after scripts, a table of timings at each step, the tests, and three sentences on which change mattered most.

**Stretch goals:**

- Match on `(order_id, product_id)` **and** an amount tolerance of 2%, without making the lookup linear again.
- Handle one order line billed across two invoices: what has to change, and what does the grain become?
- Do the same job in SQL (`LEFT JOIN`, Chapter 28) and in pandas (`merge`, Chapter 18), and time all three.
- Make the script handle a 5 GB file on a laptop with 8 GB of memory.

---

## Recap

- **Big-O** describes how work grows: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ). It's a shape, not a stopwatch, and quadratic is the shape that kills scripts.
- **Lists** keep order; **dictionaries** and **sets** find things in constant time; **tuples** are immutable and can be keys. The single most valuable habit in this chapter: **build an index before the loop**, which is a hand-written hash join.
- **Hashing** is why dictionary lookups don't slow down, why keys must be immutable, and how database hash joins work.
- **Stacks** are last in, first out; **queues** are first in, first out; use `collections.deque`, not `list.pop(0)`.
- **Recursion** needs a base case; Python's stack limit is 1,000 frames; use it for nested data, a loop for sequences.
- **Trees and graphs** are dictionaries of lists. **Depth-first** uses a stack, **breadth-first** uses a queue. On real data, guard them: a **seen** set for reachability, a **path** set for cycles and bills of materials.
- **Binary search** (`bisect`) is O(log n) on sorted data; **sorting** is O(n log n) and often makes everything after it easy. `heapq.nlargest` beats sorting for a top few.
- **Memoization** (`lru_cache`) turns repeated work into a lookup; **dynamic programming** fills a table of subproblems; **greedy** takes the best local step and is only sometimes right.
- **Memory** matters too: generators hold one row, lists hold all of them.
- **Measure first.** Profile, fix the real cost, and remember that the database or pandas may be the right answer instead of any algorithm.

---

## Key terms

algorithm · complexity · Big-O · constant time · logarithmic time · linear time · linearithmic · quadratic · exponential · data structure · list · dictionary · set · tuple · immutability · index (in-memory) · generator expression · hash function · hash table · bucket · collision · hash join · stack · queue · `deque` · last in first out · first in first out · retry queue · recursion · base case · recursive case · call stack · recursion limit · tree · graph · node · edge · depth-first search · breadth-first search · seen set · path set · cycle detection · nested function · linear search · binary search · `bisect` · sorting · Timsort · stable sort · sort key · heap · `heapq` · memoization · decorator · `lru_cache` · dynamic programming · subproblem · greedy algorithm · generator · lazy evaluation · profiling · `cProfile` · `timeit` · `tracemalloc` · vectorization

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can name the complexity of a loop I wrote, and say what happens when the data doubles.
- [ ] I reach for a dictionary or a set the moment I see a lookup inside a loop.
- [ ] I can say why `x in a_set` is instant and `x in a_list` isn't.
- [ ] I can explain a hash table, and connect it to a database hash join.
- [ ] I use `deque` for queues and know why `pop(0)` is a trap.
- [ ] I can write a recursive function with a base case, and say when a loop would be clearer.
- [ ] I can walk a tree depth-first and breadth-first, and choose between a seen set and a path set.
- [ ] I know what `sorted(key=...)` costs and when sorting first makes everything easier.
- [ ] I recognize memoization, dynamic programming, and greedy, and know greedy needs checking.
- [ ] I think about memory as well as time, and use generators for big files.
- [ ] I measure before optimizing, and state complexity out loud in interviews.

---

## Exercises

Work in `companion/ch33`, with the data built by `generate_ch33_data.py`. Predict each answer before running it.

### Warm-up

1. What is the complexity of each: (a) summing a list; (b) checking `x in a_dict`; (c) `sorted(rows)`; (d) a loop over invoices with `if invoice_id in processed_list` inside?
2. Count the distinct `(order_id, product_id)` pairs in the order lines file, twice: once with a list of seen pairs, once with a set. Time both on the first 20,000 rows.
3. Build a dictionary of order lines by `order_id` (not by the pair). How many orders are there, and what is the largest number of lines on one order?
4. Use `Counter` to find which products account for most of the 500 **unmatched** invoice lines. Is one product's mapping broken, or is the problem somewhere else?

### Core

5. Rewrite this quadratic snippet to run in linear time, and prove the results are identical: `[inv for inv in invoices if any(l["order_id"] == inv["order_id"] for l in order_lines)]`.
6. Write `band(amount)` with `bisect` to put order lines into size bands: tiny below ₹10,000, small from ₹10,000, medium from ₹25,000, large from ₹50,000, very large from ₹1,00,000. Test it on the boundary values exactly, and on a credit note of −500.
7. Walk the bill of materials in section 33.5 iteratively, with an explicit stack instead of recursion. Confirm you get the same quantities.
8. Find the 10 largest order lines by revenue with `sorted` and with `heapq.nlargest`, and time both on all 176,110 rows.
9. Detect whether a dictionary of dbt-style model dependencies contains a cycle, and report the cycle's members, not just that one exists.
10. Write a generator that yields only order lines above ₹50,000 from the file, and use it to compute the count and total without holding the file in memory.

### Stretch

11. Match invoices to order lines where the amount must be within 2%, without a nested loop. What does the index have to hold?
12. Implement binary search yourself (no `bisect`) and test it against `bisect_left` on 1,000 random cases, including values that aren't present.
13. Memoize a function that parses dates from strings, and measure the difference on a file with many repeated dates.
14. Use `cProfile` on `match_slow.py` with 500 invoices. Which function has the highest cumulative time, and is it the one you expected?
15. Write the fewest-notes function from section 33.8 using recursion with `lru_cache` instead of a table. Which version would you rather maintain, and are they the same complexity?

### Think about it (no code needed)

16. A colleague says "we'll just add more memory" to a script that is O(n²) in time. What do you say?
17. Your script does a database query inside a loop over 5,000 customers. Name three fixes, in order of how much they'd help.
18. When is an O(n²) algorithm perfectly acceptable?

---

## Answers

**1.** (a) O(n): every element is added. (b) O(1): one hash, one bucket. (c) O(n log n): Timsort. (d) O(n × m): the `in` on a list is itself a scan, so the whole loop is quadratic. Changing `processed_list` to a set makes it O(n), which is exercise 2's point.

**2.**

```python
import csv, time

def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

rows = load("match_data/order_lines.csv")[:20_000]

def with_list(rows):
    seen = []
    for row in rows:
        key = (row["order_id"], row["product_id"])
        if key not in seen:
            seen.append(key)
    return seen

def with_set(rows):
    return {(row["order_id"], row["product_id"]) for row in rows}

list_time = time.perf_counter()
pairs_list = with_list(rows)
list_time = time.perf_counter() - list_time
set_time = time.perf_counter()
pairs_set = with_set(rows)
set_time = time.perf_counter() - set_time

print(f"list: {len(pairs_list):,} pairs")
print(f"set:  {len(pairs_set):,} pairs")
print("same answer:", set(pairs_list) == pairs_set)
print("the set was faster by a factor of:", "hundreds" if set_time * 100 < list_time else "less than 100")
```

```
list: 20,000 pairs
set:  20,000 pairs
same answer: True
the set was faster by a factor of: hundreds
```

Same answer, and on the test machine the set version was about 940 times faster on these 20,000 rows (3.73 seconds against 0.004). The gap grows with the data, because the list version is O(n²): each `not in` scans everything found so far. On the full 176,110 rows it would take minutes; the set takes a fraction of a second.

**3.**

```python
from collections import defaultdict

all_rows = load("match_data/order_lines.csv")
by_order = defaultdict(list)
for row in all_rows:
    by_order[row["order_id"]].append(row)

largest = max(by_order, key=lambda order_id: len(by_order[order_id]))
print(f"{len(by_order):,} orders")
print(f"largest order {largest} has {len(by_order[largest])} lines")
print("lines per order:", {n: sum(1 for v in by_order.values() if len(v) == n) for n in (1, 2, 3)})
```

```
66,667 orders
largest order 100001 has 3 lines
lines per order: {1: 1003, 2: 21885, 3: 43779}
```

Grouping into a dictionary of lists is the Python version of `GROUP BY`, and it's one pass. Note the grain (Chapter 14): at most one line per order and product, so no order can have more lines than there are products. In this data no order has more than three.

**4.**

```python
from collections import Counter

invoices = load("match_data/carrier_invoice_lines.csv")
index = {(line["order_id"], line["product_id"]): line for line in all_rows}
unmatched = [invoice for invoice in invoices
             if (invoice["order_id"], invoice["product_id"]) not in index]
print(f"{len(unmatched)} unmatched invoice lines")
print("by product:", Counter(invoice["product_id"] for invoice in unmatched).most_common(3))
print("order ids from", min(i["order_id"] for i in unmatched), "to", max(i["order_id"] for i in unmatched))
```

```
500 unmatched invoice lines
by product: [('106', 74), ('104', 68), ('101', 66)]
order ids from 900065 to 999880
```

No product stands out: 500 lines over eight products is about 62 each, and the top three are only a little above that. So no single product mapping is broken. The last line shows the real problem: every unmatched line bills an order id from 900065 upwards, and Riverstone's order ids in this file run from 100000 to 166666. The logistics partner is billing orders that don't exist, which is the question to send back to them. `Counter` answered "is it one product?" in one line, and the answer was no, which is worth knowing before anyone starts fixing product codes.

**5.**

```python
order_ids = {line["order_id"] for line in all_rows}          # one pass, a set
linear = [inv for inv in invoices if inv["order_id"] in order_ids]

quadratic_sample = [inv for inv in invoices[:200]
                    if any(l["order_id"] == inv["order_id"] for l in all_rows)]
first_200_ids = {inv["invoice_line_id"] for inv in invoices[:200]}
print(f"linear version kept {len(linear):,} of {len(invoices):,} invoices")
print("same answer on the first 200:",
      [i["invoice_line_id"] for i in linear if i["invoice_line_id"] in first_200_ids]
      == [i["invoice_line_id"] for i in quadratic_sample])
```

```
linear version kept 19,500 of 20,000 invoices
same answer on the first 200: True
```

Note the set `first_200_ids`: even the check follows the chapter's rule, because `i in invoices[:200]` inside the list comprehension would scan 200 dictionaries for each of 19,500 invoices. The quadratic version is only run on 200 invoices here because the full version would take about a minute; that's the comparison worth internalizing.

**6.**

```python
from bisect import bisect_right

thresholds = [0, 10_000, 25_000, 50_000, 100_000]
labels = ["tiny", "small", "medium", "large", "very large"]

def band(amount):
    if amount < thresholds[0]:
        raise ValueError(f"negative amount {amount}")
    return labels[bisect_right(thresholds, amount) - 1]

for amount in (0, 9_999, 10_000, 24_999, 25_000, 100_000, 100_001, -500):
    try:
        print(f"{amount:>8,}: {band(amount)}")
    except ValueError as exc:
        print(f"{amount:>8,}: ValueError: {exc}")
```

```
       0: tiny
   9,999: tiny
  10,000: small
  24,999: small
  25,000: medium
 100,000: very large
 100,001: very large
    -500: ValueError: negative amount -500
```

Boundaries are where banding bugs live: `bisect_right` puts a value *equal* to a threshold into the higher band, which matches "from ₹10,000". If the rule is "over ₹10,000", `bisect_left` is the one you want, but then 0 falls before the first threshold and index −1 silently wraps to the last label: negative indexes are the trap, so guard the low end. Write the test with the boundary values, not with 9,500 and 30,000.

**7.**

```python
parts = {
    "Garden Chair": [("Seat shell", 1), ("Steel frame", 1),
                     ("Product label", 1), ("Shipping carton", 1)],
    "Seat shell": [("PP granules", 2.2), ("Masterbatch", 0.08)],
    "Steel frame": [("Leg assembly", 2), ("Steel tube", 1.0), ("Fastener pack", 1)],
    "Leg assembly": [("Steel tube", 1.2), ("Fastener pack", 1)],
}

def explode_iterative(part, quantity=1.0):
    totals, stack = {}, [(part, quantity)]
    while stack:
        current, current_quantity = stack.pop()
        if current not in parts:
            totals[current] = totals.get(current, 0) + current_quantity
            continue
        for child, child_quantity in parts[current]:
            stack.append((child, current_quantity * child_quantity))
    return totals

for material, amount in sorted(explode_iterative("Garden Chair").items()):
    print(f"{material:<16} {amount:>6.2f}")
```

```
Fastener pack      3.00
Masterbatch        0.08
PP granules        2.20
Product label      1.00
Shipping carton    1.00
Steel tube         3.40
```

Identical to the recursive version, because the stack *is* what recursion was using. The iterative form has no depth limit, which matters for deep structures; the recursive form is shorter to read. Choose per structure, and say which you chose in a code review.

**8.**

```python
import heapq, time

values = [(float(row["net_revenue"]), row["order_id"]) for row in all_rows]

started = time.perf_counter()
top_sorted = sorted(values, reverse=True)[:10]
sort_time = time.perf_counter() - started

started = time.perf_counter()
top_heap = heapq.nlargest(10, values)
heap_time = time.perf_counter() - started

print("same answer:", top_sorted == top_heap)
print("largest line:", top_sorted[0])
print("nlargest was quicker:", heap_time < sort_time)
```

```
same answer: True
largest line: (140000.0, '166653')
nlargest was quicker: True
```

On the test machine that was 0.048 seconds against 0.006. `sorted` orders all 176,110 values to keep 10; `nlargest` keeps a heap of 10 and scans once. The gap widens as the data grows and narrows as *k* approaches n; for k near n, just sort.

**9.**

```python
models = {"stg_orders": [], "fct_sales": ["stg_orders", "dim_customer"],
          "dim_customer": ["snapshot"], "snapshot": ["fct_sales"]}

def find_cycle(graph):
    done = set()
    def visit(node, path):
        if node in path:
            return path[path.index(node):] + [node]
        if node in done:
            return None
        for neighbor in graph.get(node, []):
            found = visit(neighbor, path + [node])
            if found:
                return found
        done.add(node)
        return None
    for node in graph:
        found = visit(node, [])
        if found:
            return found
    return None

print("cycle:", " -> ".join(find_cycle(models)))
```

```
cycle: fct_sales -> dim_customer -> snapshot -> fct_sales
```

Carrying the path as a list, in order, rather than a bare set is what lets you report the members: `path.index(node)` finds where the loop starts, and the slice from there is the cycle. The `done` set keeps it O(V + E), as in section 33.6. Naming the members is what makes the error useful, which is why dbt's own message for a circular `ref` lists the models in the loop, and why Chapter 28's `CYCLE` clause keeps the path in SQL.

**10.**

```python
import csv

def big_lines(path, floor=50_000):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            value = float(row["net_revenue"])
            if value > floor:
                yield value

count = total = 0
for value in big_lines("match_data/order_lines.csv"):
    count += 1
    total += value
print(f"{count:,} lines above 50,000, worth {total:,.0f}")
```

```
25,133 lines above 50,000, worth 2,175,373,500
```

One row is in memory at a time, so this works on a file of any size. The trade: the generator can be read only once, so computing a count and a total means either two passes or accumulating both in one loop, as here.

**11.** The index can't be keyed on the amount, because the tolerance makes it a range rather than a value. Key it on `(order_id, product_id)` as before, and check the invoice's `amount` against the order line's `net_revenue` *after* the lookup:

<!-- run: none -->
```python
line = index.get((invoice["order_id"], invoice["product_id"]))
if line is not None and abs(float(invoice["amount"]) - float(line["net_revenue"])) <= 0.02 * float(line["net_revenue"]):
    ...
```

The lookup stays O(1) and the tolerance is one comparison. If you had to match on amount *alone*, sort the lines by amount once and use `bisect` to find the window, which is O(log n) per invoice: the general lesson is that exact matches want a hash, and range matches want sorted data.

**12.**

```python
from bisect import bisect_left
import random

def my_bisect_left(values, target):
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low

numbers = sorted(random.Random(33).sample(range(1_000_000), 5_000))
rng = random.Random(34)
tests = [rng.randrange(1_000_000) for _ in range(1_000)]
tests += [numbers[0], numbers[-1], -1, 1_000_000, numbers[100]]   # first, last, below, above, present
print("distinct test values:", len(set(tests)))
print("matches bisect_left on every case:",
      all(my_bisect_left(numbers, t) == bisect_left(numbers, t) for t in tests))
print("example:", my_bisect_left(numbers, numbers[100]), bisect_left(numbers, numbers[100]))
```

```
distinct test values: 1002
matches bisect_left on every case: True
example: 100 100
```

Create the random generator once: `random.Random(34)` inside the loop would restart the same sequence every time, so all 1,000 "random" cases would be the same number, a classic testing bug. The two traps when writing binary search by hand are the loop condition (`<` against `<=`) and the update (`middle + 1` against `middle`), which is why the test includes values that aren't in the list and both ends of it.

**13.** Wrap the parser in `@lru_cache` and call it on a column with many repeats:

```python
from datetime import date
from functools import lru_cache

@lru_cache(maxsize=None)
def parse_date(text):
    year, month, day = (int(part) for part in text.split("-"))
    return date(year, month, day)

dates = [row["order_date"] for row in all_rows]
parsed = [parse_date(text) for text in dates]
info = parse_date.cache_info()
print(f"{len(dates):,} values, {len(set(dates)):,} distinct")
print(f"cache hits {info.hits:,}, misses {info.misses:,}")
print("earliest:", min(parsed), "latest:", max(parsed))
```

```
176,110 values, 700 distinct
cache hits 175,410, misses 700
earliest: 2024-01-01 latest: 2025-11-30
```

700 distinct dates in 176,110 rows, so the cache answers 99.6% of the calls. This is the shape of case where `lru_cache` is worth it: a pure function, expensive relative to a dictionary lookup, called repeatedly with few distinct inputs. It would be worth nothing if every value were unique.

**14.** Run `python3 -m cProfile -s cumtime match_slow.py 500 | head -15`. The highest cumulative time is `match`, as expected, but look at the next lines: on this data the comparisons themselves dominate, while `load` and `csv.DictReader` account for a fraction of the run. That's the useful outcome either way: profiling either confirms your suspicion (fix the algorithm) or overturns it (fix the parsing, the file reading, or the database calls), and guessing is often wrong.

**15.**

```python
from functools import lru_cache

NOTES = (2000, 500, 200, 100, 50, 20, 10)

@lru_cache(maxsize=None)
def fewest_recursive(amount):
    if amount == 0:
        return 0
    options = [fewest_recursive(amount - note) for note in NOTES if note <= amount]
    options = [o + 1 for o in options if o is not None]
    return min(options) if options else None

for amount in (760, 2750, 45):
    print(f"₹{amount:>5}: {fewest_recursive(amount)}")
```

```
₹  760: 4
₹ 2750: 4
₹   45: None
```

Same answers, same complexity: with the cache, each amount is solved once, which is precisely what the table version did. The recursive version reads closer to the definition of the problem; the table version has no recursion limit to worry about and is easier to reason about for large amounts. Most teams take the recursive one for clarity and add a comment saying why the cache is there.

**16.** Memory isn't the constraint; time is. Doubling the memory does nothing for an algorithm whose *work* is quadratic, and the job will keep getting slower as the data grows. Say it in terms of growth: *"this takes four times as long each time our data doubles, so if it takes an hour today, next year it takes four hours, not two. Changing the lookup to a dictionary makes it linear, and it's twenty minutes of work."* If it really is memory-bound rather than time-bound, that's a different conversation, and a generator is usually cheaper than more hardware.

**17.** In order: (1) **Do it in one query.** Fetch all 5,000 customers' rows in a single statement with `WHERE customer_id IN (...)` or a join, then index the result in Python. That removes 4,999 round trips. (2) **Push the work into SQL entirely.** If the loop is computing something the database could compute, let it (Chapter 28). (3) **If the loop must stay, batch it**: 50 queries of 100 ids beat 5,000 of one. A fourth, only if the first three aren't available: cache repeated lookups. Network round trips inside loops are the single most common performance bug in analyst code, and they don't show up in a Big-O count at all.

**18.** When n is small and stays small: ranking ten regions, comparing eight products, reconciling two dozen accounts. When it runs once, by hand, and finishing in a minute is fine. When the quadratic version is plainly correct and the linear one would need an index that complicates the code for a file that will never grow. The judgment is about **n and its future**, not about the notation: write the simple version, measure it on real data, and change it when the measurement says so.

---

## Where this leads

- **Chapter 35, The Math Under the Models,** does whole-matrix arithmetic in NumPy, the vectorized style this chapter's first Watch out describes, and shows why it beats a loop.
- **Chapter 46, Pipelines & Orchestration,** and **Chapter 49, Storage, Warehouses & Lakehouses,** are where these costs meet scheduled jobs and cloud bills.
- **Chapter 48, Big Data & Distributed Compute,** splits data into partitions across machines; its broadcast join is this chapter's dictionary index, copied to every machine.
- **Chapter 55, Building AI Applications,** builds a search index over documents, where the same trade of memory for lookup speed decides how retrieval scales.
- **Chapter 72A, Data Structures & Algorithms Question Bank,** has the coding questions (Chapter 72 has the Python and pandas ones); **Chapter 69** covers how to talk through them.

**Looking back:** Chapter 28 is the database version of this chapter (indexes are hash tables and B-trees, and a hash join is section 33.2's dictionary); Chapter 29 is how a fast script becomes a maintained one; and Chapter 18's pandas covers the vectorized alternatives that often beat any loop you could write.
