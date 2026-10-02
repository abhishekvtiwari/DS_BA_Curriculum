# Chapter 72A. Data Structures & Algorithms Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will practise:** answering the core data structures and algorithms (DSA) questions that come up in data-role interviews, sized for those roles rather than a full software-engineering gauntlet · reasoning about time and space (Big-O) out loud, and backing the claim with a measurement · implementing and explaining the handful of structures and patterns that actually recur: hash maps and sets, two pointers and sliding windows, recursion and memoization, sorting and searching, linked lists, trees, and graphs · predict the output of a short snippet cold, which is how this round usually opens, from the warm-up cases to the brain-racking ones.
>
> **Before you start:** **do Chapter 33 first** (The Computer Science You Actually Need): it teaches almost every idea in this bank. You also need Chapter 17 (Python from zero), Chapter 29, section 29.5 (writing a class with `__init__` and `self`), and Chapter 69 (the three answer tiers and the twelve extra-point tags). Chapter 72's Python gotchas (mutable defaults, `is` versus `==`) come back here twice.
>
> **Time needed:** 8–10 hours to run every snippet and answer each question aloud; 1 hour for a revision pass. Section 72A.10, the predict-the-output round, is worth its own sitting of about 2 hours, answering each snippet out loud before reading on. Add 3–4 hours if the Chapter 33 sections named in the Learn-it-in lines are new to you.
>
> **How this chapter is built.** Same format as the other question banks in Part 8: every core question leads with a **"Remember it as…"** hook, then a one-line answer, then a compact tier table (what **passes**, what's **strong**, and the **extra points**, tagged with Chapter 69's moves: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Rapid-fire sections are scan tables. **Every snippet was run, and every output shown is real**, on Python 3.11.15 with the standard library only — except section 72A.10, which was added later and run on Python 3.12.0, also standard library only, and which says so again where it matters; the book recommends Python 3.14 (Chapter 17, section 17.0), and none of these outputs depend on the version. Timings change on every run and every machine, so the cells that print them say so; run them yourself in a notebook (Chapter 17 set one up) and expect your numbers to differ, not the pattern.
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

## 72A.10 Predict the output: from basic to brain-racking

A DSA round often opens with a short snippet and one question: **what does this print?** It is a cheap question to ask and an expensive one to get wrong, because the answer is either right or it is not, and the interviewer learns in ten seconds whether you know how Python's containers actually behave or have been getting away with the parts that usually work.

Everything below turns on one of three things, and they are the three things that break real data code:

1. **Equality and hashing are not what you assume.** `True` is `1`. A NaN is not equal to itself. Those two facts eat dictionary keys and corrupt lookups.
2. **A container you are iterating is not safe to change**, and Python will sometimes tell you and sometimes quietly give you the wrong answer.
3. **An operation that looks cheap can be O(n)**, and the cost only shows up at production volume.

Read the snippet, say the answer out loud, then read on. The last five are hard on purpose.

**How these were run.** Every snippet below was executed and every output is that run's own, on **Python 3.12.0**, standard library only. The rest of this chapter was run on Python 3.11.15; nothing in this section behaves differently between the two, with one exception that is itself a question — Q72A-042 depends on how the compiler folds constants, and it says so. The four questions that print timings print different numbers on every machine and every run; what does not change is the ratio, and the ratio is the point.

### Q72A-031 · `counts[1]`, `counts[True]` and `counts[1.0]`: how many keys?

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *A dictionary key is found by hash and equality, not by type. `True == 1 == 1.0`, and all three hash the same, so they are one key wearing three costumes.*

**Answer in one line:** One key, holding the last value written: `True` and `1.0` are equal to `1` and hash to the same number, so each assignment overwrites the previous one rather than adding a new entry.

```python
counts = {}
counts[1] = 'one'
counts[True] = 'true'
counts[1.0] = 'float one'
print(counts)
print(len(counts))
print(hash(1), hash(True), hash(1.0))
```

```
{1: 'float one'}
1
1 1 1
```

Look at what survived: the key printed is `1`, because the first write created it and later writes only replaced its value. The key keeps the *original* object; the value is the last one in.

This is not a curiosity. Counting things is most of what data code does, and a counter keyed on a column that mixes booleans with numbers silently merges the two. A `0`/`1` flag column that pandas or a CSV reader turned into `True`/`False` in one file and `1`/`0` in another will count into the same bucket, and the total will look perfectly reasonable.

| Tier | What to say |
|---|---|
| Passes | "They overwrite each other" |
| Strong | + the mechanism: dictionary keys are matched by hash then equality, `True == 1` is true and `hash(True) == hash(1)`, so all three are the same key. Notes that the surviving key is the first object and the surviving value is the last |
| Extra points | **[+Edge cases]** `0`, `False` and `0.0` collapse the same way; so does `Decimal(1)` · **[+Validate]** `len()` on the dictionary is the one-line check that keys merged · **[+Business]** a flag column read as bool from one source and int from another merges into one count with no error anywhere |

**Likely follow-ups:** What about `0` and `False`? What does `{1, True}` give? *(A set of one element.)* How would you key a dictionary so booleans and integers stay apart? *(Key on `(type(x).__name__, x)`, or normalise the type on the way in.)*
**Red flag:** believing a dictionary keys on type as well as value. It is the assumption behind a whole class of silent merge bugs.
**Learn it in:** Chapter 33, section 33.4 (hash maps); Chapter 17, section 17.3 (types and truthiness).

### Q72A-032 · `result = nums.sort()`: what is in `result`?

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *The methods that change a list in place return `None`. If you can assign it, you probably wanted the function, not the method.*

**Answer in one line:** `None`: `list.sort()` sorts the list in place and returns nothing, so the name you assigned it to now holds `None` and the sorted data is in the original list.

```python
nums = [3, 1, 2]
result = nums.sort()
print(result)
print(nums)
print(sorted([3, 1, 2]))
```

```
None
[1, 2, 3]
[1, 2, 3]
```

Python is consistent about this: a method that mutates the object returns `None`. `sort`, `reverse`, `append`, `extend`, `update` — all of them. The functions that return a new object are the ones you assign: `sorted`, `reversed`, `list(...)`.

The bug this causes is nastier than it looks, because `None` does not fail immediately. It fails two lines later, in something that iterates, with a message that points at the wrong place: `TypeError: 'NoneType' object is not iterable`.

| Tier | What to say |
|---|---|
| Passes | "`sort` returns `None`" |
| Strong | + the rule it is an instance of — mutating methods return `None`, functions return new objects — and names `sorted` as the one to assign |
| Extra points | **[+Edge cases]** the same for `reverse()` against `reversed()`, and `dict.update()` · **[+Validate]** `TypeError: 'NoneType' object is not iterable` a few lines later is the signature of this mistake · **[+Trade-offs]** `sort` is cheaper than `sorted` because it does not copy; use it when you do not need the original order back |

**Likely follow-ups:** How would you sort a list without changing it? Which is faster, and why? What does `sorted` return for a dictionary? *(A list of its keys.)*
**Red flag:** writing `nums = nums.sort()`, which throws the data away and keeps `None`.
**Learn it in:** Chapter 17, section 17.4 (lists); Chapter 33, section 33.6 (sorting).

### Q72A-033 · `nums[5:]` and `nums[5]` on a three-item list: which one raises?

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *Slicing clamps, indexing does not. A slice past the end gives you nothing; an index past the end gives you an error.*

**Answer in one line:** `nums[5:]` returns an empty list without complaint, while `nums[5]` raises `IndexError` — slicing silently clips to the available range, which is convenient and is also how an empty result reaches production unnoticed.

```python
nums = [1, 2, 3]
print(nums[5:])
print(nums[1:99])
print(nums[5])
```

```
[]
[2, 3]
Traceback (most recent call last):
  ...
IndexError: list index out of range
```

The first two lines are the whole lesson. `nums[5:]` wanted items from position 5 onward and there are none, so it returns `[]`. `nums[1:99]` wanted up to position 99 and stopped at the end.

Convenient, and dangerous in exactly one situation: paging. Code that slices `rows[page*size : (page+1)*size]` returns an empty list for every page past the last one, rather than telling you the page does not exist. An empty page and a page of nothing look identical.

| Tier | What to say |
|---|---|
| Passes | "The slice works, the index errors" |
| Strong | + why: a slice describes a range and clamps it to what exists, an index names one position and must find it |
| Extra points | **[+Edge cases]** a negative index also raises, but a negative *slice* bound counts from the end: `nums[-99:]` is the whole list · **[+Business]** paging code that slices past the end returns an empty page silently; check the page number against `len` first · **[+Validate]** if a slice unexpectedly returns `[]`, print `len()` of the thing you sliced before guessing |

**Likely follow-ups:** What does `nums[-99:]` give? What about `nums[::-1]`? *(The list reversed.)* How do you get the last item safely on a list that may be empty?
**Red flag:** expecting a slice to raise. It is the reason an empty result gets blamed on the data rather than the index arithmetic.
**Learn it in:** Chapter 17, section 17.4 (lists and slicing).

### Q72A-034 · `a = (1)` and `b = (1,)`: what are their types?

**Level:** Fresher · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *The comma makes the tuple, not the brackets.*

**Answer in one line:** `a` is an `int` and `b` is a `tuple`: brackets around a single value are just arithmetic grouping, and it is the trailing comma that makes a one-item tuple.

```python
a = (1)
b = (1,)
print(type(a).__name__, type(b).__name__)
print(len(b))

d = {}
d[(1, 2)] = 'pair'
print(d)
```

```
int tuple
1
{(1, 2): 'pair'}
```

The reason it matters in a DSA round is that tuples are the hashable container. Lists cannot be dictionary keys or set members (Q72A-039); tuples can. So the moment you need to key something on a pair of coordinates, a (row, column) cell, or an edge in a graph, you need a tuple and you need the syntax to be right.

The failure is quiet when the one-item case appears: a function that returns `(value)` returns the value, and a caller that does `x, = result` or `len(result)` gets a surprise.

| Tier | What to say |
|---|---|
| Passes | "You need the comma" |
| Strong | + that the brackets are grouping, the comma is the tuple constructor, and `1,` on its own is also a tuple |
| Extra points | **[+Edge cases]** `()` *is* the empty tuple, the one case with no comma · **[+Edge cases]** `return x,` accidentally returns a one-tuple, a common source of "why is my value in brackets" · **[+Validate]** `type(...).__name__` in a print is quicker than reasoning about it |

**Likely follow-ups:** Why can a tuple be a dictionary key when a list cannot? What is `()`? Is a tuple always hashable? *(No — `(1, [2])` is not, because it contains a list.)*
**Learn it in:** Chapter 17, section 17.4 (tuples); Chapter 33, section 33.4 (hashable keys).

### Q72A-035 · Removing items from a list while looping over it

**Level:** Mid · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *The loop walks by position while `remove` shifts everything left. Every time you delete, the next item slides under the cursor and is skipped.*

**Answer in one line:** `['a', 'b', 'drop', 'drop', 'c']` — two of the four `'drop'` items survive, because each removal shifts the remaining items down one position and the loop's internal counter has already moved past the one that slid into the gap.

```python
items = ['a', 'drop', 'drop', 'b', 'drop', 'drop', 'c']
for x in items:
    if x == 'drop':
        items.remove(x)
print(items)
```

```
['a', 'b', 'drop', 'drop', 'c']
```

Trace it once and you never write it again. The loop holds an index, not the item. At index 1 it sees `'drop'` and removes it; everything shifts left, so the second `'drop'` is now at index 1 — but the loop goes to index 2, which is `'b'`. The second `'drop'` was never examined.

The pattern in the output is the signature: **every other match survives**. If you ever see a cleaning step that removed roughly half of what it should have, this is almost always why.

Three safe ways, in order of preference:

```python
items = ['a', 'drop', 'drop', 'b', 'drop', 'drop', 'c']
kept = [x for x in items if x != 'drop']        # build a new list
print(kept)

items[:] = [x for x in items if x != 'drop']    # same, but rebinds in place
print(items)
```

```
['a', 'b', 'c']
['a', 'b', 'c']
```

The second form matters when other names refer to the same list: `items[:] = ...` changes the list every name can see, where `items = ...` would only move your own name to a new list.

| Tier | What to say |
|---|---|
| Passes | "You shouldn't modify a list while iterating it" |
| Strong | + the actual output, and the mechanism: the loop tracks an index, `remove` shifts items left, so the item after a removed one is skipped |
| Extra points | **[+Validate]** the tell is that *every other* match survives, so a filter that removed about half of what it should is this bug · **[+Trade-offs]** a comprehension is clearer and usually faster than removing in place; `items[:] = ...` keeps other references pointing at the right list · **[+Edge cases]** iterating backwards also works and is sometimes necessary when you must mutate in place |

**Likely follow-ups:** Why does iterating backwards work? What is the complexity of `list.remove`? *(O(n), so this loop is O(n²) as well as wrong.)* What happens if you do this to a dictionary? *(Q72A-036 — it raises.)*
**Red flag:** not noticing. The code runs, returns a list, and the list looks plausible.
**Learn it in:** Chapter 17, section 17.6 (loops); Chapter 33, section 33.2 (arrays and lists).

### Q72A-036 · The same thing, but on a dictionary

**Level:** Mid · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *A list lets you corrupt it quietly. A dictionary refuses and tells you.*

**Answer in one line:** `RuntimeError: dictionary changed size during iteration` — unlike a list, a dictionary detects that its size changed mid-loop and raises immediately, which is the better behaviour of the two.

```python
d = {'a': 1, 'b': 2, 'c': 3}
for k in d:
    if d[k] == 2:
        del d[k]
```

```
Traceback (most recent call last):
  ...
RuntimeError: dictionary changed size during iteration
```

The fix is to iterate over a snapshot of the keys, so the thing you are walking and the thing you are changing are two different objects:

```python
d = {'a': 1, 'b': 2, 'c': 3}
for k in list(d):
    if d[k] == 2:
        del d[k]
print(d)
```

```
{'a': 1, 'c': 3}
```

`list(d)` copies the keys out before the loop starts. It costs one pass and one list, and it is correct.

Worth saying out loud in the interview: the dictionary's behaviour is *better* than the list's, and knowing that is the point. The list silently gives a wrong answer; the dictionary stops. Given a choice between a wrong result and a loud failure, every data pipeline wants the loud failure.

| Tier | What to say |
|---|---|
| Passes | "It raises an error" |
| Strong | + names it — `RuntimeError`, "dictionary changed size during iteration" — gives the `list(d)` fix, and contrasts it with the list case that fails silently |
| Extra points | **[+Edge cases]** changing a *value* is fine; only changing the size raises · **[+Edge cases]** sets behave like dictionaries here · **[+Business]** a loud failure beats a silent wrong answer, which is why this design is right |

**Likely follow-ups:** Does changing a value raise? *(No.)* What about a set? *(The same.)* Why does a list not do this?
**Learn it in:** Chapter 33, section 33.4 (hash maps); Chapter 17, section 17.7 (dictionaries).

### Q72A-037 · Reading from a `defaultdict` changes it

**Level:** Mid · **Roles:** DE, AE, MLE, DS

**Remember it as:** *A `defaultdict` creates the key the moment you look at it. Reading is writing.*

**Answer in one line:** The length goes from 1 to 2 and `'b' in seen` is `True`, because looking up a missing key on a `defaultdict` inserts it with the default value — merely *testing* `seen['b'] == 0` created `'b'`.

```python
from collections import defaultdict

seen = defaultdict(int)
seen['a'] += 1
print(len(seen), dict(seen))

if seen['b'] == 0:
    pass

print(len(seen), dict(seen))
print('b' in seen)
```

```
1 {'a': 1}
2 {'a': 1, 'b': 0}
True
```

Nothing was assigned to `'b'`. The `if` only read it. But `defaultdict.__missing__` runs on a failed lookup, inserts the default, and returns it — so the read had a side effect.

This is how a counter ends up with a long tail of zeros that were never observed, and the bug survives review because the code that caused it reads like a check rather than a write. In a graph problem it is worse: probing `adjacency[node]` for a node with no edges adds that node to the graph, and a later `len(adjacency)` reports more nodes than exist.

Two ways to look without touching:

```python
from collections import defaultdict
seen = defaultdict(int)
seen['a'] += 1

print(seen.get('b', 0))
print('b' in seen)
print(len(seen))
```

```
0
False
1
```

`.get()` and `in` never insert. Use them whenever you are asking a question rather than accumulating.

| Tier | What to say |
|---|---|
| Passes | "`defaultdict` fills in missing keys" |
| Strong | + that a *read* inserts, so `len` and `in` change as a side effect of looking, with `.get()` or `in` as the non-mutating alternatives |
| Extra points | **[+Edge cases]** `dict.setdefault` has the same effect on a plain dictionary · **[+Business]** a counter grows a tail of unobserved zeros, and a graph grows nodes that have no edges · **[+Validate]** compare `len()` before and after a read-only pass; if it moved, this is why |

**Likely follow-ups:** How would you count without this happening? *(`Counter`, or `dict.get(k, 0) + 1`.)* Does `Counter` behave the same way? *(Reading a missing key returns 0 without inserting.)* What does `setdefault` do?
**Red flag:** using a `defaultdict` as a general-purpose dictionary and then trusting `len` or `in`.
**Learn it in:** Chapter 33, section 33.4 (hash maps); Chapter 17, section 17.7 (dictionaries).

### Q72A-038 · `shallow = grid[:]`, then `shallow[0][0] = 99`

**Level:** Mid · **Roles:** DE, AE, MLE, DS

**Remember it as:** *A slice copies the outer list and nothing else. The rows are still the same rows.*

**Answer in one line:** `grid` becomes `[[99, 2], [3, 4]]` — `grid[:]` makes a new outer list holding references to the *same* inner lists, so changing an item inside a row changes it for both names.

```python
grid = [[1, 2], [3, 4]]
shallow = grid[:]
shallow[0][0] = 99
print(grid)
```

```
[[99, 2], [3, 4]]
```

The copy is real but shallow: `shallow` is a different list object from `grid`, and `shallow[0]` is the *same* object as `grid[0]`. Replacing a whole row (`shallow[0] = [9, 9]`) would leave `grid` alone; changing inside a row does not.

For a grid, a matrix, an adjacency list, or any nested structure, use `copy.deepcopy`:

```python
import copy
grid = [[1, 2], [3, 4]]
deep = copy.deepcopy(grid)
deep[1][0] = 77
print(grid)
print(deep)
```

```
[[1, 2], [3, 4]]
[[1, 2], [77, 4]]
```

Chapter 72, Q72-003 covers shallow against deep copying in general. The reason it reappears here is that DSA problems are mostly nested containers — grids, adjacency lists, memoisation tables — and a backtracking solution that "restores" a grid it never really copied will give a wrong answer that depends on the order the branches ran in.

| Tier | What to say |
|---|---|
| Passes | "It's a shallow copy" |
| Strong | + precisely what is shared: a new outer list, the same inner objects, so replacing a row is safe and mutating inside a row is not |
| Extra points | **[+Edge cases]** `list(grid)`, `grid.copy()` and `copy.copy(grid)` are all the same shallow copy · **[+Scale]** `deepcopy` is slow; in a hot loop, rebuild the rows with `[row[:] for row in grid]` instead · **[+Business]** a backtracking search that restores a grid it never copied gives answers that depend on branch order, which is a nightmare to reproduce |

**Likely follow-ups:** How would you copy one level deeper without `deepcopy`? *(`[row[:] for row in grid]`.)* What does `deepcopy` do with a cycle? *(It handles it, by remembering what it has already copied.)*
**Learn it in:** Chapter 72, Q72-003 (shallow and deep copies); Chapter 33, section 33.2.

### Q72A-039 · `{[1, 2], [3]}`: what happens?

**Level:** Mid · **Roles:** DE, AE, MLE, DS

**Remember it as:** *Sets and dictionary keys need something that cannot change, because the hash has to stay put. Lists change, so they are out.*

**Answer in one line:** `TypeError: unhashable type: 'list'` — a set stores items by hash, a list's contents can change and so would its hash, so Python refuses to let a list into a set or be used as a dictionary key.

```python
s = {[1, 2], [3]}
```

```
Traceback (most recent call last):
  ...
TypeError: unhashable type: 'list'
```

Tuples are the fix, because they cannot change:

```python
s = {(1, 2), (3,)}
print(sorted(s))
print(hash((1, 2)))
```

```
[(1, 2), (3,)]
-3550055125485641917
```

The hash is a big arbitrary-looking number and it differs between runs for strings, which is deliberate; for a tuple of integers it is stable within a run. What matters is the rule, not the number: **if an object can change, it cannot be hashed, and if it cannot be hashed it cannot be a key or a set member.**

This decides real design choices. Visited-set problems in graph and grid traversal need a hashable representation of a position, so cells go in as `(row, col)` tuples. A list of lists of edges cannot be deduplicated with a set; a list of tuples can.

| Tier | What to say |
|---|---|
| Passes | "Lists aren't hashable" |
| Strong | + why: a set finds items by hash, and a mutable object's hash could change after it was stored, so it would become unfindable. Tuples are immutable, so they are allowed |
| Extra points | **[+Edge cases]** a tuple containing a list is *also* unhashable: immutability has to go all the way down · **[+Edge cases]** `frozenset` is the hashable set, for when you need a set of sets · **[+Business]** this is why visited-sets in grid problems use `(row, col)` tuples |

**Likely follow-ups:** Is `(1, [2])` hashable? *(No.)* How do you make a set of sets? *(`frozenset`.)* Can a custom class be a dictionary key? *(Yes, if it defines `__hash__` and `__eq__` consistently.)*
**Learn it in:** Chapter 33, section 33.4 (hashable keys); Chapter 17, section 17.4.

### Q72A-040 · `print({3, 1, 2})` and `print({'banana', 'apple', 'cherry'})`

**Level:** Mid · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *A set of small integers looks sorted because each one hashes to itself. That is a coincidence of the data, not a promise.*

**Answer in one line:** `{1, 2, 3}` and `{'apple', 'cherry', 'banana'}` — the integers come out in ascending order and the strings do not, because small integers hash to themselves and land in slot order, while strings hash to scattered values.

```python
print({3, 1, 2})
print({'banana', 'apple', 'cherry'})
print({1, 2, 3} == {3, 2, 1})
```

```
{1, 2, 3}
{'apple', 'cherry', 'banana'}
True
```

The first line is the trap. Build a set of small integers, print it, see it sorted, and conclude that sets keep order. They do not. Dictionaries have kept insertion order since Python 3.7 and that *is* a guarantee; sets have no ordering guarantee at all, and the integer case only looks ordered because `hash(n) == n` for small integers, so they fall into slots in numeric order.

The third line is the part that is actually guaranteed: **set equality ignores order entirely.** Two sets with the same members are equal however they were built, which is exactly what you want for a "did I visit the same nodes" check.

The practical rule: never rely on the order of a set. If you need order, call `sorted()` on it, and say so in the code.

| Tier | What to say |
|---|---|
| Passes | "Sets are unordered" |
| Strong | + why the integer case looks ordered anyway (small integers hash to themselves), and that dictionaries *do* guarantee insertion order while sets do not |
| Extra points | **[+Edge cases]** string hashing is randomised per process by default, so a set of strings can print in a different order in a different run · **[+Validate]** any test that asserts on the printed form of a set is fragile; compare sets with `==`, or sort first · **[+Trade-offs]** `dict.fromkeys(xs)` deduplicates while keeping order, when you need both |

**Likely follow-ups:** How would you deduplicate while keeping order? *(`list(dict.fromkeys(xs))`.)* Do dictionaries guarantee order? *(Yes, since 3.7.)* Why would a set of strings print differently between runs?
**Red flag:** writing a test that asserts the printed form of a set. It passes until it does not.
**Learn it in:** Chapter 33, section 33.4; Chapter 17, section 17.7.

### Q72A-041 · `nan == nan` is `False`, so what does `nan in [nan]` give?

**Level:** Brain-racking · **Roles:** DE, AE, MLE, DS

**Remember it as:** *`in` checks identity before equality. The same NaN object is found; an equal-looking new one is not.*

**Answer in one line:** `True` — even though a NaN is not equal to itself, `in` tests `x is item or x == item`, and the NaN in the list is the very same object, so the identity test succeeds before equality is ever tried.

```python
nan = float('nan')
print(nan == nan)

values = [1.0, nan, 3.0]
print(nan in values)
print(values.index(nan))
print(float('nan') in values)
```

```
False
True
1
False
```

Read those four lines together, because the pair at the end is the whole question:

- `nan in values` is **`True`**: the object you are searching for *is* the object in the list.
- `float('nan') in values` is **`False`**: a brand new NaN is a different object, so identity fails, and then equality fails too, because no NaN equals anything.

So membership depends on *which* NaN you ask with. The same value, built twice, gives two different answers.

This is the single most useful thing to know about missing numeric data. A column with NaNs cannot be deduplicated by equality, cannot be grouped by equality, and cannot be reliably searched. Every library that handles it well — pandas among them — handles NaN as a special case rather than relying on `==`, which is why `df.isna()` exists and `df == np.nan` does not work.

The containment short-circuit (`is` before `==`) is a real optimisation in CPython and applies to every container, not just lists. It is almost always invisible, and NaN is where it becomes visible.

| Tier | What to say |
|---|---|
| Passes | "NaN isn't equal to itself" (true, and does not answer the question) |
| Strong | + `in` tries identity first, so the same object is found and an equal-looking new one is not, with both results read off |
| Extra points | **[+Edge cases]** `values.index(nan)` finds it for the same reason, and raises `ValueError` for a fresh NaN · **[+Business]** NaN cannot be deduplicated or grouped by equality, which is why pandas has `isna()` and why `df == np.nan` never works · **[+Edge cases]** the IEEE 754 rule that NaN compares unequal to everything is deliberate, so that a failed computation cannot silently equal a real result · **[+Validate]** test for it with `math.isnan(x)`, never `x == float('nan')` |

**Likely follow-ups:** How do you test for NaN? *(`math.isnan`, or `x != x`.)* What does `sorted` do with NaNs in a list? *(Something arbitrary — the comparisons are all false, so the result depends on the algorithm.)* What does `{nan, nan}` give? *(One element if it is the same object, two if they are different objects.)*
**Red flag:** confidently answering `False` because NaN is not equal to itself. It is the reasoning that *sounds* right and gets the answer wrong.
**Learn it in:** Chapter 33, section 33.3 (how numbers are stored); Chapter 14, section 14.3 (missing values); Chapter 72, Q72-010 (floating point).

### Q72A-042 · `int('257') is int('257')` against `257 is 257`

**Level:** Brain-racking · **Roles:** DE, AE, MLE, DS

**Remember it as:** *Python caches small integers, and the compiler folds repeated literals. Two different mechanisms, both making `is` lie about numbers.*

**Answer in one line:** `int('256') is int('256')` is `True` and `int('257') is int('257')` is `False`, because CPython keeps one shared object for every integer from −5 to 256 — but `257 is 257` written as literals is `True` anyway, because the compiler collapses the two identical constants into one before the code ever runs.

```python
a = int('256'); b = int('256')
print(a is b)

c = int('257'); d = int('257')
print(c is d)
print(c == d)

e = 257; f = 257
print(e is f)
```

```
True
False
True
True
```

Three different things are happening, and naming all three is what makes this a strong answer:

1. **The small-integer cache.** CPython creates the integers −5 to 256 once at startup and hands out the same object every time. So two separately computed 256s are the same object.
2. **No cache above that.** 257 is built fresh each time, so the two are equal but not identical.
3. **Constant folding.** When you write the literal `257` twice in the same block of code, the compiler stores one constant and points both names at it — so `e is f` is `True` even though nothing is cached at runtime. Build the same numbers at runtime, as the `int('257')` lines do, and the folding cannot happen.

That third point is why this question has to be written with `int('257')` to show anything at all. Written with plain literals it quietly answers `True` and teaches the opposite of the truth.

**None of this is a rule to rely on.** It is a CPython implementation detail; the boundary at 256 is not in the language specification and another implementation may do something else. The real lesson is the one that applies everywhere: **use `==` for values and `is` only for `None`, `True` and `False`.**

```python
x = [1, 2]
y = [1, 2]
print(x == y, x is y)
```

```
True False
```

Same values, different objects — and for lists there is no caching to confuse it.

| Tier | What to say |
|---|---|
| Passes | "Python caches small integers" |
| Strong | + the two separate mechanisms, cache and constant folding, and why the question needs `int('257')` to demonstrate anything |
| Extra points | **[+Edge cases]** the range is −5 to 256 in CPython and is not part of the language · **[+Trade-offs]** `is` is only correct for `None`, `True`, `False` and deliberate identity checks; linters flag `is` against a literal for exactly this reason · **[+Scale]** the cache exists because small integers are created constantly, so sharing them saves real allocation work |

**Likely follow-ups:** What is `is` actually comparing? *(Object identity — `id(x) == id(y)`.)* When *should* you use `is`? Does this apply to strings? *(Interning does something similar, and is equally not to be relied on.)*
**Red flag:** treating the 256 boundary as a language rule rather than one implementation's optimisation.
**Learn it in:** Chapter 72, Q72-002 (`is` against `==`); Chapter 33, section 33.3.

### Q72A-043 · A correct binary search returns −1 for an item that is in the list

**Level:** Brain-racking · **Roles:** DE, AE, MLE, DS

**Remember it as:** *Binary search does not search. It navigates a sorted order. Take the order away and it walks confidently to the wrong place.*

**Answer in one line:** `-1`, although `20` really is in the list — binary search assumes the data is sorted, and on unsorted data it discards the half containing the answer on its very first comparison, which is why its precondition is the whole question.

```python
def binary_search(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

print(binary_search([10, 20, 30, 40, 50], 20))
print(binary_search([50, 10, 40, 20, 30], 20))
print(20 in [50, 10, 40, 20, 30])
```

```
1
-1
True
```

The last two lines are the point. The linear `in` says the item is there. The binary search says it is not. The function has no bug.

Walk the second call: `mid` is 2, `xs[2]` is `40`, and `40 > 20`, so it throws away everything from index 2 rightwards — including index 3, where the `20` is. It then searches `[50, 10]`, compares against `50`, throws away the right half again, checks `50` once more and gives up. Every step is correct; the premise was not.

The standard library's `bisect` has the same precondition and fails the same way, without an error:

```python
import bisect
ordered = [10, 20, 30, 40, 50]
jumbled = [50, 10, 40, 20, 30]
print(bisect.bisect_left(ordered, 30), ordered.index(30))
print(bisect.bisect_left(jumbled, 30), jumbled.index(30))
```

```
2 2
2 4
```

On the sorted list `bisect` and `index` agree. On the jumbled one `bisect` says position 2 and the item is really at position 4 — and nothing anywhere raises.

The interview-grade version of the lesson: **if a function has a precondition, the caller owns it.** Sorting costs O(n log n) once, and then every search is O(log n). Searching n times without sorting costs O(n) each. The crossover is why you sort first and search many times, never the reverse.

| Tier | What to say |
|---|---|
| Passes | "Binary search needs a sorted list" |
| Strong | + reads off the contradiction — `in` says yes, binary search says no — and traces the first comparison to show which half was wrongly discarded |
| Extra points | **[+Edge cases]** `bisect` has the same precondition and returns a wrong position silently rather than raising · **[+Scale]** sorting once at O(n log n) pays for itself after enough searches; for a single lookup a linear scan is better · **[+Validate]** if a search says "not found" for something you can see in the data, check the precondition before the algorithm · **[+Clarify]** asking "is the input guaranteed sorted?" before writing the function is the move the interviewer is waiting for |

**Likely follow-ups:** How would you check the input is sorted, and what does that cost? *(O(n), which is the cost of the linear search you were avoiding.)* What is the complexity of sort-then-search against scanning n times? What does `bisect_left` return for an item that is not present?
**Red flag:** debugging the implementation. The function is correct, and time spent reading it is time not spent questioning the input.
**Learn it in:** Chapter 33, section 33.6 (binary search); Q72A-021 in this chapter.

### Q72A-044 · `heapq.heappop` after pushing 5, 1, 9, 3

**Level:** Mid · **Roles:** DE, AE, MLE, DS

**Remember it as:** *Python's heap is a min-heap. For a max-heap, push the negatives and negate on the way out.*

**Answer in one line:** `1` — `heapq` is a min-heap, so the smallest item is always on top; and the list prints as `[1, 3, 9, 5]`, which is heap order, not sorted order.

```python
import heapq

h = []
for x in [5, 1, 9, 3]:
    heapq.heappush(h, x)

print(h)
print(heapq.heappop(h))
```

```
[1, 3, 9, 5]
1
```

Two things to notice. The pop gives the smallest, not the largest — people coming from languages whose default heap is a max-heap get this backwards. And the internal list is **not sorted**: `[1, 3, 9, 5]` only guarantees that each parent is no larger than its children. Printing a heap and expecting sorted output is a separate small trap inside this one.

For a max-heap, negate:

```python
import heapq
h = []
for x in [5, 1, 9, 3]:
    heapq.heappush(h, -x)
print(-heapq.heappop(h))
```

```
9
```

This is the "top K" workhorse. For the k largest items out of n, a heap of size k costs O(n log k) and holds only k items in memory, where sorting everything costs O(n log n) and holds all n. On a stream you cannot sort at all, and the heap is the only option.

| Tier | What to say |
|---|---|
| Passes | "It's a min-heap, so 1" |
| Strong | + that the underlying list is in heap order rather than sorted order, and the negation trick for a max-heap |
| Extra points | **[+Scale]** top-k with a size-k heap is O(n log k) and O(k) memory, against O(n log n) and O(n) for sorting · **[+Edge cases]** `heapq.nlargest` and `nsmallest` do this for you and are clearer · **[+Edge cases]** negation is wrong for anything that is not a number; push `(-priority, item)` tuples instead |

**Likely follow-ups:** How would you get the 3 largest? Why is `heappush` O(log n)? What does `heapify` cost? *(O(n), better than pushing one at a time.)*
**Learn it in:** Chapter 33, section 33.7 (heaps and priority queues).

### Q72A-045 · Three operations that look O(1) and are not

**Level:** Brain-racking · **Roles:** DE, AE, MLE, DS

**Remember it as:** *Appending to a string, checking membership in a list, and inserting at the front of a list all copy or scan. Three loops that look linear and are quadratic.*

**Answer in one line:** All three are O(n) per operation and so O(n²) in a loop: building a string with `+=` copies the whole string each time, `x in list` scans every item, and `list.insert(0, x)` shifts every element right — and the measured gaps are large enough that none of it is theoretical.

```python
import time
from collections import deque

n = 20_000
data = list(range(n))
as_set = set(data)

t0 = time.perf_counter()
hits = sum(1 for i in range(n) if i in data)
list_t = time.perf_counter() - t0

t0 = time.perf_counter()
hits2 = sum(1 for i in range(n) if i in as_set)
set_t = time.perf_counter() - t0

print(hits, hits2)
print(f"list {list_t*1000:.0f} ms, set {set_t*1000:.0f} ms, ratio {list_t/set_t:.0f}x")
```

```
20000 20000
list 959 ms, set 1 ms, ratio 867x
```

Same answer, same data, **867 times** the time. The list has to scan on average half its contents for every one of the 20,000 lookups; the set hashes once.

The other two, measured the same way:

```python
import time
from collections import deque

n = 40_000
t0 = time.perf_counter()
s = ''
for _ in range(n):
    s += 'x'
concat = time.perf_counter() - t0

t0 = time.perf_counter()
parts = []
for _ in range(n):
    parts.append('x')
joined = ''.join(parts)
join_t = time.perf_counter() - t0

print(len(s), len(joined), s == joined)
print(f"concat {concat*1000:.1f} ms, join {join_t*1000:.1f} ms")

n = 50_000
t0 = time.perf_counter()
lst = []
for i in range(n):
    lst.insert(0, i)
ins_t = time.perf_counter() - t0

t0 = time.perf_counter()
dq = deque()
for i in range(n):
    dq.appendleft(i)
dq_t = time.perf_counter() - t0

print(f"list.insert(0) {ins_t*1000:.0f} ms, deque.appendleft {dq_t*1000:.0f} ms, ratio {ins_t/dq_t:.0f}x")
```

```
40000 40000 True
concat 22.5 ms, join 2.6 ms
list.insert(0) 288 ms, deque.appendleft 3 ms, ratio 103x
```

**These timings differ on every machine and every run** — the ratio in the last line came out 103× once and 72× on the next run of the same code. Run it yourself and expect different numbers. What does not change is which side is faster and by roughly how much, and that is what the question is about.

The three fixes are all one-liners: build a `set` for repeated membership tests, collect into a list and `''.join` it, and use `collections.deque` when you add or remove at the front.

The reason this is the brain-racking one rather than a triviality is that all three look innocent in review. `if customer_id in id_list` reads perfectly well. It is O(n), it is inside a loop over n customers, and it is the single most common accidental O(n²) in analysis code.

| Tier | What to say |
|---|---|
| Passes | "Sets are faster for lookups" |
| Strong | + names all three costs with their mechanism — copy, scan, shift — and gives the one-line fix for each |
| Extra points | **[+Validate]** measures it rather than asserting it, and says the ratio matters while the absolute numbers do not · **[+Scale]** a 20,000-row test that takes a second becomes a 2,000,000-row job that takes hours, because the cost is quadratic · **[+Edge cases]** `list.append` *is* amortised O(1); it is only the front that is expensive · **[+Business]** this is the usual reason a notebook that worked on a sample times out on the real extract |

**Likely follow-ups:** Why is `append` cheap when `insert(0)` is not? What is amortised complexity? What does `deque` give up to make both ends cheap? *(Indexing in the middle is O(n).)*
**Red flag:** knowing sets are faster but not being able to say what the list is actually doing, or by how much.
**Learn it in:** Chapter 33, section 33.1 (Big-O); Chapter 33, section 33.4 (hash maps); Q72A-002 in this chapter.

### Q72A-046 · Sorting twice to sort by two keys

**Level:** Mid · **Roles:** DE, AE, MLE, DS, DA

**Remember it as:** *Python's sort is stable, so equal items keep the order they came in. Sort by the minor key first, then the major one, and both hold.*

**Answer in one line:** Both lines print the same thing — sorting by name and then by score gives names in order within each score, because a stable sort never reorders items its key says are equal.

```python
people = [('Asha', 2), ('Bela', 1), ('Chit', 2), ('Dev', 1)]

print(sorted(people, key=lambda p: p[1]))

by_name = sorted(people, key=lambda p: p[0])
print(sorted(by_name, key=lambda p: p[1]))
```

```
[('Bela', 1), ('Dev', 1), ('Asha', 2), ('Chit', 2)]
[('Bela', 1), ('Dev', 1), ('Asha', 2), ('Chit', 2)]
```

They agree here because the input already happened to be alphabetical within each score. The guarantee is what matters: **stability is documented, not accidental**, so sorting by the minor key and then the major key is a correct way to do a multi-key sort, and it is the only way when the two keys sort in opposite directions.

That last case is the one worth knowing, because a single `key=` tuple cannot do it for a non-numeric field:

```python
people = [('Asha', 2), ('Bela', 1), ('Chit', 2), ('Dev', 1)]
by_name = sorted(people, key=lambda p: p[0])
print(sorted(by_name, key=lambda p: p[1], reverse=True))
```

```
[('Asha', 2), ('Chit', 2), ('Bela', 1), ('Dev', 1)]
```

Score descending, name ascending within each score. A single `key=lambda p: (-p[1], p[0])` would also work here because the score is a number that can be negated; if the major key were a string sorted in reverse, two passes would be the only option.

| Tier | What to say |
|---|---|
| Passes | "Python's sort is stable" |
| Strong | + what stability buys: minor key first, major key second, and both survive — plus the mixed-direction case where a single key tuple cannot do it |
| Extra points | **[+Edge cases]** `sorted(xs, key=lambda p: (-p[1], p[0]))` works for numbers only; negating a string is not possible · **[+Trade-offs]** two passes cost two sorts, so a single key tuple is faster when it is available · **[+Validate]** stability is a documented guarantee of `list.sort` and `sorted`, not an implementation accident |

**Likely follow-ups:** What algorithm does Python use? *(Timsort.)* Is it stable in every language? *(No — C++'s `std::sort` is not; `std::stable_sort` is.)* How would you sort by score descending and name ascending in one pass?
**Learn it in:** Chapter 33, section 33.6 (sorting); Q72A-020 in this chapter.

### Rapid-fire, 72A.10, part A: predict the output

Roles: DE, AE, MLE and DS for every row. Say the answer before you read it. Everything was run.

| # | Snippet | What it gives, and why | Extra point |
|---|---|---|---|
| Q72A-047 | `len({1, True, 1.0})` | `1` — same hash, all equal, one member. The set version of Q72A-031 | **[+Edge cases]** `{0, False}` is also one member → Ch 33 §33.4 |
| Q72A-048 | `print([1,2,3][::-1])` | `[3, 2, 1]` — a step of −1 reverses. It copies, so the original is unchanged | **[+Trade-offs]** `reversed()` returns a lazy iterator and copies nothing → Ch 17 §17.4 |
| Q72A-049 | `x = [1,2]; y = x; y.append(3); print(x)` | `[1, 2, 3]` — `y = x` binds a second name to one list, it does not copy | **[+Validate]** `y is x` is `True`; that is the check → Ch 17 §17.4 |
| Q72A-050 | `d = {}; print(d.get('k'), d.get('k', 0))` | `None 0` — `get` returns `None` by default, and never inserts | **[+Edge cases]** `d['k']` raises `KeyError`; `get` is the non-raising, non-inserting read → Ch 17 §17.7 |
| Q72A-051 | `print(sum([]), max([], default=0))` | `0` and `0` — `sum` of nothing is 0, but bare `max([])` raises `ValueError`; `default=` is what prevents it | **[+Edge cases]** unlike SQL's `SUM`, which gives NULL over no rows → Ch 71 Q71-078 |
| Q72A-052 | `print('10' > '9')` | `False` — string comparison is character by character, and `'1' < '9'` | **[+Business]** the classic reason sorted version numbers or IDs come out wrong → Ch 71 Q71-011 |
| Q72A-053 | `print(list(range(10**9))[:3])` vs `print(range(10**9)[:3])` | The first tries to build a billion-item list and exhausts memory; the second is instant, because `range` computes on demand | **[+Scale]** `range` is O(1) memory whatever its length → Ch 33 §33.2 |
| Q72A-054 | `print([] == False, bool([]) == False)` | `False` then `True` — an empty list is *falsy* but is not *equal* to `False` | **[+Edge cases]** test emptiness with `if not xs`, never `if xs == False` → Ch 17 §17.3 |
| Q72A-055 | `s = 'abc'; s[0] = 'z'` | `TypeError: 'str' object does not support item assignment` — strings are immutable | **[+Edge cases]** which is also why strings are hashable and lists are not → Q72A-039 |
| Q72A-056 | `print(len('café'), len('café'.encode()))` | `4` and `5` — one character, two bytes in UTF-8. Length in characters is not length in bytes | **[+Business]** a `VARCHAR(4)` column will reject that string if the database counts bytes → Ch 12 §12.8 |

### Rapid-fire, 72A.10, part B: complexity you can be caught on

| # | Question | The answer, and the reason | Extra point |
|---|---|---|---|
| Q72A-057 | Complexity of `x in my_list` against `x in my_set`? | O(n) against O(1) average. Measured in Q72A-045 at 867× on 20,000 items | **[+Edge cases]** set lookup is O(n) in the worst case, if every key collides → Ch 33 §33.4 |
| Q72A-058 | `list.append` against `list.insert(0, x)`? | Amortised O(1) against O(n): appending occasionally reallocates, inserting at the front shifts every element every time | **[+Scale]** `deque.appendleft` is O(1); measured at 103× faster → Ch 33 §33.2 |
| Q72A-059 | Is `dict` lookup really O(1)? | O(1) *average*, O(n) worst case when keys collide. Interviewers listen for the word "average" | **[+Validate]** saying "amortised" when you mean "average" is a different claim → Ch 33 §33.4 |
| Q72A-060 | Space complexity of naive recursive Fibonacci? | O(n) — not O(1). The call stack holds up to n frames even though no array is allocated | **[+Edge cases]** which is why it hits `RecursionError` at depth 1,000 before it is slow → Q72A-018 |
| Q72A-061 | Default recursion limit, and what happens at it? | 1,000, then `RecursionError: maximum recursion depth exceeded`. Raising it risks a real stack overflow, which crashes the process rather than raising | **[+Trade-offs]** convert to an explicit stack and a loop instead of raising the limit → Ch 33 §33.5 |
| Q72A-062 | Complexity of `sorted(xs)` and is it stable? | O(n log n), and yes — Timsort, stable, and the stability is guaranteed in the language | **[+Scale]** near-sorted input runs much closer to O(n), which Timsort is designed for → Q72A-046 |

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
| Removing items from a list while looping over it | Roughly every other match survives, with no error | Build a new list with a comprehension, or assign back with `xs[:] = ...` (Q72A-035) |
| Reading a missing key from a `defaultdict` | `len` and `in` change as a side effect of looking | Use `.get(k, default)` or `k in d` when you are asking rather than accumulating (Q72A-037) |
| Testing for NaN with `==` | Always false, so the row is never caught | `math.isnan(x)`, or `x != x`; and remember `in` finds the *same* NaN object (Q72A-041) |
| `x in a_list` inside a loop | Accidental O(n²); fine on a sample, hours on the real extract | Build a set once and test against that (Q72A-045) |

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

Big-O notation · time complexity · space complexity · O(1)/O(log n)/O(n)/O(n log n)/O(n²)/O(2ⁿ) · amortized complexity · hash map / set · hashable · two-pointer pattern · sliding-window pattern · recursion · base case · `RecursionError` · memoization · `lru_cache` · dynamic programming (top-down / bottom-up) · merge sort · quicksort · bubble sort · binary search · stable sort · heap · linked list · node · head · fast/slow pointers (Floyd's cycle detection) · binary search tree (BST) · BST invariant · tree height · in-order/pre-order/post-order traversal · breadth-first search (BFS) · depth-first search (DFS) · level-order traversal · stack (LIFO) · queue (FIFO) · hashable · identity against equality (`is` / `==`) · small-integer cache · constant folding · NaN · IEEE 754 · shallow copy · `deepcopy` · mutation during iteration · `RuntimeError: dictionary changed size` · `defaultdict.__missing__` · `dict.get` · `Counter` · set ordering · insertion order · stable sort · Timsort · min-heap · `heapq` · `deque` · amortised O(1) · average against worst case · `bisect` · precondition · immutability · `frozenset`

---

## Final-week revision list

Q72A-001, Q72A-002, Q72A-007, Q72A-008, Q72A-009, Q72A-014, Q72A-018, Q72A-020, Q72A-021, Q72A-025, Q72A-026, Q72A-027, Q72A-028, Q72A-030, Q72A-035, Q72A-041, Q72A-043, Q72A-045.

The last four are the predict-the-output questions worth most per minute: removing while iterating (Q72A-035), NaN and the identity short-circuit (Q72A-041), binary search on unsorted data (Q72A-043), and the three operations that look O(1) and are not (Q72A-045).

---

## Where this leads

- **Looking back: Chapter 33, The Computer Science You Actually Need,** teaches the structures and patterns this bank tests; **Chapter 72, Python & pandas Question Bank,** covers the Python gotchas that came back here (mutable defaults, `is` versus `==`).
- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 74, Machine Learning Question Bank,** picks up "algorithm" in its other sense: the learning algorithms themselves, not data structures.
- **Chapter 77, Data Engineering & Data System Design Bank,** is where several of this chapter's patterns (the O(n²) lesson of Q72A-002 especially, which returns in Q77-035's deduplication design) show up again at real production scale.
