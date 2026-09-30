# Chapter 72A. Data Structures & Algorithms Question Bank

*Part 8 — The Interview Playbook*

> **Chapter at a glance**
>
> **You will practise:** answering the core data structures and algorithms (DSA) questions that come up in data-role interviews, sized for those roles rather than a full software-engineering gauntlet · reasoning about time and space (Big-O) out loud, and backing the claim with a measurement · implementing and explaining the handful of structures and patterns that actually recur: hash maps and sets, two pointers and sliding windows, recursion and memoization, sorting and searching, linked lists, trees, and graphs.
>
> **Before you start:** **do Chapter 33 first** (The Computer Science You Actually Need): it teaches almost every idea in this bank. You also need Chapter 17 (Python from zero), Chapter 29, section 29.5 (writing a class with `__init__` and `self`), and Chapter 69 (the three answer tiers and the twelve extra-point tags). Chapter 72's Python gotchas (mutable defaults, `is` versus `==`) come back here twice.
>
> **Time needed:** 6–8 hours to run every snippet and answer each question aloud; 1 hour for a revision pass. Add 3–4 hours if the Chapter 33 sections named in the Learn-it-in lines are new to you.
>
> **How this chapter is built.** Same format as the other question banks in Part 8: every core question leads with a **"Remember it as…"** hook, then a one-line answer, then a compact tier table (what **passes**, what's **strong**, and the **extra points**, tagged with Chapter 69's moves: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Rapid-fire sections are scan tables. **Every snippet was run, and every output shown is real**, on Python 3.11.15 with the standard library only; the book recommends Python 3.14 (Chapter 17, section 17.0), and none of these outputs depend on the version. Timings change on every run and every machine, so the cells that print them say so; run them yourself in a notebook (Chapter 17 set one up) and expect your numbers to differ, not the pattern.
>
> **Learn it in** pointers name the chapter and section that teach each idea. Four topics go beyond Chapter 33: the two-pointer and sliding-window patterns, merge sort, linked lists, and binary search trees. Those questions are marked **Beyond the book** and carry a short primer you can learn from before the question itself.

---

## 72A.1 Why data roles get asked this at all

Not every data role gets a DSA round. A Data Analyst or BA interview rarely does. A Data Engineer or ML Engineer interview, especially at a larger tech company, very often does, because the underlying skill (can you reason precisely about how a solution scales) is exactly what separates "a pipeline that works on the sample data" from "a pipeline that survives production volume." The bar is usually lower than a pure software-engineering interview: fewer obscure edge cases, more emphasis on getting a correct, reasonably efficient solution and explaining your reasoning clearly (Chapter 69's moves apply here as much as anywhere else in this part). Chapter 33, section 33.10 describes what that round looks like; this bank is the practice.

**Levels and roles.** Each question carries a level and the roles that usually ask it:

- **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds.
- **DE** data engineer · **AE** analytics engineer · **MLE** machine learning engineer · **DS** data scientist · **DA** data analyst.

Within each section the core questions run from easier to harder. If a DSA round is on your calendar for a first job, do every Fresher question first, then come back for the Mid ones.

---

## 72A.2 Big-O: reasoning about time and space

### Q72A-001 · Explain Big-O notation to someone who's never seen it

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *Big-O answers one question: if the input doubles, does the work stay the same, double, or explode?*

**Answer in one line:** Big-O describes how an algorithm's running time (or memory use) grows as the input size grows, ignoring constant factors and keeping only the dominant term as the input gets large.

**The common orders, cheapest to most expensive:**

| Order | Name | Example | Steps for 5,000 items |
|---|---|---|---|
| O(1) | Constant | Dictionary lookup, list index access | 1 |
| O(log n) | Logarithmic | Binary search | 13 |
| O(n) | Linear | A single loop through the data | 5,000 |
| O(n log n) | Linearithmic | Merge sort, Python's `sorted()` | 61,439 |
| O(n²) | Quadratic | A loop inside a loop over the same data | 25,000,000 |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci, trying every subset | 2⁵⁰⁰⁰, a 1,506-digit number: never finishes |

The last column is plain arithmetic, and worth being able to do yourself:

```python
import math

n = 5_000
print(f"O(log n):   {math.ceil(math.log2(n))} steps")
print(f"O(n):       {n:,} steps")
print(f"O(n log n): {n * math.log2(n):,.0f} steps")
print(f"O(n^2):     {n * n:,} steps")
```

```
O(log n):   13 steps
O(n):       5,000 steps
O(n log n): 61,439 steps
O(n^2):     25,000,000 steps
```

- **`math`** is the standard library's maths module; **`math.log2(n)`** answers "how many times can you halve `n` before you reach 1?" (logarithms: Chapter 31, section 31.0). For 5,000 that's 12.3, so a binary search needs at most 13 looks; **`math.ceil`** rounds up to the next whole number.
- **`{…:,}`** and **`{…:,.0f}`** are the f-string formats from Chapter 17: thousands separators, and no decimals.

| Tier | What to say |
|---|---|
| Passes | "It's how fast an algorithm is" |
| Strong | + names the common orders (above) and what each looks like in code: one loop is O(n), a loop inside a loop over the same data is O(n²) |
| Extra points | **[+Business]** ties complexity to a real cost: an O(n²) report that's fine on 100 test rows can time out on 5 million production rows. **[+Edge cases]** Big-O is an upper bound on growth; unless you say otherwise, people assume you mean the worst case. Say "average case" explicitly when you mean it (a dictionary lookup is O(1) on average, Q72A-003) |

**Likely follow-ups:** What's the difference between time and space complexity? What's amortized complexity (Q72A-006)? Best case versus worst case for quicksort (Q72A-020)?
**Red flag:** confusing Big-O with measured runtime; can't name what O(n²) looks like in code.
**Learn it in:** Chapter 33, section 33.1 (and Chapter 48 for the same instinct at distributed scale).

### Q72A-002 · Live demonstration: why the nested-loop duplicate check is dangerous

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *A nested loop over the same array is O(n²) hiding in plain sight. A set turns it into O(n).*

**Answer in one line:** Comparing every element with every later one is O(n²); remembering what you've seen in a set, whose membership check is O(1) on average, does the same job in one O(n) pass.

The two versions:

```python
def has_dup_On2(arr):          # O(n^2): compares every pair
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

def has_dup_On(arr):           # O(n): one pass, a set remembers what's been seen
    seen = set()
    for x in arr:
        if x in seen:
            return True
        seen.add(x)
    return False
```

- **`has_dup_On2`**: the outer loop picks position `i`; the inner loop starts at `i + 1`, so each pair is compared once, never an element with itself. It returns `True` at the first match.
- **`has_dup_On`**: one loop. `x in seen` asks the set, not a scan (Chapter 33, section 33.3 shows why that's instant); `seen.add(x)` records `x` for later.

Now some test data: 5,000 different whole numbers, so neither version can stop early (the worst case for both).

```python
import random

random.seed(72)
data = random.sample(range(10_000_000), 5_000)
print(len(data), len(set(data)))
print(has_dup_On2(data), has_dup_On(data))
print(has_dup_On2(data + [data[0]]), has_dup_On(data + [data[0]]))
```

```
5000 5000
False False
True True
```

- **`random.seed(72)`** fixes the random generator's starting point, so you get the same 5,000 numbers every time you run it.
- **`random.sample(range(10_000_000), 5_000)`** draws 5,000 *different* numbers from 0 to 9,999,999. `len(set(data))` is 5,000 too, which proves there are no duplicates.
- The last line adds a copy of the first number at the end; both functions now find the duplicate. Always check that the fast version gives the *same answer* before you time it.

How many comparisons does the slow version make on the unique data? Each pair once:

```python
n = len(data)
print(f"{n * (n - 1) // 2:,} comparisons, against n squared = {n * n:,}")
```

```
12,497,500 comparisons, against n squared = 25,000,000
```

That's n(n−1)/2, about 12.5 million: half of n², and still O(n²), because Big-O drops the ½. The table in Q72A-001 counts every ordered pair (25 million); the shape is the same.

Now time them, at 2,500 and at 5,000 items. Timings change on every run and every machine, so this cell's numbers will differ on yours:

<!-- run: none -->
```python
import time

def seconds(func, arr):
    start = time.perf_counter()
    func(arr)
    return time.perf_counter() - start

for size in (2_500, 5_000):
    sample = data[:size]
    slow = seconds(has_dup_On2, sample)
    fast = seconds(has_dup_On, sample)
    print(f"n={size:,}: O(n^2) {slow:.4f} s   O(n) {fast:.6f} s   {slow / fast:,.0f}x")
```

```
n=2,500: O(n^2) 0.0719 s   O(n) 0.000183 s   393x
n=5,000: O(n^2) 0.2871 s   O(n) 0.000679 s   423x
```

- **`seconds(func, arr)`** runs any function once on `arr` and returns how long it took, using `time.perf_counter()`, Chapter 18's stopwatch. Passing a function as an argument (`has_dup_On2`, with no brackets) hands over the function itself, not its result.
- **`data[:size]`** takes the first 2,500 or 5,000 numbers.
- Read the two rows against each other: doubling n multiplied the O(n²) time by four (0.0719 s to 0.2871 s), the measured shape of a quadratic, and a stronger answer than one speedup number. The O(n) times stay under a millisecond, too small for a single run to time precisely.

| Tier | What to say |
|---|---|
| Passes | "Use a set instead of nested loops" |
| Strong | + explains *why*: `x in seen` is O(1) on average, versus scanning the rest of the array for every element |
| Extra points | **[+Validate]** the timings above, on real data, with the answers checked equal first; doubling n quadruples the slow version. **[+Business]** checking for duplicate customer IDs or order IDs is everyday data cleaning, and on millions of rows the O(n²) version doesn't finish in any reasonable time |

**Likely follow-ups:** What's the trade-off (a set uses more memory)? What if the input needs to stay in its original order?
**Red flag:** reaching for nested loops as a first instinct without considering a hash-based structure.
**Learn it in:** Chapter 33, sections 33.1 (the measured curves) and 33.2 (list versus set, timed).

### Rapid-fire, 72A.2

Roles: DE, AE, MLE and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q72A-003 | Complexity of a dictionary (hash map) lookup? | O(1) on average | **[+Edge cases]** worst case is O(n) if almost every key collides; rare in practice with a good hash function | Fresher · 33.3 |
| Q72A-004 | Complexity of Python's built-in `sort()`? | O(n log n) | **[+Edge cases]** it's Timsort, which is O(n) on data that's already sorted | Fresher · 33.7 |
| Q72A-005 | Time versus space trade-off, one example? | Memoization (see Q72A-018 below) spends memory on a cache to avoid repeated work | **[+Business]** it isn't free: caching everything can exhaust memory | Mid · 33.8, 33.9 |
| Q72A-006 | What's amortized complexity, in one example? | Appending to a Python list is O(1) amortized: an occasional append copies the list into bigger storage (O(n)), but so rarely that the average per append stays constant | **[+Edge cases]** "amortized" is an average over many operations; any single call can still be slow | Mid · 33.1 |

---

## 72A.3 Arrays, strings, and the two-pointer / sliding-window patterns

**Beyond the book: two pointers and sliding windows.** Chapter 33, section 33.10 names both patterns; here is what they are. A **pointer** here is just a position in a list, held in a variable such as `l` or `r`. The **two-pointer** pattern keeps two positions and moves them towards each other (or both forwards) by a rule, so one pass does the job a pair of nested loops would. The **sliding-window** pattern keeps a running total for a fixed-width stretch of the list, the **window**, and moves it one place at a time: add the item that comes in, subtract the item that falls out, instead of adding the whole window up again. Q72A-008 and Q72A-009 trace each one step by step.

### Q72A-007 · Find two numbers in an array that sum to a target (Two Sum)

**Level:** Fresher · **Roles:** DE, AE, MLE, DS

**Remember it as:** *"What number would complete this?": check a hash map before you check the rest of the array.*

**Answer in one line:** Loop once, and at each element check whether `target - element` has already been seen; a dictionary turns an O(n²) check of every pair into a single O(n) pass.

```python
def two_sum(nums, target):
    seen = {}                       # value -> the position where we saw it
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return None

print(two_sum([2, 7, 11, 15], 9))
print(two_sum([2, 7, 11, 15], 100))
```

```
[0, 1]
None
```

- **`enumerate(nums)`** (Chapter 17, section 17.6) gives each value with its position.
- **`target - n in seen`** asks "have I already met the number that completes this one?" It's a dictionary lookup, O(1) on average; this is Chapter 33's dictionary index in miniature.
- **`seen[n] = i`** is stored *after* the check, so an element is never paired with itself.
- No pair adds up to 100, so the loop finishes and the function returns `None`.

| Tier | What to say |
|---|---|
| Passes | Nested loop checking every pair (O(n²), correct, not the answer they want) |
| Strong | The dictionary version above, O(n) time, O(n) space |
| Extra points | **[+Clarify]** ask whether the array is sorted: if so, two pointers from both ends work in O(1) extra space. **[+Edge cases]** no valid pair (the `None` above), or several: which should be returned? **[+Trade-offs]** the dictionary version is faster but uses O(n) extra memory; the two-pointer version uses O(1) extra memory but needs sorted data, and sorting costs O(n log n) |

**Likely follow-ups:** What if you need all pairs, not just one? What if the array is sorted? Three Sum instead of two?
**Red flag:** jumping straight to nested loops with no mention of the hash-map alternative.
**Learn it in:** Chapter 33, sections 33.2 (the dictionary index) and 33.10 (the patterns).

### Q72A-008 · Check whether a string is a palindrome

**Level:** Fresher · **Roles:** DE, AE, MLE, DS · **Beyond the book** (the two-pointer pattern)

**Remember it as:** *Two pointers walking toward each other from both ends: stop the moment they disagree.*

**Answer in one line:** Compare the first and last characters, then the second and second-to-last, and so on inwards; any mismatch means no, and meeting in the middle means yes.

```python
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True

print(is_palindrome("racecar"), is_palindrome("hello"), is_palindrome(""))
```

```
True False True
```

- **`l, r = 0, len(s) - 1`** puts one pointer on the first character and one on the last.
- **`while l < r`** keeps going until the pointers meet or cross; each step moves `l` right and `r` left.
- The empty string never enters the loop, so it counts as a palindrome.

Here is the walk for "racecar", printed by the same loop:

```python
s = "racecar"
l, r = 0, len(s) - 1
while l < r:
    print(f"l={l} r={r}  {s[l]} vs {s[r]}  {'same' if s[l] == s[r] else 'different'}")
    l += 1
    r -= 1
print(f"l={l} r={r}  pointers met: palindrome")
```

```
l=0 r=6  r vs r  same
l=1 r=5  a vs a  same
l=2 r=4  c vs c  same
l=3 r=3  pointers met: palindrome
```

- **`{'same' if s[l] == s[r] else 'different'}`** is a one-line `if` inside the f-string: it prints *same* when the two characters match and *different* when they don't.
- The last `print` runs once the loop ends, showing where the pointers met.

Three comparisons for seven letters: the middle `e` never needs checking.

| Tier | What to say |
|---|---|
| Passes | Reverse the string and compare (`s == s[::-1]`): correct, O(n) extra space for the reversed copy |
| Strong | The two-pointer version above: O(1) extra space, same O(n) time, no copy needed |
| Extra points | **[+Clarify]** capitals, spaces and punctuation ("A man, a plan, a canal: Panama") need normalizing first; ask whether that's in scope. **[+Trade-offs]** the O(1)-space version matters on huge strings; on interview-sized ones the slicing version is fine and clearer, so say you know both |

**Likely follow-ups:** Ignore case and punctuation? Longest palindromic substring instead?
**Red flag:** not knowing the two-pointer alternative to slicing and reversing.
**Learn it in:** Beyond the book (the primer at the start of this section); slicing and `while`: Chapter 17, sections 17.4 and 17.6.

### Q72A-009 · Maximum sum of any contiguous subarray of size k

**Level:** Mid · **Roles:** DE, AE, MLE, DS · **Beyond the book** (the sliding-window pattern)

**Remember it as:** *Don't recompute the whole window every time: slide it. Subtract what falls out, add what comes in.*

**Answer in one line:** Summing every window from scratch is O(n·k); a sliding window that updates the running sum (minus the element leaving, plus the element entering) is O(n).

```python
def max_sum_subarray(arr, k):
    window = sum(arr[:k])
    best = window
    for i in range(k, len(arr)):
        window += arr[i] - arr[i - k]
        best = max(best, window)
    return best

print(max_sum_subarray([2, 1, 5, 1, 3, 2], 3))
```

```
9
```

- **`window = sum(arr[:k])`** adds up the first window, positions 0 to k−1, once.
- **`for i in range(k, len(arr))`**: `arr[i]` is the item coming into the window and `arr[i - k]` the one falling out, so one addition and one subtraction move the window along.
- **`best = max(best, window)`** keeps the largest total seen so far.

The same loop, printing each step:

```python
arr, k = [2, 1, 5, 1, 3, 2], 3
window = sum(arr[:k])
best = window
print(f"start: window {arr[:k]} sum {window}, best {best}")
for i in range(k, len(arr)):
    window += arr[i] - arr[i - k]
    best = max(best, window)
    print(f"i={i}: +{arr[i]} -{arr[i - k]}  sum {window}, best {best}")
```

```
start: window [2, 1, 5] sum 8, best 8
i=3: +1 -2  sum 7, best 8
i=4: +3 -1  sum 9, best 9
i=5: +2 -5  sum 6, best 9
```

The best window is 5, 1, 3, found at `i=4`. One trap the function doesn't guard against:

```python
print(max_sum_subarray([1, 2], 3))
```

```
3
```

With k bigger than the list, `arr[:k]` quietly returns the whole short list, the loop never runs, and the function answers 3 for a window of size 3 that doesn't exist.

| Tier | What to say |
|---|---|
| Passes | Recompute the sum of each window of size k from scratch: correct, O(n·k) |
| Strong | The sliding-window version above, O(n), with the trace to show it |
| Extra points | **[+Edge cases]** guard with `if k <= 0 or k > len(arr): return None`, otherwise a short list returns a sum of fewer than k items, as the last cell shows. **[+Signpost]** the same subtract-outgoing, add-incoming idea handles a whole family of window problems, not just sums. **[+Business]** this is a trailing-window calculation, the idea behind a moving average, written as raw list logic instead of pandas' `.rolling()` |

**Likely follow-ups:** What if k varies (a variable-size window)? Maximum item rather than sum? The shortest window that contains every character of a given set?
**Red flag:** recomputing the full window sum every step with no mention of the sliding update.
**Learn it in:** Beyond the book (the primer at the start of this section); Chapter 40, section 40.6 for the same trailing window with `.rolling()`.

### Rapid-fire, 72A.3

Roles: DE, AE, MLE and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q72A-010 | Reverse an array in place? | Two pointers from each end: swap, move both inwards; O(n) time, O(1) space | **[+Edge cases]** odd length: the middle element never needs swapping, and the loop handles it | Fresher · primer above |
| Q72A-011 | Find the missing number in a range 1 to n? | The sum of 1..n, n(n+1)/2, minus the actual sum of the array; O(n) time, O(1) space | **[+Trade-offs]** a set-based approach also works but uses O(n) extra space; the sum trick doesn't | Fresher · 33.2 |
| Q72A-012 | Merge two sorted arrays into one sorted array? | Two pointers, one per array; always take the smaller current element; O(n + m) | **[+Business]** this merge step is the core of merge sort (see Q72A-020 below) and of merging two sorted feeds | Mid · 33.7, primer above |
| Q72A-013 | Group anagrams from a list of strings? | A dictionary keyed by each string's sorted letters; strings with the same key are anagrams | **[+Edge cases]** sorting each string's letters costs O(k log k) per string; a tuple of 26 letter counts as the key avoids that sort | Mid · 33.2 |

---

## 72A.4 Hash maps and sets

### Q72A-014 · When would you reach for a set instead of a list, and why does it matter?

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *"Is X in here?": a list checks every element one by one; a set asks the hash table directly.*

**Answer in one line:** A set's membership check (`x in my_set`) is O(1) on average; a list's is O(n), because it scans element by element: the mechanism behind Q72A-002's speedup.

Sets have one rule a list doesn't: everything in them must be **hashable** (Chapter 33, section 33.3).

```python
print({(1, 2), (1, 2), (3, 4)})
try:
    {(1, [2])}
except TypeError as exc:
    print("TypeError:", exc)
```

```
{(1, 2), (3, 4)}
TypeError: unhashable type: 'list'
```

- The first set keeps one copy of `(1, 2)`: sets drop duplicates.
- **`try:` … `except TypeError as exc:`** (Chapter 17, section 17.10) runs the risky line, and if it raises a `TypeError`, prints the error's message (`exc`) instead of stopping.
- A tuple of numbers is hashable, so it can go in a set. A tuple *containing a list* isn't, because the list inside could change, and Python refuses it.

| Tier | What to say |
|---|---|
| Passes | "Sets are faster for checking if something exists" |
| Strong | + explains the O(1) versus O(n) mechanism, and that sets don't keep order or allow duplicates |
| Extra points | **[+Business]** deduplicating a customer or order list, and checking "has this ID been processed already", are the two most common reasons to reach for a set in data work. **[+Edge cases]** set elements must be hashable: a list or dict can't go in a set, and a tuple can only if everything inside it is hashable too (the `TypeError` above) |

**Likely follow-ups:** Set versus dictionary: when do you need one over the other? What makes something "hashable" (Q72A-015)?
**Red flag:** not knowing why the membership check is faster, just that "sets are faster".
**Learn it in:** Chapter 33, sections 33.2 (list versus set, timed) and 33.3 (hashing).

### Rapid-fire, 72A.4

Roles: DE, AE, MLE and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q72A-015 | What makes an object hashable in Python? | It has a working `__hash__`, and its hash never changes while it's in a set or used as a key. Built-in immutable values (str, int, a tuple of hashable values) qualify; list, dict and set don't. Instances of a plain class hash by identity (Q72A-026 uses that) | **[+Edge cases]** two equal objects must produce the same hash, or a set or dict silently misbehaves | Mid · 33.3 |
| Q72A-016 | Find the first non-repeating character in a string? | Count every character in one pass (`Counter`), then a second pass returns the first with count 1 | **[+Trade-offs]** two O(n) passes; a single-pass version is possible but usually less readable | Fresher · 33.2 |
| Q72A-017 | Count the frequency of every word in a large text? | A dictionary, or `collections.Counter`, in one pass: O(n) | **[+Business]** it's the same counting that builds Chapter 41's bag of words (section 41.3) | Fresher · 33.2 |

---

## 72A.5 Recursion and memoization

### Q72A-018 · Fibonacci, naive recursion versus memoized, and why the difference is so dramatic

**Level:** Mid · **Roles:** DE, MLE, DS

**Remember it as:** *Naive recursive Fibonacci recomputes the same small answers hundreds of thousands of times. Memoization is just "remember what you already solved."*

**Answer in one line:** The naive version calls itself twice per call and solves the same subproblems over and over, O(2ⁿ); caching each answer the first time it's computed makes it O(n).

The naive version, with one extra line that counts how often each `n` is computed:

```python
from collections import Counter

calls = Counter()

def fib_naive(n):
    calls[n] += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

print(fib_naive(28))
print(f"{sum(calls.values()):,} calls; fib(2) was computed {calls[2]:,} times")
```

```
317811
1,028,457 calls; fib(2) was computed 196,418 times
```

- **`calls[n] += 1`** counts one more call for this `n`; a `Counter` starts every key at 0 (Chapter 33, section 33.2).
- **`if n <= 1: return n`** is the base case; the last line is the recursive case, which calls the function twice.
- Over a million calls to get one number, and `fib(2)` alone was worked out nearly 200,000 times. That duplicated work is the whole problem.

The memoized version, with the cache Python has built in:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

print(fib_memo(28))
print(fib_memo.cache_info())
```

```
317811
CacheInfo(hits=26, misses=29, maxsize=None, currsize=29)
```

- **`@lru_cache(maxsize=None)`** (Chapter 33, section 33.8) wraps the function so each call first looks up its argument in a dictionary of past results, and only runs the body for an `n` it hasn't seen. `maxsize=None` means it never forgets.
- **`cache_info()`** reports the work: 29 **misses** (each `n` from 0 to 28 computed once) and 26 **hits** (answers reused). Fifty-five calls instead of 1,028,457.

Now time both. Timings change on every run and every machine:

<!-- run: none -->
```python
import time

start = time.perf_counter()
fib_naive(28)
naive_s = time.perf_counter() - start

fib_memo.cache_clear()          # start with an empty cache, or the timing is a pure lookup
start = time.perf_counter()
fib_memo(28)
memo_s = time.perf_counter() - start

print(f"naive: {naive_s:.4f} s   memoized: {memo_s:.6f} s   {naive_s / memo_s:,.0f}x")
```

```
naive: 0.1383 s   memoized: 0.000018 s   7,485x
```

- **`start = time.perf_counter()`** reads the stopwatch before each call, and `time.perf_counter() - start` after it gives the seconds taken, stored as `naive_s` and `memo_s`.
- **`cache_clear()`** empties the cache first; without it, the second call would find `fib_memo(28)` already stored and time a single lookup. The naive version still has its counting line, which slows it a little, but the ratio would be in the thousands without it too, and it widens fast as `n` grows, since one version is O(2ⁿ) and the other O(n).

The memoized version still recurses `n` calls deep, and Python allows about 1,000:

```python
fib_memo.cache_clear()
try:
    fib_memo(1500)
except RecursionError:
    print("RecursionError: fib_memo(1500) needs 1,500 calls at once")
```

```
RecursionError: fib_memo(1500) needs 1,500 calls at once
```

- **`try` / `except RecursionError`** (Chapter 17, section 17.10) catches the error and prints a line of our own. Python's own message starts "maximum recursion depth exceeded", as in Chapter 33, section 33.5; its ending varies with where the limit is hit, so the cell prints its own words instead.

That's the practical reason for the **bottom-up** version, which builds the answer from `fib(0)` upwards in a loop and keeps only the last two numbers:

```python
def fib_bottom_up(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib_bottom_up(28))
print(len(str(fib_bottom_up(1500))), "digits, no recursion")
```

```
317811
314 digits, no recursion
```

- **`a, b = 0, 1`** holds fib(0) and fib(1). **`a, b = b, a + b`** moves both one step along at once: the right-hand side is worked out in full before either name changes.
- **`for _ in range(n)`**: `_` is the usual name for a loop variable you don't use.
- **`len(str(fib_bottom_up(1500)))`** turns the huge number into text and counts its characters, which is its number of digits.
- O(n) time, O(1) space, and no depth limit: fib(1500) has 314 digits and comes back instantly.

| Tier | What to say |
|---|---|
| Passes | The naive recursive version: correct, exponential time |
| Strong | + explains *why* it's slow (the same subproblems recomputed in different branches: 1,028,457 calls for n = 28) and fixes it with `@lru_cache` |
| Extra points | **[+Validate]** the call counts and `cache_info()` above, not a claimed speedup. **[+Edge cases]** the memoized recursion still goes n calls deep, so `fib_memo(1500)` raises `RecursionError`; the bottom-up loop doesn't, and uses O(1) space instead of O(n). **[+Edge cases]** a hand-rolled `def fib(n, cache={})` works, but it's Chapter 72's mutable-default trap (Q72-001): the one dictionary survives between calls. Write `cache=None` and create the dictionary inside, or say you're keeping it on purpose. **[+Business]** any recursive calculation with overlapping subproblems is a memoization candidate, not just textbook Fibonacci |

**Likely follow-ups:** What does the bottom-up version look like (above)? How do you spot a memoization opportunity? What's the space complexity of each version?
**Red flag:** saying "recursion is slow"; it isn't, inherently. Redundant recomputation is the problem.
**Learn it in:** Chapter 33, sections 33.8 (memoization, `lru_cache`, dynamic programming) and 33.5 (recursion and the 1,000-frame limit).

### Rapid-fire, 72A.5

Roles: DE, MLE and DS.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q72A-019 | What's a base case, and why does every recursive function need one? | The condition that returns an answer without calling the function again, so the recursion stops | **[+Edge cases]** with a missing or wrong base case the recursion never stops; Python halts it with `RecursionError` (the language-neutral name is a stack overflow), the recursive twin of Q70-041's never-ending macro loop | Fresher · 33.5 |

---

## 72A.6 Sorting and searching

### Q72A-020 · Implement merge sort and explain why it's O(n log n)

**Level:** Mid · **Roles:** DE, MLE, DS · **Beyond the book**

**Remember it as:** *Split in half until you can't, then merge back up while comparing. The "log n" is how many times you can halve; the "n" is the work at each level.*

**Answer in one line:** Merge sort splits the list in half repeatedly down to single items, then merges sorted halves back together; there are about log₂ n levels of splitting, and each level's merging touches all n items, so the total is n log n.

**Beyond the book: merge sort by hand.** Chapter 33 uses `sorted()` and doesn't build a sort. Here is merge sort on four numbers. Split until every piece has one item (a one-item list is already sorted), then merge pairs of sorted pieces, each time taking the smaller front item:

```text
[38, 27, 43, 3]
split:   [38, 27]         [43, 3]
split:   [38]  [27]       [43]  [3]
merge:   [27, 38]         [3, 43]         level 1: 4 items handled
merge:   [3, 27, 38, 43]                  level 2: 4 items handled
```

Two levels, because 4 halves twice to reach 1 (log₂ 4 = 2), and each level handles all 4 items: 2 × 4 = 8 steps of merging. For n items: log₂ n levels × n items each.

First the merge step on its own, the two-pointer walk of Q72A-012:

```python
def merge(left, right):
    merged = []
    i = 0                            # next unused item in left
    j = 0                            # next unused item in right
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])          # one side is used up; copy what's left of the other
    merged.extend(right[j:])
    return merged

print(merge([27, 38], [3, 43]))
```

```
[3, 27, 38, 43]
```

- **`i` and `j`** are the two pointers, one per list. Each pass of the loop takes the smaller front item and moves that list's pointer on.
- **`left[i] <= right[j]`** uses `<=`, not `<`, so on a tie the item from the left list goes first. That keeps equal items in their original order, which makes merge sort **stable** (Q72A-024).
- **`.extend(left[i:])`** adds whatever remains once one list runs out; one of the two slices is always empty.
- **What if you change `<=` to `<`?** The output is the same for these numbers, but on a tie the right-hand item would go first, and the sort would no longer be stable.

Then the sort itself calls itself on each half and merges the results:

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

print(merge_sort([38, 27, 43, 3]))
print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

```
[3, 27, 38, 43]
[3, 9, 10, 27, 38, 43, 82]
```

- **`if len(arr) <= 1: return arr`** is the base case: nothing to split.
- **`mid = len(arr) // 2`** finds the halfway point (`//` is whole-number division); the two recursive calls sort each half, and `merge` combines them.

| Tier | What to say |
|---|---|
| Passes | Names merge sort as O(n log n) with no explanation of why |
| Strong | The implementation above, explaining the split-then-merge structure and the base case |
| Extra points | **[+Signpost]** "log n" is the number of times the list can be halved before reaching single items; "n" is the merging work at each of those levels; together n log n. **[+Trade-offs]** merge sort needs O(n) extra space and is stable. Quicksort is typically faster in practice, uses O(log n) stack space on average, is unstable, and degrades to O(n²) when pivots are chosen badly (for example, always the first element on already-sorted data); random or median-of-three pivots avoid that |

**Likely follow-ups:** Quicksort instead: implement it? Why would you pick one over the other? Is Python's built-in sort stable?
**Red flag:** can't explain where the "log n" comes from.
**Learn it in:** Beyond the book (the primer above); `sorted()`, Timsort and stability: Chapter 33, section 33.7.

### Q72A-021 · Implement binary search, and state its one hard requirement

**Level:** Fresher · **Roles:** DE, AE, MLE, DS

**Remember it as:** *Binary search only works on sorted data. That's not a footnote, it's the whole trick.*

**Answer in one line:** Look at the middle item of a sorted list; if the target is bigger, throw away the left half, if smaller the right half, and repeat: O(log n), about 20 looks for a million items.

The cell's last line searches an *unsorted* list. Before you run it, predict what it prints: the list does hold a 9.

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

sorted_data = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(sorted_data, 9), binary_search(sorted_data, 4))
print(binary_search([9, 1, 13, 3, 11, 5, 7], 9))
```

```
4 -1
-1
```

- **`binary_search(arr, target)`** returns the position of `target` in `arr`, or −1 if it isn't there.
- **`while lo <= hi`** keeps going while there is anything left to search.
- **`lo` and `hi`** mark the part of the list still worth searching; **`mid = (lo + hi) // 2`** is the middle position of that part.
- **`if` / `elif` / `else`**: found it, return the position; the middle value is too small, so the target can only be to its right (`lo = mid + 1`); otherwise it can only be to the left (`hi = mid - 1`).
- 9 is at position 4. 4 isn't in the list, so the loop ends with `lo > hi` and the function returns −1.
- **The last line is the trap:** the same numbers, unsorted. 9 *is* in the list (at position 0), but the search throws away the half it's in and answers −1, with no error. That's why the requirement matters.

| Tier | What to say |
|---|---|
| Passes | The implementation, without stating the sorted-input requirement clearly |
| Strong | + states explicitly: the list must be sorted, or binary search silently gives wrong answers rather than raising an error (the last line above) |
| Extra points | **[+Edge cases]** `(lo + hi) // 2` can overflow in languages with fixed-size integers; Python's integers are unbounded, but say you know the general issue. **[+Business]** a database index lookup is the same halving idea on a B-tree, which is why an index turns a slow table scan into a fast lookup. **[+Simple first]** in real Python code, `bisect` does this for you |

**Likely follow-ups:** Find the first occurrence of a duplicated value? Search in a rotated sorted list?
**Red flag:** forgetting the sorted-input requirement.
**Learn it in:** Chapter 33, section 33.7 (binary search, `bisect`); Chapter 28, section 28.4 (B-tree indexes).

### Rapid-fire, 72A.6

Roles: DE, AE, MLE and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q72A-022 | Find the kth largest element in an array? | `heapq.nlargest(k, nums)[-1]`, or keep a min-heap of size k for very large data | **[+Trade-offs]** sorting everything is O(n log n) and simplest to write; the heap is O(n log k), faster when k is small next to n | Mid · 33.7 |
| Q72A-023 | Bubble sort versus merge sort: why does one matter in interviews and not in practice? | Bubble sort compares neighbours and swaps them if they're in the wrong order, repeating up to n passes: O(n²). It's asked to see whether you can *reason* about why it's slow, not because anyone uses it | **[+Business]** production code uses the language's built-in sort (Timsort in Python), not a hand-rolled one; interviews test the reasoning, not the reinvention | Fresher · 33.7 |
| Q72A-024 | What's a stable sort, and when does stability matter? | Equal elements keep their original relative order after sorting | **[+Edge cases]** sorting orders by date and wanting ties left in their original row order needs a stable sort; an unstable one can silently scramble the ties | Fresher · 33.7 |

---

## 72A.7 Linked lists

**Beyond the book: what a linked list is.** A Python list keeps its items side by side in memory. A **linked list** keeps each item in its own small object, a **node**, which holds a value and a pointer to the next node, in an attribute called `next`. The last node's `next` is `None`. The list itself is just a reference to the first node, the **head**:

```text
head
 |
[1 | next] --> [2 | next] --> [3 | next] --> None
```

To reach the third item you start at the head and follow `next` twice: finding an item is O(n), but adding or removing one where you already stand is O(1), since only a pointer changes. Python programs rarely need one (a list or `deque` does the job), but interviews like them because every answer is about pointers. A node is a small class, written as in Chapter 29, section 29.5: `__init__` runs when you write `Node(5)`, `self` is the new node, and `self.val = val` stores a value on it.

```python
class Node:
    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt

def build(values):                  # [1, 2, 3] -> 1 -> 2 -> 3, returns the head
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head

def to_list(head):                  # walk the nodes and collect their values
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

three = build([1, 2, 3])
print(three.val, three.next.val, three.next.next.val, three.next.next.next)
print(to_list(three))
```

```
1 2 3 None
[1, 2, 3]
```

- **`nxt=None`** is the default for the pointer; it's named `nxt` because `next` is already a Python built-in.
- **`build`** makes the nodes back to front: each new node points at the one made before it, so the last one made is the head.
- **`to_list`** is the walk every linked-list answer uses: `while head:` keeps going until it reaches `None`, and `head = head.next` steps forward.
- The first printed line follows the pointers by hand: 1, then 2, then 3, then `None`.

### Q72A-025 · Reverse a singly linked list

**Level:** Mid · **Roles:** DE, MLE · **Beyond the book**

**Remember it as:** *Three pointers walking together: remember where you came from, flip the arrow, step forward.*

**Answer in one line:** Walk the list once, turning each node's `next` to point at the node before it, while holding on to the rest of the list so it isn't lost: O(n) time, O(1) extra space.

```python
def reverse_list(head):
    prev = None
    while head:
        nxt = head.next     # remember what's next before we overwrite it
        head.next = prev    # flip this node's arrow backwards
        prev = head         # move prev forward
        head = nxt          # move head forward
    return prev

print(to_list(reverse_list(build([1, 2, 3, 4, 5]))))
print(to_list(reverse_list(build([]))), to_list(reverse_list(build([7]))))
```

```
[5, 4, 3, 2, 1]
[] [7]
```

The trace on three nodes, printed by the same loop, one row per pass (values shown instead of nodes):

```python
def val(node):
    return None if node is None else node.val

head, prev, step = build([1, 2, 3]), None, 0
while head:
    step += 1
    nxt = head.next
    head.next = prev
    print(f"step {step}: node {head.val} now points to {val(prev)}; prev={head.val}, head={val(nxt)}")
    prev, head = head, nxt
print("result:", to_list(prev))
```

```
step 1: node 1 now points to None; prev=1, head=2
step 2: node 2 now points to 1; prev=2, head=3
step 3: node 3 now points to 2; prev=3, head=None
result: [3, 2, 1]
```

After each step, one more arrow points backwards, and `nxt` has kept the rest of the list safe.

| Tier | What to say |
|---|---|
| Passes | Describes the goal correctly, struggles to produce working pointer logic |
| Strong | The three-pointer version above, walked through out loud step by step |
| Extra points | **[+Validate]** trace it by hand on a three-node list before typing it, the table above. **[+Edge cases]** the empty list and a one-node list both work without special cases (second output line); say that you checked |

**Likely follow-ups:** Reverse only part of the list (between positions m and n)? A recursive version instead of the loop?
**Red flag:** losing track of `head.next` before reassigning it, ending up with a list that loses its tail.
**Learn it in:** Beyond the book (the primer above); classes: Chapter 29, section 29.5.

### Q72A-026 · Detect a cycle in a linked list

**Level:** Mid · **Roles:** DE, MLE · **Beyond the book**

**Remember it as:** *Fast and slow pointers: if there's a loop, the fast one eventually laps the slow one. If there isn't, fast just reaches the end first.*

**Answer in one line:** Move one pointer one node at a time and another two at a time; if they ever land on the same node the list loops, and if the fast one reaches `None` it doesn't (Floyd's cycle detection): O(n) time, O(1) extra space.

The simple version first, with a set of nodes already visited:

```python
def has_cycle_set(head):
    seen = set()
    while head:
        if head in seen:
            return True
        seen.add(head)
        head = head.next
    return False
```

It works because a `Node` is hashable: instances of a plain class hash by identity, so the set asks "have I stood on *this very node* before?" (Q72A-015). Now the two-pointer version:

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

straight = build([1, 2, 3])
looped = build([1, 2, 3])
looped.next.next.next = looped          # node 3 now points back to node 1

print(has_cycle(straight), has_cycle(looped))
print(has_cycle_set(straight), has_cycle_set(looped))
```

```
False True
False True
```

- **`slow = fast = head`** starts both pointers at the head.
- **`while fast and fast.next`**: the fast pointer jumps two nodes, so both must exist; on a straight list it reaches the end and the loop stops.
- **`slow is fast`** asks "the very same node?", the identity test from Chapter 72's Q72-002, not "equal values".
- **`looped.next.next.next = looped`** makes the loop: the third node's `next` goes back to the first instead of to `None`. Both functions agree on both lists.

| Tier | What to say |
|---|---|
| Passes | "Keep a set of visited nodes and check for repeats": correct, O(n) extra space |
| Strong | The fast/slow pointer version (Floyd's cycle detection): O(1) extra space, same O(n) time |
| Extra points | **[+Trade-offs]** the set version is easier to write and reason about; interviewers usually want the two-pointer version because it's O(1) space. **[+Business]** cycle detection matters in real systems: circular references in data, or a loop in a pipeline's task graph (Chapter 33, section 33.6 checks one) |

**Likely follow-ups:** Find where the cycle begins, not just whether one exists? A cycle in a directed graph instead of a linked list?
**Red flag:** the set version presented as the only option, with no mention of the O(1)-space alternative.
**Learn it in:** Beyond the book (the primer above); cycles in graphs: Chapter 33, section 33.6.

---

## 72A.8 Trees and graphs

**Beyond the book: binary search trees.** Chapter 33, section 33.6 walks trees such as the org chart, where a node can have any number of children. A **binary tree** allows at most two, a **left** and a **right** child. A **binary search tree (BST)** adds one rule, the **invariant**: everything in a node's left subtree is smaller than the node, and everything in its right subtree is larger (or equal). Insert 50, 30, 70, 20 by hand: 50 becomes the root; 30 is smaller, so it goes left; 70 is larger, so it goes right; 20 is smaller than 50 (go left) and smaller than 30 (go left again):

```text
        50
       /  \
     30    70
    /
  20
```

Finding a value repeats the same choice at each node, so on a well-shaped tree a search takes about log₂ n steps, like binary search. An **in-order traversal** visits the left subtree, then the node, then the right subtree; on a BST that reads the values in sorted order (20, 30, 50, 70 here). The catch: insert values that are already sorted (20, 30, 50, 70) and each one goes right of the last, so the "tree" is a chain four deep and a search is O(n). Q72A-027 measures that.

### Q72A-027 · Build a binary search tree and do an in-order traversal

**Level:** Mid · **Roles:** DE, MLE, DS · **Beyond the book**

**Remember it as:** *In-order traversal of a BST always visits nodes in sorted order: that's the whole point of a BST.*

**Answer in one line:** Insert each value by walking down from the root (left if smaller, right if not) and attaching it where the walk runs out; an in-order traversal (left, node, right) then returns the values sorted.

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root

def inorder(root, out):
    if root:
        inorder(root.left, out)
        out.append(root.val)
        inorder(root.right, out)
    return out

root = None
for v in [50, 30, 70, 20, 40, 60, 80]:
    root = insert(root, v)
print(inorder(root, []))
```

```
[20, 30, 40, 50, 60, 70, 80]
```

- **`insert`** is recursive (Chapter 33, section 33.5). The base case, an empty spot (`root is None`), makes the new node. Otherwise it goes left or right, and **`root.left = insert(root.left, val)`** reattaches whatever the call below returns, so the new node is hooked in at the right place.
- **`inorder`** does exactly "left subtree, this node, right subtree", adding values to `out` as it goes. The output is sorted, which is itself the check that the tree was built correctly.

Now the shape problem, measured. The **height** is the number of nodes on the longest path from the root down:

```python
def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

chain = None
for v in [20, 30, 40, 50, 60, 70, 80]:          # the same values, already sorted
    chain = insert(chain, v)

print("mixed order, height:", height(root))
print("sorted order, height:", height(chain), inorder(chain, []))
```

```
mixed order, height: 3
sorted order, height: 7 [20, 30, 40, 50, 60, 70, 80]
```

The same seven values: inserted in a mixed order, the tree is three levels deep; inserted already sorted, it's a chain seven deep, a linked list in disguise, and every search walks it from end to end.

| Tier | What to say |
|---|---|
| Passes | Can build the tree, struggles to explain what in-order traversal guarantees |
| Strong | + states the invariant (left smaller, right larger), and that in-order traversal (left, node, right) therefore produces sorted output |
| Extra points | **[+Validate]** the sorted output is itself the check that the tree is right. **[+Edge cases]** inserting already-sorted data makes the tree a chain (height 7 instead of 3 above), O(n) instead of O(log n). That's why balanced trees exist: in-memory libraries use red-black or AVL trees, and databases use B-trees (Chapter 28, section 28.4), which stay shallow by keeping many keys in each node |

**Likely follow-ups:** Pre-order and post-order traversal, and what each is used for? How would you check whether a tree is balanced? Delete a node from a BST?
**Red flag:** not connecting in-order traversal to "produces sorted output" as the key insight.
**Learn it in:** Beyond the book (the primer above); recursion: Chapter 33, section 33.5; classes: Chapter 29, section 29.5.

### Q72A-028 · Breadth-first search (BFS) versus depth-first search (DFS) on a graph

**Level:** Mid · **Roles:** DE, AE, MLE, DS

**Remember it as:** *BFS spreads out level by level (a queue). DFS commits to one path and backtracks (a stack, or recursion).*

**Answer in one line:** Both visit every node reachable from a start; BFS takes nodes from a first-in-first-out queue, so it goes level by level and finds shortest paths in an unweighted graph, while DFS takes them from a stack (or recurses), so it follows one route to the end before backing up.

```python
from collections import deque

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order

def dfs(graph, node, visited=None):
    if visited is None:
        visited = []
    visited.append(node)
    for nb in graph[node]:
        if nb not in visited:
            dfs(graph, nb, visited)
    return visited

print("BFS:", bfs(graph, "A"))
print("DFS:", dfs(graph, "A"))
```

```
BFS: ['A', 'B', 'C', 'D', 'E']
DFS: ['A', 'B', 'D', 'E', 'C']
```

- **`graph`** is a dictionary of lists, as in Chapter 33, section 33.6: each node maps to its neighbours. D can be reached two ways (through B and through C).
- **`visited = {start}`** is a **set**, so each `nb not in visited` check is O(1) and BFS is O(V + E) for V nodes and E edges. A list here would make every check a scan (Q72A-014) and BFS O(V²).
- **`queue.popleft()`** takes from the front (Chapter 33, section 33.4), which is what makes the walk level by level: A, then B and C, then D, then E.
- **`dfs`** goes as deep as it can first: A, B, D, E, and only then back to C. It keeps `visited` as a list so the list *is* the visiting order, and it defaults to `None` rather than `[]` to avoid Chapter 72's mutable-default trap (Q72-001). On a big graph you'd keep a set for the checks as well.

| Tier | What to say |
|---|---|
| Passes | Knows BFS and DFS are "two ways to traverse a graph" |
| Strong | + BFS uses a queue (FIFO), explores level by level, and finds the *shortest* path in an unweighted graph; DFS uses a stack or recursion (LIFO) and goes as deep as possible before backtracking; `visited` is a set, so each check is O(1) and the walk is O(V + E) |
| Extra points | **[+Business]** BFS's shortest-path property makes it the choice for "fewest hops" problems (shortest chain of connections, fewest steps through a process); DFS is the natural choice for "does *any* path exist" and for checking a pipeline's graph for cycles. **[+Edge cases]** both need a `visited` set on any graph with cycles, or they loop forever: Q70-041's never-ending loop, applied to graph traversal |

**Likely follow-ups:** DFS without recursion (a list used as a stack)? Return the shortest path itself, not just the order? Detect a cycle in a directed graph?
**Red flag:** can't say which one (BFS) guarantees the shortest path in an unweighted graph.
**Learn it in:** Chapter 33, sections 33.6 (depth-first, breadth-first, cycles) and 33.4 (`deque`).

### Q72A-029 · Level-order traversal of a tree, and why it's really BFS in disguise

**Level:** Mid · **Roles:** DE, MLE, DS

**Remember it as:** *A tree is just a graph with no cycles and one path down from the root. BFS on it, level by level, is level-order traversal.*

**Answer in one line:** Run BFS from the root with a queue, but before each round note how many nodes the queue holds: exactly those nodes form the current level.

```python
from collections import deque

def level_order(root):
    out = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            if node:
                level.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
        if level:
            out.append(level)
    return out

print(level_order(root))       # the BST from Q72A-027
print(level_order(None))
```

```
[[50], [30, 70], [20, 40, 60, 80]]
[]
```

- **`for _ in range(len(queue))`** is the key line: `len(queue)` is read once, before the loop starts, so the loop takes exactly the nodes of this level, even though it keeps adding their children to the back of the queue.
- **`if node:`** skips the `None` children of leaf nodes; **`if level:`** skips the empty round those `None`s produce at the bottom.
- An empty tree (`None`) gives an empty list, with no special case.

| Tier | What to say |
|---|---|
| Passes | Produces a flat list of values with no level grouping |
| Strong | The queue-based version above, grouping values level by level, recognized as BFS applied to a tree |
| Extra points | **[+Signpost]** explain the `for _ in range(len(queue))` line explicitly: it's what separates "this level" from "everything else in the queue", and it's easy to get subtly wrong. **[+Edge cases]** the empty tree, checked above |

**Likely follow-ups:** Zigzag level order (alternating left-to-right and right-to-left)? The maximum width of any level?
**Red flag:** conflating this with a plain BFS that doesn't track level boundaries.
**Learn it in:** Chapter 33, section 33.6 (breadth-first, level by level: "who is two levels below the MD?"); the BST primer above.

---

## 72A.9 A live-coding walk-through: parentheses validation

### Q72A-030 · Given a string of brackets, determine if every bracket is properly closed and nested

**Level:** Fresher · **Roles:** DE, AE, MLE, DS

**Remember it as:** *A stack is "last opened, first closed": exactly how nested brackets have to resolve.*

**What they're really testing:** whether you recognize the stack pattern immediately from "nested" and "matching", and handle the edge cases without being prompted.

```python
def is_valid_parens(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

for test in ["({[]})", "({[)]}", "", ")))", ")(", "(("]:
    print(repr(test), is_valid_parens(test))
```

```
'({[]})' True
'({[)]}' False
'' True
')))' False
')(' False
'((' False
```

- **`stack`** is a plain list used as a stack (Chapter 33, section 33.4): `.append` pushes onto the top and `.pop()` takes the top off.
- **`pairs`** maps each closing bracket to the opening bracket it needs.
- **`not stack or stack.pop() != pairs[ch]`**: if the stack is empty, `or` stops there (Chapter 17, section 17.5), so `.pop()` is never called on an empty list.
- **`repr(test)`** prints each string with its quotes, so the empty string shows as `''`.

**Walking through it out loud, the way you'd say it live:**

"I'll use a stack. Every time I see an opening bracket, I push it. Every time I see a closing bracket, I check two things: is the stack empty (a closing bracket with nothing open is automatically invalid), and does the top of the stack match this closing bracket's opener. If either check fails, I return false immediately. At the very end, if anything's still on the stack, there's an opener that was never closed, so I return `not stack`."

**Extra-points moves demonstrated:**
- **[+Edge cases]** the empty string is valid (`not stack` on an empty stack is `True`), and `")))"` fails at its first character, on the empty-stack check inside the loop.
- **[+Edge cases]** `"(("` gets through the loop but leaves two openers on the stack, so the final `not stack` catches it.
- **[+Validate]** all six cases above were run, not just claimed to work.
- **[+Business]** matching opens to closes is the same logic that checks JSON or HTML tags are balanced, not just an interview toy problem.

**Likely follow-ups:** What if other characters (letters, numbers) are mixed in and should be ignored? What's the space complexity? Could you solve it without a stack?
**Red flag:** checking only whether the counts of opens and closes match; that misses ordering entirely, and `")("` would wrongly pass (it's `False` above).
**Learn it in:** Chapter 33, section 33.4 (stacks).

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Nested loops over the same array | O(n²): fine on test data, far too slow at real volume | Reach for a dictionary or set first when checking "does this exist" |
| Keeping `visited` as a list in BFS or DFS | Every check is a scan, so the walk becomes O(V²) | Use a set: `visited = {start}`, `visited.add(nb)` |
| Assuming binary search works on unsorted data | Silently wrong answers, no error | Confirm sorted input before reaching for binary search |
| Losing a pointer before reassigning it (linked lists) | The rest of the list gets silently dropped | Save `head.next` before overwriting it, every time |
| No `visited` tracking in graph traversal | Infinite loop on any graph with a cycle | Always track visited nodes on a graph; trees don't need it (no cycles) but graphs do |
| Recursion with no base case, or a wrong one | `RecursionError` (a stack overflow) | State the base case explicitly before writing the recursive case |
| A mutable default as a cache (`def f(n, cache={})`) | State leaks between calls; timings and results depend on what ran before | `@lru_cache`, or `cache=None` and create the dictionary inside |
| Treating Big-O as "how fast it feels" | Confidently wrong complexity claims | Trace what happens as n doubles, on paper, before answering; then measure |
| Reinventing a sort algorithm in real code | Slower and buggier than the built-in sort | Know how sorting works for interviews; use `sorted()` in practice |

---

## In the real world: the DSA question that was really a scale question

Karan, interviewing for a Data Engineer role, is asked: "Given two large lists of customer IDs, find the ones that appear in both." He recognizes it immediately as a set-intersection problem and writes a clean, O(n + m) solution using Python sets in under two minutes.

The interviewer doesn't move on. "Good. Now: what if one of these lists has 200 million IDs and doesn't fit in memory?" This is a Senior-level follow-up, and Karan pauses, then reasons out loud: "Then I can't build a full Python set in memory. I'd sort both lists externally, with a merge sort variant designed for data that doesn't fit in RAM: sort chunks that do fit, write each to disk, then merge the sorted chunks. Then I'd walk through both sorted lists with two pointers, the same pattern as Q72A-012's sorted-array merge, advancing whichever pointer is behind. That's O(n log n) for the external sort plus O(n + m) for the merge-walk, and it only ever needs a small, bounded amount of memory at once."

The follow-up wasn't really about algorithms at all: it was about whether Karan's algorithmic thinking survives contact with a real, unglamorous constraint (memory), which is the everyday reality of data engineering work. His answer to the "easy" version was necessary but not sufficient; the extra-point move that mattered was **[+Scale]**, reasoning about what changes when an assumption (it fits in memory) breaks.

---

## Project

**Goal:** implement, verify, and explain your own version of the highest-value patterns from this chapter.

### Tools you'll need

**Python** (Chapter 17, section 17.0), standard library only, as in Chapter 33: `collections.deque` for BFS queues, `collections.Counter` for counting, `heapq` for the kth-largest pattern, `functools.lru_cache` for memoization, `time.perf_counter()` for timings. This chapter's snippets were run on Python 3.11.15. Practice platforms such as LeetCode or HackerRank are useful for volume practice, though the questions in this bank are deliberately sized for data-role interviews, not the hardest tier those platforms offer.

1. Implement Two Sum, a sliding-window maximum, and a stack-based bracket validator, each with your own test cases, run and checked, not just written.
2. Time a nested-loop O(n²) approach against a set-based O(n) approach at two sizes, n and 2n, with at least 5,000 elements, the way Q72A-002 did. Report both speedups, and check that doubling n roughly quadruples the slow version's time.
3. Build a small binary search tree from a list of your own choosing, verify that in-order traversal returns it sorted, and compare its height with the tree you get from the same values sorted.
4. Pick one problem from this chapter and practise saying your solution out loud, Chapter 69-style: clarify, simple answer first, then edge cases and complexity.

---

## Key terms

Big-O notation · time complexity · space complexity · O(1)/O(log n)/O(n)/O(n log n)/O(n²)/O(2ⁿ) · amortized complexity · hash map / set · hashable · two-pointer pattern · sliding-window pattern · recursion · base case · `RecursionError` · memoization · `lru_cache` · dynamic programming (top-down / bottom-up) · merge sort · quicksort · bubble sort · binary search · stable sort · heap · linked list · node · head · fast/slow pointers (Floyd's cycle detection) · binary search tree (BST) · BST invariant · tree height · in-order/pre-order/post-order traversal · breadth-first search (BFS) · depth-first search (DFS) · level-order traversal · stack (LIFO) · queue (FIFO)

---

## Final-week revision list

Q72A-001, Q72A-002, Q72A-007, Q72A-008, Q72A-009, Q72A-014, Q72A-018, Q72A-020, Q72A-021, Q72A-025, Q72A-026, Q72A-027, Q72A-028, Q72A-030.

---

## Where this leads

- **Looking back: Chapter 33, The Computer Science You Actually Need,** teaches the structures and patterns this bank tests; **Chapter 72, Python & pandas Question Bank,** covers the Python gotchas that came back here (mutable defaults, `is` versus `==`).
- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 74, Machine Learning Question Bank,** picks up "algorithm" in its other sense: the learning algorithms themselves, not data structures.
- **Chapter 77, Data Engineering & Data System Design Bank,** is where several of this chapter's patterns (the external-sort-and-merge story above, especially) show up again at real production scale.
