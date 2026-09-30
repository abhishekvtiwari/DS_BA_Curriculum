# Chapter 72. Python & pandas Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the Python and pandas questions that come up across screening calls, live-coding rounds, and take-homes for every data role · recognize the classic Python gotchas (mutable defaults, `is` vs `==`, late-binding closures) before they bite you live · write idiomatic, vectorized pandas instead of slow, easy-to-get-wrong loops · debug broken pandas code the way a live round actually tests you.
>
> **Before you start:** Chapter 17 (Python from zero) and Chapter 18 (pandas), which teach almost everything here; Chapter 29 (classes, decorators, generators, keyword-only arguments) and Chapter 33 (generators and memory) for section 72.3; Chapter 69 for the answer tiers and the twelve extra-point tags. Chapter 71's SQL answers are the twins of this chapter's `merge` questions.
>
> **Time needed:** about 4–6 hours to run every snippet yourself; 1 hour for a revision pass.
>
> **How this chapter is built.** Same format as every question bank in Part 8 (Chapters 70–82): every core question leads with a **"Remember it as…"** hook, a one-line answer, and a compact tier table; rapid-fire sections are scan tables. Each question carries a level, **Warm-up**, **Core**, or **Advanced**, and within each group the questions run from easy to hard. **Every code snippet in this chapter was run**, on Python 3.11.15 with pandas 3.0.6; the book's recommended Python is 3.14 (Chapter 17, section 17.0), and where a version changes an output, the text says so. The order: language fundamentals and their gotchas first, then functions and iteration, then pandas from basic selection through to debugging and live coding.
>
> **Learn it in** pointers name the chapter and section that teach each idea. Questions marked **Beyond the book** go further than Chapters 17–18 and carry their own short explanation, so you can learn the idea here.
>
> **A note on currency.** This chapter is written against **pandas 3.0**, where two recent changes affect classic interview answers. First, **Copy-on-Write is always on** and can't be turned off, which retires the once-common "explain `SettingWithCopyWarning`" question (Q72-036). Second, **text columns now default to a dedicated `str` dtype**, not the older, more generic `object` dtype every pre-3.0 tutorial describes (Q72-038, Q72-051, Q72-054). Both the old behavior (which you may still meet on a team running an older pandas) and the current one are covered, clearly labeled.

---

## 72.1 Python fundamentals: the gotchas that catch experienced candidates

### Q72-001 · Why does calling a function with a mutable default argument twice give a surprising result?

**Level:** Core · **Beyond the book**

**Remember it as:** *A default argument is created once, when the function is defined, not fresh on every call. A mutable default remembers everything you've ever done to it.*

**Answer in one line:** A default argument value is evaluated exactly once, at function definition time, and reused across every call, so a mutable default (like a list) accumulates changes across calls instead of starting fresh each time.

**Beyond the book.** Chapter 17, section 17.8 teaches default values (`discount_pct=0`) but not this trap. A list is **mutable**: `.append()` changes the list itself rather than making a new one. Python builds a default value once, when it runs the `def` line, and hands that same object to every call that leaves the argument out. With a number as the default, nothing can change it in place; with a list, every `.append()` lands in the one shared list.

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket

r1 = add_item("crate")
print(r1)
```

```
['crate']
```

So far, as expected. Now call it a second time, with no `basket` again:

```python
r2 = add_item("lid")
print(r1, r2, r1 is r2)
```

```
['crate', 'lid'] ['crate', 'lid'] True
```

- The second call returned `['crate', 'lid']`, not `['lid']`: the default list still held `"crate"` from the first call.
- **`r1` changed too**, after the fact, although nothing touched `r1` directly. That's because `r1` and `r2` are two names for the same list.
- **`r1 is r2`** asks "are these the very same object?" (`is`, Chapter 17, section 17.5; Q72-002 goes further). `True` proves there is one list, not two that happen to look alike.

**The fix:** use `None` as the default and build a fresh list inside the function, on every call.

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print(add_item("crate"))
print(add_item("lid"))
```

```
['crate']
['lid']
```

- **`basket=None`** makes the default something that can't be changed in place.
- **`if basket is None: basket = []`** runs on every call that leaves `basket` out, so each such call builds its own new list; `.append(item)` then adds to that list only, and `return` hands it back.
- Each call now returns a list with just its own item.

| Tier | What to say |
|---|---|
| Passes | "You shouldn't use mutable defaults" (correct instinct, no demonstration of why) |
| Strong | The mechanism: the empty list is created once, at definition time, and silently shared by every call that doesn't pass its own `basket`; the fix is `basket=None`, then `if basket is None: basket = []` inside the function |
| Extra points | **[+Validate]** the two cells above: `r1 is r2` is `True`, so both calls returned the exact same list object, and the fixed version returns `['lid']` on its own. **[+Edge cases]** the same trap applies to a `{}` or `set()` default |

**Likely follow-ups:** Does this happen with immutable defaults like `basket=0`? *(No: immutable defaults can't be changed in place, so there's nothing to accumulate.)* Where else in Python does "created once, reused" show up? *(Q72-004 and Q72-020.)*
**Red flag:** not knowing why this specific bug happens, or claiming it's random behavior.
**Learn it in:** Beyond the book (defaults themselves: Chapter 17, section 17.8).

### Q72-002 · What's the difference between `is` and `==`, and when does mixing them up cause a real bug?

**Level:** Warm-up

**Remember it as:** *`==` asks "do these look the same?" `is` asks "are these literally the same object in memory?"*

**Answer in one line:** `==` compares values for equality (and can be customized per type); `is` compares object identity, whether two names point to the exact same object in memory.

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a
print("a == b:", a == b)
print("a is b:", a is b)
print("a is c:", a is c)
```

```
a == b: True
a is b: False
a is c: True
```

- `a` and `b` hold the same values, so `==` is `True`; they are two separate lists, so `is` is `False`.
- `c = a` doesn't copy anything: it gives the one list a second name, so `a is c` is `True`.

| Tier | What to say |
|---|---|
| Passes | "`is` checks identity, `==` checks equality" (correct, no example of the bug it causes) |
| Strong | The three-way comparison above, and a concrete case where confusing them bites: `if my_list is []:` is **always** `False`, even for an empty list, because `[]` builds a brand-new list, and no existing list can be that new object. Write `if my_list == []:` or, better, `if not my_list:` |
| Extra points | **[+Edge cases]** small integers and short strings are cached by CPython (the standard Python you installed in Chapter 17), so `a = 5; b = 5; a is b` can return `True` purely as an implementation detail, not a language guarantee: never use `is` for values, only for `None`, `True`, and `False`. **[+Validate]** Python itself catches part of this: `n is 1000` makes it print `SyntaxWarning: "is" with a literal. Did you mean "=="?`. It gives no warning for `is []`, which is why that bug survives |

**Likely follow-ups:** Why is `if x is None:` the recommended style over `if x == None:`? What's `__eq__`, and how does defining it change `==` for your own classes?
**Red flag:** using `is` to compare values (numbers, strings, lists) rather than reserving it for identity checks like `is None`.
**Learn it in:** Chapter 17, section 17.5 (`is None`, and what `is` asks); two names for one list is Beyond the book (Q72-001, Q72-026).

### Q72-003 · What's the difference between a shallow copy and a deep copy, demonstrated on nested data?

**Level:** Core · **Beyond the book**

**Remember it as:** *A shallow copy duplicates the outer box. A deep copy duplicates everything inside it too, all the way down.*

**Answer in one line:** `.copy()` (or `copy.copy()`) creates a new outer container, but the *inner* objects it holds are still shared with the original; `copy.deepcopy()` copies everything, level by level, so nothing is shared.

**Beyond the book.** A dictionary holding a list doesn't hold a copy of the list, only a reference to it (the same "two names, one object" as Q72-002). `.copy()` makes a new dictionary with the same references inside. **`copy.deepcopy`**, from the standard library's `copy` module, also copies every list, dictionary, and object inside, however deep. Chapter 43, section 43.7 uses it to copy a whole model before changing it.

```python
import copy
orig = {"items": [1, 2, 3]}
shallow = orig.copy()
deep = copy.deepcopy(orig)
shallow["items"].append(4)
print('orig["items"]:   ', orig["items"])
print('shallow["items"]:', shallow["items"])
print('deep["items"]:   ', deep["items"])
```

```
orig["items"]:    [1, 2, 3, 4]
shallow["items"]: [1, 2, 3, 4]
deep["items"]:    [1, 2, 3]
```

Appending through `shallow` changed `orig` as well, because both dictionaries point at the same inner list. `deep` has its own list and is untouched.

| Tier | What to say |
|---|---|
| Passes | "Deep copy copies everything, shallow copy doesn't" (correct, no demonstration) |
| Strong | The nested-dictionary example above, showing the *original* data changing through a shallow copy of something you thought was safely duplicated |
| Extra points | **[+Validate]** the live proof: changing `shallow["items"]` silently changed `orig["items"]` too, exactly the kind of bug that's easy to miss in a larger program. **[+Business]** this trap shows up with nested configuration dictionaries or lists of records passed between functions: ask "does this container hold other mutable containers?" before reaching for a plain `.copy()` |

**Likely follow-ups:** Does this matter for a flat dictionary with no nested containers? *(No: a shallow copy is completely safe when nothing inside is itself mutable and shared.)* What does `deepcopy` cost on a large nested structure? *(Time and memory in proportion to everything inside it.)*
**Red flag:** assuming `.copy()` always produces a fully independent object.
**Learn it in:** Beyond the book (`copy.deepcopy` in use: Chapter 43, section 43.7).

### Q72-004 · Why does this loop of lambdas return the same value for every function, and how do you fix it?

**Level:** Advanced · **Beyond the book**

**Remember it as:** *A closure remembers the variable, not its value at the time the closure was made. By the time you call it, the loop has already finished.*

**Answer in one line:** A `lambda` created inside a loop refers to the *variable* `i`, not to its value at that point in the loop, so by the time any of the lambdas are called, the loop has finished and every one of them sees `i`'s final value.

**Beyond the book.** A `lambda` is a one-line function without a name (Chapter 18, section 18.6). A function created inside another piece of code can use that code's variables; it is then called a **closure**. It looks the variable up when it *runs*, not when it's created: that is **late binding**.

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])
```

```
[2, 2, 2]
```

- The first line builds three small functions, each returning `i`.
- The second line calls each one. By then the loop is over and `i` is 2, so all three return 2, not 0, 1, 2 as intuition suggests.

**Fixed, by capturing the value as a default argument, which is evaluated at once, when each lambda is made:**

```python
funcs_fixed = [lambda i=i: i for i in range(3)]
print([f() for f in funcs_fixed])
```

```
[0, 1, 2]
```

`lambda i=i:` gives each function its own parameter `i` whose default is the loop's *current* value. Defaults are evaluated once, at definition time (Q72-001), which is exactly the behavior needed here.

| Tier | What to say |
|---|---|
| Passes | "Something about closures" (senses it's a known gotcha, can't explain it or fix it) |
| Strong | The variable-not-value explanation above, and the `lambda i=i:` fix, using the fact that default arguments *are* evaluated once, immediately |
| Extra points | **[+Validate]** both real outputs above: the broken `[2, 2, 2]` and the fixed `[0, 1, 2]`, same loop, one change. **[+Signpost]** this is the same "evaluated once vs. evaluated every time" distinction as Q72-001, showing up as a bug here and as a fix there |

**Likely follow-ups:** Does this happen with a regular `for` loop and `def`, not just `lambda`? *(Yes, the same late binding applies to any nested function.)* What's a cleaner fix than the default-argument trick? *(A small factory function, or `functools.partial`.)*
**Red flag:** not recognizing this as a known, named Python behavior (late-binding closures), and guessing at random causes.
**Learn it in:** Beyond the book (`lambda`: Chapter 18, section 18.6).

### Rapid-fire, §72.1

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q72-005 | *Warm-up.* What's the difference between a list and a tuple? | Lists are mutable, tuples are immutable; tuples can be dictionary keys and set members (if everything inside them is hashable: `([1], 2)` isn't), lists can't | **[+Business]** a tuple signals "this shouldn't change," which is documentation as much as a technical constraint |
| Q72-006 | *Warm-up.* What does Python's `None` represent, and how do you check for it? | The absence of a value; check with `is None`, never `== None` | **[+Edge cases]** `== None` usually works too, but `is None` can't be fooled by a class whose own `__eq__` changes what `==` means |
| Q72-007 | *Core, Beyond the book.* What's the difference between `*args` and `**kwargs`? | In a `def`, `*args` collects extra positional arguments into a tuple; `**kwargs` collects extra keyword arguments into a dictionary | **[+Validate]** run below: `describe(1, 2, 3, name="crate", qty=5)` |
| Q72-008 | *Warm-up.* What's a list comprehension, and is it always faster than a loop? | `[expr for item in iterable if condition]`. Usually faster than the same loop, because it skips looking up and calling `.append` for every item, but not always and not by much: readability is the real reason to use one | **[+Trade-offs]** for big numeric work, vectorized pandas or NumPy beats both (Q72-047) |
| Q72-009 | *Advanced.* What does `__init__` do, and is it a constructor? | It fills in a newly created object's attributes; the object itself is created just before, by `__new__` | **[+Edge cases]** almost nobody overrides `__new__` in data work (it's Beyond the book); knowing it exists is usually enough |

Q72-007, run. The names `args` and `kwargs` are only a convention; the stars do the work:

```python
def describe(*args, **kwargs):
    print("args =", args, "kwargs =", kwargs)

describe(1, 2, 3, name="crate", qty=5)
```

```
args = (1, 2, 3) kwargs = {'name': 'crate', 'qty': 5}
```

The three unnamed values arrive as the tuple `args`, and the two named ones as the dictionary `kwargs`. In a *call*, the stars work the other way round: `f(**settings)` unpacks a dictionary into keyword arguments, as Chapter 54, section 54.5 does.

**Learn it in:** Q72-005 Chapter 17, section 17.4 · Q72-006 section 17.5 · Q72-007 Beyond the book (`**` in a call: Chapter 54, section 54.5) · Q72-008 Chapter 17, section 17.6 · Q72-009 Chapter 29, section 29.5 (`__init__`).

---

## 72.2 Predict the output: basic to advanced tricky questions

The purest interview format: a short snippet, no explanation, just "what does this print, and why." The five core questions come first, easy to hard, then two rapid-fire tables, each easy to hard. Every one below was run; the printed output is real, not a remembered answer.

### Q72-010 · `print(0.1 + 0.2 == 0.3)`: what prints, and why?

**Level:** Warm-up

**Remember it as:** *Computers store most decimals as an approximation in binary, the same way 1/3 has no exact end in decimal. 0.1 and 0.2 already aren't exactly what you typed, before you even add them.*

**Answer in one line:** `False`: floating-point numbers are stored in binary, and most decimal fractions (0.1, 0.2, 0.3 included) have no exact binary form, so tiny rounding errors add up and `0.1 + 0.2` lands a hair away from the stored value of `0.3`.

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

```
0.30000000000000004
False
```

| Tier | What to say |
|---|---|
| Passes | "Floating point is imprecise" (true, no mechanism, can't predict the actual behavior) |
| Strong | The binary-representation explanation above, and the right fix: compare within a small tolerance (`abs(a - b) < 1e-9`, or `round` both first) or use the `decimal` module for money, not `==` |
| Extra points | **[+Validate]** the real printed value above, `0.30000000000000004`, not just "it's not exactly 0.3". **[+Business]** this is why money is safer in `decimal.Decimal` or whole paise than in a raw `float` (the same point Chapter 17, section 17.3 makes, and why Chapter 12 stores money as `NUMERIC`), and why comparing two computed revenue totals with `==` in a test is a bug waiting to happen |

**Likely follow-ups:** How would you safely compare two floats for "close enough"? Does this affect `int` arithmetic the same way? *(No: Python's integers are exact, however large.)*
**Red flag:** claiming this is a Python bug rather than how almost every language stores floating-point numbers (the IEEE 754 standard).
**Learn it in:** Chapter 17, section 17.3 ("Numbers with decimals are approximate"); Chapter 12, section 12.8 for the same test in SQL.

### Q72-011 · `print(0 or 5)` and `print(3 and 5)`: what prints, and why?

**Level:** Core

**Remember it as:** *`and`/`or` in Python don't return True/False. They return whichever actual operand decided the answer.*

**Answer in one line:** `or` returns its first operand if it's truthy, otherwise its second; `and` returns its first operand if it's falsy, otherwise its second. Neither converts its result to a real boolean.

```python
print(0 or 5)           # 5: 0 is falsy, so `or` returns its second operand
print(3 and 5)          # 5: 3 is truthy, so `and` returns its second operand
print([] or 'default')  # an empty list is falsy too
print(None and 'x')     # None is falsy, so `and` stops at it
```

```
5
5
default
None
```

| Tier | What to say |
|---|---|
| Passes | "It returns True or False" (the single most common wrong assumption) |
| Strong | Correctly predicts all four outputs above, explaining that `or`/`and` return an actual operand, not a boolean |
| Extra points | **[+Business]** this is the mechanism behind the idiom `value = user_input or "default"`, using `or` on purpose to provide a fallback (Chapter 29's API client does it with `session or requests.Session()`). **[+Edge cases]** an empty list, an empty string, `0`, and `None` are all falsy and behave identically here, which can surprise someone expecting only `None`/`False` to count, and turns a genuine `0` into the fallback |

**Likely follow-ups:** What's the output of `print(bool(0 or 5))`? What are *all* the falsy values in Python?
**Red flag:** assuming `and`/`or` always produce `True`/`False`.
**Learn it in:** Chapter 17, section 17.5 (`and`, `or`, truthiness); Chapter 29, section 29.9 (`or` as a fallback).

### Q72-012 · `print(2 ** 3 ** 2)`: what prints, and why?

**Level:** Core

**Remember it as:** *Most operators go left to right. The power operator is the odd one out: it goes right to left.*

**Answer in one line:** `512`: `**` is **right-associative** (a chain of them is worked from the right), so this is `2 ** (3 ** 2)` = `2 ** 9` = `512`, not `(2 ** 3) ** 2` = `8 ** 2` = `64`.

```python
print(2 ** 3 ** 2)
print(-2 ** 2)
```

```
512
-4
```

| Tier | What to say |
|---|---|
| Passes | Guesses 64, assuming left to right like most other operators |
| Strong | Correctly computes 512, naming right-associativity as the reason |
| Extra points | **[+Edge cases]** `-2 ** 2` gives `-4`, not `4`, because the minus sign binds *less* tightly than `**`, so it's `-(2 ** 2)`, not `(-2) ** 2`: a second surprise in the same family. **[+Validate]** both real outputs above, together, since they're easy to mix up |

**Likely follow-ups:** What's the full precedence order for arithmetic in Python? How would you force `(2 ** 3) ** 2`? *(With the brackets, exactly as written.)*
**Red flag:** confidently stating `**` works left to right like `+` or `*`.
**Learn it in:** Chapter 17, section 17.3 (`**` is power); the right-to-left rule is Beyond the book and explained above.

### Q72-013 · `a = int("20", 4); print(a)`: what prints, and why?

**Level:** Core

**Remember it as:** *The second argument to `int()` isn't a data type: it's the base the string should be read in. "20" in base 4 means 2 fours plus 0 ones.*

**Answer in one line:** `int(string, base)` reads `string` as a number written in the given base, not base 10, so `"20"` in base 4 means `2×4¹ + 0×4⁰ = 8`.

```python
a = int("20", 4)
print(a)
```

```
8
```

Try changing the base: `int("20", 5)` is two fives, 10, and `int("20", 10)` is plain 20.

| Tier | What to say |
|---|---|
| Passes | Guesses `20` (reading the string as if the base didn't matter), or guesses at random |
| Strong | Correctly computes 8 from place values: digit "2" is in the fours place, digit "0" in the ones place, `2×4 + 0×1 = 8` |
| Extra points | **[+Edge cases]** `int("0x1A", 16)` and `int("0x1A", 0)` both give 26: base 0 tells Python to *infer* the base from a prefix like `0x` (hexadecimal, base 16), `0o` (octal), or `0b` (binary) in the string itself. **[+Business]** this comes up whenever a system hands you IDs, hashes, or flags written in hex or binary as plain text and you need them back as integers |

**Likely follow-ups:** What does `int("20")` give with no second argument? *(20: base 10 is the default.)* What happens with a digit that's invalid for the base, like `int("29", 4)`? *(A `ValueError`, since 9 isn't a base-4 digit.)*
**Red flag:** assuming the second argument changes the *output's* type or format rather than how the *input string* is read.
**Learn it in:** Chapter 17, section 17.3 (`int()`); Chapter 2, section 2.1 (binary). The `base` argument is Beyond the book and explained above.

### Q72-014 · `grid = [[0]*3]*3; grid[0][0] = 1; print(grid)`: what prints, and why?

**Level:** Core · **Beyond the book**

**Remember it as:** *`[[0]*3]*3` makes one inner list, then three references to that same list. Changing "one row" changes all of them at once.*

**Answer in one line:** `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]`: the outer `* 3` doesn't create three independent inner lists, it repeats three references to the *same* inner list, so changing one row through any of them changes what looks like every row.

**Beyond the book.** `*` on a list repeats what the list holds. `[0]*3` repeats a number, which is harmless. `[[0]*3]*3` repeats a *reference to a list*, the same "two names, one object" as Q72-001 and Q72-003.

```python
grid = [[0]*3]*3
grid[0][0] = 1
print(grid)
```

```
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```

**The correct way to build three independent rows:**

```python
grid2 = [[0]*3 for _ in range(3)]
grid2[0][0] = 1
print(grid2)
```

```
[[1, 0, 0], [0, 0, 0], [0, 0, 0]]
```

The comprehension runs `[0]*3` three times, so it builds three separate lists. `_` is the conventional name for a loop variable you don't use.

| Tier | What to say |
|---|---|
| Passes | Predicts `[[1, 0, 0], [0, 0, 0], [0, 0, 0]]`, the intuitive but wrong answer for the broken version |
| Strong | Correctly predicts all three rows changing, and explains it's the same bug family as Q72-003's shallow copy: `*` on a list of lists repeats references, not the lists they point to |
| Extra points | **[+Validate]** both real outputs above, the trap and its fix, side by side. **[+Business]** this is a common bug in anyone's first 2D grid, matrix, or game board in Python, and exactly the kind of thing worth a two-line check before trusting a larger program built on it |

**Likely follow-ups:** Does the same trap apply to `[0, 0, 0] * 3`? *(No: the items are numbers, which can't be changed in place, so there's nothing to share by accident.)* How would you build a 2D NumPy array instead? *(`np.zeros((3, 3))`, which has no such trap.)*
**Red flag:** not recognizing this as the same "shared reference" mechanism as the mutable-default and shallow-copy traps.
**Learn it in:** Beyond the book (lists and comprehensions: Chapter 17, sections 17.4 and 17.6).

### Rapid-fire, §72.2, part A: more predict-the-output, easy to hard

| # | Snippet | Output | Why |
|---|---|---|---|
| Q72-015 | `print(1 < 2 < 3)` | `True` | *Warm-up.* Python chains comparisons: this is `(1 < 2) and (2 < 3)`, with the middle `2` worked out only once |
| Q72-016 | `print('ab' * 3)` | `ababab` | *Warm-up.* `*` on a string repeats it, the same repetition as `*` on a list, just on characters instead of items |
| Q72-017 | `print(sum([]))` and `print(sum([], 10))` | `0` and `10` | *Warm-up.* `sum()`'s second argument is the starting value, 0 by default: useful for a possibly empty list without a separate empty check |
| Q72-018 | `first, *rest = "hello"; print(first, rest)` | `h ['e', 'l', 'l', 'o']` | *Core.* Unpacking works on any iterable, including a string (character by character); the starred name collects everything left over, as a list |
| Q72-019 | `c = int("1000"); d = int("1000"); print(c is d)` | `False` | *Advanced, Beyond the book.* CPython keeps one shared copy of each small integer (about −5 to 256); 1000 is outside that cache, and building each 1000 at run time with `int()` stops Python from merging two identical literals into one constant, so these are two separate objects |
| Q72-020 | `class C: items = []` then `c1 = C(); c1.items.append(1); c2 = C(); print(c2.items)` | `[1]` | *Advanced, Beyond the book.* A mutable **class attribute** (set in the class body, not inside `__init__`) is shared by *every instance*: the class-level cousin of Q72-001's mutable default |
| Q72-021 | `print([x for x in range(5) if (y := x * 2) > 4])` | `[3, 4]` | *Advanced, Beyond the book.* The **walrus operator** `:=` assigns *and* returns a value in one expression, here inside the filter; the list holds the `x` values (not `y`) that pass |

**Learn it in:** Q72-015 Beyond the book · Q72-016 Chapter 17, section 17.3 (`+` on strings) · Q72-017 section 17.4 (`sum`) · Q72-018 section 17.4 (unpacking; the star is Beyond the book) · Q72-019 Beyond the book · Q72-020 Chapter 29, section 29.5 (classes) · Q72-021 Beyond the book.

### Rapid-fire, §72.2, part B: sequences, going deeper

Same quick format, narrowed to one theme: lists, tuples, strings, and the operations that show how they actually differ underneath.

| # | Snippet | Output | Why |
|---|---|---|---|
| Q72-022 | `print(list(zip([1,2,3], [4,5])))` | `[(1, 4), (2, 5)]` | *Warm-up.* `zip()` silently stops at the *shorter* input, with no warning or error: a quiet source of lost data when two "matching" lists aren't the same length |
| Q72-023 | `lst=[0,1,2,3,4,5]; print(lst[5:1:-1])` | `[5, 4, 3, 2]` | *Core.* A negative step walks backward from index 5 down to, but not including, index 1; the stop is still left out, just approached from the other side |
| Q72-024 | `print([1,2,3] + (4,5))` | `TypeError: can only concatenate list (not "tuple") to list` | *Core.* `+` between sequences needs matching types; mixing a list and a tuple is an error, not a silent conversion |
| Q72-025 | `print(sorted([(1,'b'),(1,'a'),(0,'z')], key=lambda x: x[0]))` | `[(0, 'z'), (1, 'b'), (1, 'a')]` | *Core.* Python's sort is **stable**: items that tie on the key keep their original order, so `(1,'b')` stays before `(1,'a')` because it came first |
| Q72-026 | `a=[1,2]; b=a; a+=[3]; print(a, b, a is b)` | `[1, 2, 3] [1, 2, 3] True` | *Core, Beyond the book.* `+=` on a list extends the *same* list in place; `b` sees the change because `a` and `b` are two names for one list |
| Q72-027 | `c=[1,2]; d=c; c=c+[3]; print(c, d, c is d)` | `[1, 2, 3] [1, 2] False` | *Core, Beyond the book.* Plain `+` always builds a *new* list; pointing `c` at it leaves `d` on the original: the direct contrast with Q72-026 |
| Q72-028 | `t=([1,2], 3); t[0].append(99); print(t)` | `([1, 2, 99], 3)` | *Advanced, Beyond the book.* A tuple can't change *what it points to*, but the list `t[0]` points to can still be changed: you can't replace `t[0]`, you can append to it |

**Learn it in:** Q72-022 Chapter 17, section 17.6 (`zip`) · Q72-023 section 17.4 (slices) · Q72-024 section 17.4 (lists and tuples) · Q72-025 section 17.4 (`sorted`), Chapter 18, section 18.6 (`lambda`), and Chapter 33, section 33.7 (stable sorting) · Q72-026 to Q72-028 Beyond the book (Q72-001 and Q72-003 explain the shared reference).

---

## 72.3 Functions, generators, and decorators

### Q72-029 · What's the difference between a function that returns a list and one that's a generator, and why does it matter for a large dataset?

**Level:** Core

**Remember it as:** *A list builds and holds everything in memory at once. A generator hands you one value at a time and forgets it immediately after.*

**Answer in one line:** A function using `return [...]` computes and stores every value at once; a function using `yield` produces values one at a time, on demand, using a small, constant amount of memory however many values there are.

Two ways to make the squares of the first `n` whole numbers:

```python
def squares_list(n):
    return [i*i for i in range(n)]

def squares_gen(n):
    for i in range(n):
        yield i*i
```

A first, rough measure: `sys.getsizeof` gives the size of one object, in bytes.

```python
import sys
print(sys.getsizeof(squares_list(1_000_000)))
print(sys.getsizeof(squares_gen(1_000_000)))
```

```
8448728
208
```

- `1_000_000` is one million; the underscores only make it easier to read.
- The list's 8,448,728 bytes (about 8.4 MB) are only its **slots**, one reference per item. `getsizeof` doesn't count the million numbers those slots point to.
- The generator's size is a small fixed amount, because it hasn't produced anything yet. Python 3.11 prints 208 here; 3.12 and 3.13 print 200.

For the real footprint, measure the peak memory while each version is summed, with **`tracemalloc`**, as Chapter 33, section 33.9 does:

```python
import tracemalloc

tracemalloc.start()
total = sum(squares_list(1_000_000))
list_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.reset_peak()
total = sum(squares_gen(1_000_000))
gen_peak = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

print(f"list peak:      {list_peak / 1e6:.1f} MB")
print(f"generator peak: {gen_peak:,} bytes")
```

```
list peak:      40.4 MB
generator peak: 1,168 bytes
```

- **`tracemalloc.start()`** starts recording memory use; **`get_traced_memory()`** returns the current and the peak amount, in bytes, and `[1]` takes the peak.
- **`reset_peak()`** starts a new peak, so the second measurement is the generator's alone.
- With the numbers counted, the list needs about 40 MB at its peak and the generator a few hundred bytes: roughly 100,000 times less.

| Tier | What to say |
|---|---|
| Passes | "Generators are more memory efficient" (true, no sense of the size of the difference) |
| Strong | The mechanism above, plus the catch: a generator can be read only once, while a list can be looped over again and again |
| Extra points | **[+Validate]** measured, not guessed: about 40 MB for the list against a few hundred bytes for the generator, and **[+Limits]** the honest caveat that `getsizeof` alone understates the list five times over. **[+Scale]** this is why reading a huge file or query result with a generator, or with pandas' `chunksize` (Q72-052), avoids running out of memory on data that would never fit in one list or DataFrame |

**Likely follow-ups:** When would you *not* want a generator, even for a large sequence? *(When you need the values twice, or need `len()` or indexing.)* What's a generator expression, versus a generator function? *(`(i*i for i in range(n))`: the same idea in round brackets, Chapter 33, section 33.2.)*
**Red flag:** not knowing a generator can be consumed only once, or claiming it has no downsides.
**Learn it in:** Chapter 29, section 29.9 ("Step 5: a generator hands out the leads") and Chapter 33, section 33.9 (memory and `tracemalloc`).

### Q72-030 · Write a decorator that times how long a function takes to run

**Level:** Advanced · **Beyond the book**

**Remember it as:** *A decorator is a function that takes a function and returns a new function that wraps it: extra behavior added around the original, without changing the original's own code.*

**Answer in one line:** `@decorator` above a function definition is shorthand for `function = decorator(function)`, and a typical decorator defines an inner `wrapper` function that does something extra, then calls the original inside it.

**Beyond the book.** Chapter 29, section 29.5 *uses* decorators (`@property`, `@classmethod`) and Chapter 33, section 33.8 uses `@lru_cache`; writing one is new. Three ideas make it work. A function can be passed around like any value. A function defined inside another function can use the outer one's names (a closure, Q72-004). And `*args, **kwargs` (Q72-007) let the wrapper accept and pass on whatever arguments the original takes.

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        print(f"{func.__name__} took {t1 - t0:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))
```

- **`timer(func)`** receives the function being decorated and returns `wrapper` in its place.
- **`wrapper(*args, **kwargs)`** starts the stopwatch (`time.perf_counter()`, Chapter 18, section 18.1), calls the original with the same arguments, prints the time, and hands back the original's result unchanged.
- **`@wraps(func)`** keeps `slow_sum`'s own name and docstring on the wrapper (Q72-032).
- **`@timer`** above `def slow_sum` means `slow_sum = timer(slow_sum)`.

Now call it. Timings change on every run, so the first line of the output will differ on your machine:

<!-- run: none -->
```python
result = slow_sum(1_000_000)
print("result:", result)
```

```
slow_sum took 0.011286s
result: 499999500000
```

The result is unchanged by the decorator: 499,999,500,000 is the sum of 0 to 999,999. And thanks to `@wraps`, the decorated function still knows its own name:

```python
print(slow_sum.__name__)
```

```
slow_sum
```

| Tier | What to say |
|---|---|
| Passes | Can describe what a decorator does in English, struggles to write one from scratch |
| Strong | The working `timer` decorator above, using `*args, **kwargs` (Q72-007) so it works on any function's signature, and `@wraps(func)` |
| Extra points | **[+Validate]** the timing line and the unchanged result (499,999,500,000) shown together, proving the decorator adds behavior without changing the return value. **[+Business]** a timing or logging decorator is one of the most common real uses in data code, wrapping pipeline steps to log how long each took |

**Likely follow-ups:** What does `functools.wraps` do, and why add it? *(Q72-032.)* What if the decorated function takes arguments of its own? *(Already handled, by `*args, **kwargs` inside `wrapper`.)*
**Red flag:** a decorator without `*args, **kwargs`, which then works only on functions with one hard-coded signature.
**Learn it in:** Beyond the book (decorators in use: Chapter 29, section 29.5 and Chapter 33, section 33.8).

### Rapid-fire, §72.3

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q72-031 | *Advanced, Beyond the book.* What's a closure? | A function that "remembers" variables from the code it was defined in, even after that outer code has finished running | **[+Signpost]** Q72-004's late-binding bug is a closure behaving exactly as designed; the surprise is *when* the variable is read, not that it's remembered |
| Q72-032 | *Advanced, Beyond the book.* What does `functools.wraps` do inside a decorator? | Copies the original function's name, docstring, and other details onto the wrapper, which would otherwise show the wrapper's own | **[+Business]** without it, error messages and documentation tools show `wrapper` instead of the real function's name, which makes tracebacks confusing |
| Q72-033 | *Core.* What's the difference between a function and a method? | A method is a function defined inside a class; an ordinary method receives the instance (`self`) as its first argument (`@classmethod` receives the class, `@staticmethod` receives neither) | **[+Edge cases]** `@staticmethod` is Beyond the book: a plain function kept inside a class for tidiness |
| Q72-034 | *Core.* What does `*` alone (with nothing after it) do in a function signature? | Every parameter after it must be passed by keyword, not by position | **[+Business]** used in well-designed APIs, like Chapter 29's `CrmClient`, so a caller can't pass several same-typed settings in the wrong order |

**Learn it in:** Q72-031 and Q72-032 Beyond the book · Q72-033 Chapter 29, section 29.5 (methods, `self`, `@classmethod`) · Q72-034 Chapter 29, section 29.9 ("The robust client, as a class").

---

## 72.4 pandas fundamentals: Series, DataFrames, and selection

Every pandas cell from here on needs pandas imported once, as in Chapter 18:

```python
import pandas as pd
print(pd.__version__)
```

```
3.0.6
```

### Q72-035 · What's the difference between a pandas Series and a DataFrame, in one sentence?

**Level:** Warm-up

**Remember it as:** *A Series is one labeled column. A DataFrame is a table of them, sharing a common row index.*

**Answer in one line:** A **Series** is a one-dimensional labeled array (one column, with an index); a **DataFrame** is a two-dimensional table, a collection of Series sharing the same row index, each with its own name and data type.

| Tier | What to say |
|---|---|
| Passes | "A DataFrame is like a table, a Series is like a column" |
| Strong | + explicitly: `df["column"]` returns a Series; selecting several columns (`df[["a", "b"]]`) returns a DataFrame |
| Extra points | **[+Edge cases]** `df["column"]` (single brackets) returns a Series; `df[["column"]]` (double brackets) returns a one-column DataFrame: a common source of "why doesn't this method exist" errors, since Series and DataFrame methods overlap but aren't identical |

**Likely follow-ups:** How would you turn a Series back into a one-column DataFrame? *(`.to_frame()`.)* What does a DataFrame's `.index` represent?
**Red flag:** not knowing the single-bracket vs. double-bracket distinction, or why it matters.
**Learn it in:** Chapter 18, section 18.1 ("DataFrames and Series").

### Q72-036 · Does `SettingWithCopyWarning` still happen in current pandas, and what changed?

**Level:** Core

**Remember it as:** *In pandas 3 every filtered table behaves like its own copy. Changing it never changes the original. To change the original, use `.loc` on it.*

**Answer in one line:** Before pandas 3.0, filtering a DataFrame (`sub = df[condition]`) and then assigning to a column of `sub` might or might not change `df`, and pandas warned `SettingWithCopyWarning`; **pandas 3.0 turns on Copy-on-Write permanently**, so a filtered subset always behaves as its own copy and that warning is gone. Chained assignment (`df[mask]["col"] = x`) now never updates `df`, and pandas warns `ChainedAssignmentError`: write `df.loc[mask, "col"] = x`.

A three-row table:

```python
df = pd.DataFrame({
    "customer": ["A", "B", "C"],
    "category": ["Storage", "Kitchen", "Storage"],
    "quantity": [3, 10, 2],
})
print(df)
```

```
  customer category  quantity
0        A  Storage         3
1        B  Kitchen        10
2        C  Storage         2
```

**Changing a filtered subset** changes the subset only, with no warning:

```python
sub = df[df["category"] == "Storage"]
sub["quantity"] = sub["quantity"] * 2
print(sub)
```

```
  customer category  quantity
0        A  Storage         6
2        C  Storage         4
```

```python
print(df)
```

```
  customer category  quantity
0        A  Storage         3
1        B  Kitchen        10
2        C  Storage         2
```

`sub` has the doubled quantities, and `df` is untouched. That is Copy-on-Write: `sub` shares `df`'s data until one of them is changed, and then gets its own copy.

**Chained assignment**, filtering and assigning in one line, never reaches `df`:

```python
df[df["category"] == "Storage"]["quantity"] = 99
print(df)
```

```
  customer category  quantity
0        A  Storage         3
1        B  Kitchen        10
2        C  Storage         2
```

`df` is unchanged, and beneath the cell pandas prints a warning that starts `ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.` The filter makes a new table, the `= 99` lands on that, and the new table is thrown away.

**The one-step way to change the original** is `.loc[rows, column]`:

```python
df.loc[df["category"] == "Storage", "quantity"] = 99
print(df)
```

```
  customer category  quantity
0        A  Storage        99
1        B  Kitchen        10
2        C  Storage        99
```

| Tier | What to say |
|---|---|
| Passes | Describes the old `SettingWithCopyWarning` trap as if it's still current behavior, without checking the pandas version |
| Strong | Distinguishes the versions: on an older pandas (before 3.0, still common in production code), the warning is real and the safe habit is `.copy()` when you mean a new table and `.loc` when you mean the original; on pandas 3.0+, a filtered subset is always its own copy, chained assignment never updates the original (and warns `ChainedAssignmentError`), and `.loc` is the one way to change `df` |
| Extra points | **[+Validate]** the real outputs above: `sub` changed and `df` provably untouched; the chained version warned and changed nothing; `.loc` changed rows 0 and 2. **[+Business]** confirm which pandas version a team runs before answering either way: this is exactly the kind of fast-changing fact to check, not recite |

**Likely follow-ups:** What is Copy-on-Write, in one sentence? *(Tables share data until one is changed, and the change then happens on a private copy.)* What's the safe pattern on an older pandas you don't control? *(`.copy()` for a new table, `.loc` for the original.)*
**Red flag:** describing `SettingWithCopyWarning` as current behavior without saying which pandas version that applies to.
**Learn it in:** Chapter 18, section 18.4 (the chained-assignment cell and its "Watch out").

### Rapid-fire, §72.4

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q72-037 | *Warm-up.* `.loc` vs. `.iloc`? | Label-based selection (`.loc[row_label, col_label]`) / position-based selection (`.iloc[row_number, col_number]`) | **[+Edge cases]** `.loc`'s slices *include* the end label; `.iloc`'s follow normal Python rules and exclude the end. With the default 0, 1, 2… index, `df.loc[0:2]` returns 3 rows and `df.iloc[0:2]` returns 2 (run below) |
| Q72-038 | *Warm-up.* What does `df.dtypes` tell you, and why check it early? | The data type pandas chose for each column | **[+Business]** a numeric-looking column stored as text (`str` in pandas 3.0+, `object` in earlier versions) usually means non-numeric values mixed in, worth catching before any calculation (Q72-054) |
| Q72-039 | *Warm-up.* How do you check for and count duplicate rows? | `df.duplicated().sum()` counts them; `df[df.duplicated()]` shows them; `df.drop_duplicates()` removes them | **[+Edge cases]** `.duplicated()` treats the *first* occurrence as the original by default; `keep="last"` or `keep=False` change that |
| Q72-040 | *Warm-up.* What's `df.info()` useful for that `df.head()` isn't? | Row count, column types, and non-blank counts per column, all at once: a fast structural health check | **[+Signpost]** the pandas twin of Chapter 71's SQL table-profiling walk-through (Q71-076, section 71.10): one call, several facts about data you've never seen |

Q72-037, run on the three-row `df`:

```python
print(len(df.loc[0:2]), len(df.iloc[0:2]))
```

```
3 2
```

**Learn it in:** Q72-037 Chapter 18, section 18.4 (`loc` and `iloc`) · Q72-038 and Q72-040 section 18.3 · Q72-039 section 18.10.

---

## 72.5 pandas: grouping, joining, and reshaping

The questions in this section and the next use one small table of six orders and four customers, a toy built for the questions, not Riverstone's data. Build and print both first:

```python
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "order_date": pd.to_datetime(["2025-01-05", "2025-01-06", "2025-01-06",
                                  "2025-01-07", "2025-01-08", "2025-01-09"]),
    "customer": ["Sharma Hardware", "Metro Mart", "Sharma Hardware",
                 "Coastal Foods", "Metro Mart", "Sharma Hardware"],
    "category": ["Storage", "Kitchen", "Cleaning", "Storage", "Kitchen", "Storage"],
    "quantity": [3, 10, 4, 5, 2, 2],
    "unit_price": [320.0, 85.0, 90.0, 980.0, 260.0, 320.0],
})
customers = pd.DataFrame({
    "customer": ["Sharma Hardware", "Metro Mart", "Coastal Foods", "Home Plus"],
    "city": ["Pune", "Mumbai", "Chennai", "Delhi"],
})
print(orders)
print(customers)
```

```
   order_id order_date         customer  category  quantity  unit_price
0         1 2025-01-05  Sharma Hardware   Storage         3       320.0
1         2 2025-01-06       Metro Mart   Kitchen        10        85.0
2         3 2025-01-06  Sharma Hardware  Cleaning         4        90.0
3         4 2025-01-07    Coastal Foods   Storage         5       980.0
4         5 2025-01-08       Metro Mart   Kitchen         2       260.0
5         6 2025-01-09  Sharma Hardware   Storage         2       320.0
          customer     city
0  Sharma Hardware     Pune
1       Metro Mart   Mumbai
2    Coastal Foods  Chennai
3        Home Plus    Delhi
```

`pd.to_datetime` turns the date text into real dates (Chapter 18, section 18.9). Home Plus is in `customers` but has no orders, on purpose.

### Q72-041 · Group the orders by customer, computing total revenue, order count, and average quantity in one call

**Level:** Core

**Remember it as:** *`.agg()` with named outputs beats calling `.sum()`, `.count()`, and `.mean()` separately: one grouping step, self-documenting column names.*

**Answer in one line:** `.groupby(col).agg(name=("column", "function"), ...)` computes several aggregations, on different columns if you like, from one grouping step, with output column names you choose.

```python
orders["revenue"] = orders["quantity"] * orders["unit_price"]
print(orders.groupby("customer").agg(
    total_revenue=("revenue", "sum"),
    orders=("order_id", "count"),
    avg_qty=("quantity", "mean"),
))
```

```
                 total_revenue  orders  avg_qty
customer                                       
Coastal Foods           4900.0       1      5.0
Metro Mart              1370.0       2      6.0
Sharma Hardware         1960.0       3      3.0
```

- The first line adds a `revenue` column, quantity times price, row by row.
- **`total_revenue=("revenue", "sum")`** reads "a column called `total_revenue`, made by summing `revenue`". **`orders=("order_id", "count")`** counts each customer's order IDs, and **`avg_qty=("quantity", "mean")`** averages their quantities.

| Tier | What to say |
|---|---|
| Passes | Three separate `.groupby().sum()`, `.groupby().count()`, `.groupby().mean()` calls, then joining the results by hand: works, but three groupings and more code to keep in step |
| Strong | The single `.agg()` call above, with named outputs |
| Extra points | **[+Validate]** the output reconciles by hand: Sharma Hardware's three orders are 3 × 320 + 4 × 90 + 2 × 320 = 1,960, with quantities 3, 4, and 2 averaging 3.0; Metro Mart's are 10 × 85 + 2 × 260 = 1,370. **[+Business]** named aggregation gives readable column names at once, where the older `.agg({"revenue": "sum"})` style leaves you renaming columns afterwards |

**Likely follow-ups:** How would you group by *two* columns at once? What's the difference between `.agg()` and `.transform()`? *(Q72-046.)*
**Red flag:** running several separate `.groupby()` calls and merging the results by hand, instead of one `.agg()` call.
**Learn it in:** Chapter 18, section 18.6 (named aggregation).

### Q72-042 · Merge an orders table with a customers table, and find any customer with zero orders

**Level:** Core

**Remember it as:** *An inner join only shows what matches on both sides. Finding "nothing matched" needs a left join from the side you want to keep, checked for the rows that found no partner: the pandas version of Chapter 71's SQL LEFT JOIN / IS NULL pattern.*

**Answer in one line:** `customers.merge(orders, on="customer", how="left", indicator=True)`, then keep the rows whose `_merge` column says `left_only`: customers with no matching order, exactly the SQL `LEFT JOIN ... WHERE ... IS NULL` of Chapter 71 (Q71-001).

```python
m = customers.merge(orders, on="customer", how="left", indicator=True)
print(m[m["_merge"] == "left_only"][["customer", "city"]])
```

```
    customer   city
6  Home Plus  Delhi
```

- **`how="left"`** keeps every customer, with or without orders; customers with orders appear once per order.
- **`indicator=True`** adds a `_merge` column saying where each row came from: `both`, or `left_only` when no order matched.
- The filter keeps the `left_only` rows, and `[["customer", "city"]]` shows two columns. Home Plus is row 6 because the six rows for customers with orders come first.

The same answer, with the tables the other way round, is `how="right"` checked for a missing `order_id`:

```python
merged_right = orders.merge(customers, on="customer", how="right")
print(merged_right[merged_right["order_id"].isna()][["customer", "city"]])
```

```
    customer   city
6  Home Plus  Delhi
```

| Tier | What to say |
|---|---|
| Passes | `orders.merge(customers, on="customer")` with the default `how="inner"`: silently drops customers with no orders instead of surfacing them |
| Strong | The `how="left"`, `indicator=True` version above, finding the one customer (Home Plus) with no orders |
| Extra points | **[+Validate]** also check that the plain inner merge keeps every order: its row count equals `orders`'s (run below: 6 and 6), so no order was dropped for lack of a known customer. **[+Edge cases]** the same fan-out risk as Chapter 71's SQL joins: a duplicate `customer` in `customers` would silently multiply the matching order rows, because `merge` follows the same join rules as SQL; `validate="many_to_one"` makes pandas stop instead |

```python
print(len(orders.merge(customers, on="customer")), len(orders))
```

```
6 6
```

**Likely follow-ups:** How would you do this with `how="outer"`, and what changes? *(Unmatched rows from both sides appear, marked `left_only` or `right_only`.)*
**Red flag:** using the default inner merge and never checking whether any expected rows disappeared.
**Learn it in:** Chapter 18, section 18.7 (`merge`, `indicator=True`, fan-out) and Chapter 71, section 71.1 for the SQL side.

### Rapid-fire, §72.5

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q72-043 | *Core.* `pivot_table` vs. `groupby`? | `pivot_table` reshapes grouped results into a wide table (categories become columns) / `groupby` keeps results long | **[+Validate]** run below: each customer's spend lands under the right category column, zeros elsewhere |
| Q72-044 | *Warm-up.* What does `fill_value=0` do in `pivot_table`, and why not leave the default? | Fills cells with no matching data (a customer-category pair that never happened) with 0 instead of `NaN` | **[+Edge cases]** a `NaN` left in a pivot meant for summing or charting can break later arithmetic; 0 is usually the right "this didn't happen" |
| Q72-045 | *Warm-up.* What's `pd.concat()` for, and how is it different from `merge`? | Stacks DataFrames, by rows (the default) or columns, by position, not by matching key values | **[+Signpost]** `concat` is pandas' `UNION ALL` (Chapter 71, Q71-006); `merge` is pandas' `JOIN` |
| Q72-046 | *Core.* What does `.transform()` do that `.agg()` doesn't? | Returns one value per original row (each row gets its group's result), rather than one row per group | **[+Business]** useful for adding "this row's share of its group's total" directly onto the original, uncollapsed table |

Q72-043, run:

```python
print(orders.pivot_table(index="customer", columns="category",
                         values="revenue", aggfunc="sum", fill_value=0))
```

```
category         Cleaning  Kitchen  Storage
customer                                   
Coastal Foods         0.0      0.0   4900.0
Metro Mart            0.0   1370.0      0.0
Sharma Hardware     360.0      0.0   1600.0
```

- **`index="customer"`** gives one row per customer, and **`columns="category"`** one column per category.
- **`values="revenue"`** with **`aggfunc="sum"`** puts the total revenue of each customer-category pair in its cell: Sharma Hardware's 1,600 in Storage is 3 × 320 + 2 × 320.
- **`fill_value=0`** writes 0 where a pair never happened. Leave it out and those cells show `NaN` instead (Q72-044).

**Learn it in:** Q72-043 and Q72-044 Chapter 18, section 18.8 · Q72-045 section 18.7 · Q72-046 section 18.6 (`transform`).

---

## 72.6 pandas: performance, missing data, strings, and dates

### Q72-047 · Why is `.apply()` with `axis=1` almost always slower than a vectorized operation, and how much slower in practice?

**Level:** Core

**Remember it as:** *`.apply(axis=1)` is a Python for-loop in disguise. Vectorized pandas operations run in fast, compiled code underneath, on the whole column at once.*

**Answer in one line:** `.apply(func, axis=1)` calls `func` once per row, in plain Python, as slow as an explicit loop; a vectorized operation (`df["a"] * df["b"]`) works on whole columns at once in compiled code, with no Python loop at all.

A table of 200,000 rows, built without NumPy:

```python
big = pd.DataFrame({"a": range(200_000), "b": range(200_000)})
print(big.shape)
```

```
(200000, 2)
```

Now time both ways with Chapter 18's stopwatch, `time.perf_counter()`. Timings change on every run and every machine, so this cell's numbers will differ on yours:

<!-- run: none -->
```python
import time

t0 = time.perf_counter()
r1 = big.apply(lambda row: row["a"] * row["b"], axis=1)   # row by row
t1 = time.perf_counter()
r2 = big["a"] * big["b"]                                  # vectorized
t2 = time.perf_counter()

print(f"apply:      {t1 - t0:.4f} s")
print(f"vectorized: {t2 - t1:.6f} s")
print(f"speedup:    {(t1 - t0) / (t2 - t1):,.0f}x")
```

```
apply:      0.9891 s
vectorized: 0.001292 s
speedup:    766x
```

Fast is only useful if the answer is the same. Check every row:

```python
r1 = big.apply(lambda row: row["a"] * row["b"], axis=1)
r2 = big["a"] * big["b"]
print((r1 == r2).all())
```

```
True
```

`r1 == r2` compares the two columns row by row, and `.all()` is `True` only if every one of the 200,000 rows matches.

| Tier | What to say |
|---|---|
| Passes | "Vectorized code is faster" (true, no sense of *how much*, no explanation) |
| Strong | The compiled-code-versus-Python-loop explanation above, identifying `.apply(axis=1)` as a loop wearing a pandas costume |
| Extra points | **[+Validate]** measured, not asserted: several hundred times faster on the machine used for this book (766× in the run above; your number will differ), with every row checked to match. **[+Business]** on a large table this is the difference between a report that runs in a second and one that takes minutes, with no change to the logic |

**Likely follow-ups:** Is `.apply()` ever the right choice? *(Yes, when the per-row logic genuinely can't be vectorized: complex branching, or calling an outside function per row.)* Is `.apply()` on a single column faster than the row-wise version? *(Yes, but still a loop: look for a `.str`, `.dt`, `.map`, or arithmetic equivalent first.)*
**Red flag:** reaching for `.apply(axis=1)` for row-wise arithmetic that could be a direct column operation.
**Learn it in:** Chapter 18, section 18.1 ("Whole columns, not loops"), section 18.5 (`.apply`, "a loop wearing a costume"), and section 18.16.

### Q72-048 · Handle missing data in a numeric column: detect it, then decide between filling and dropping

**Level:** Core

**Remember it as:** *Detect first, decide second. Filling and dropping are both valid, but only after you know how much is missing and why.*

**Answer in one line:** `.isna().sum()` counts missing values; `.fillna(value)` replaces them (a mean, median, zero, or a forward fill, depending on context); `.dropna(subset=[...])` removes rows missing a required value. The right choice depends on *why* the data is missing, not on habit.

First, a copy of `orders` with one price blanked out, so there is something to find:

```python
orders2 = orders.copy()
orders2.loc[2, "unit_price"] = None
print(orders2["unit_price"].isna().sum())
```

```
1
```

- **`.copy()`** makes `orders2` a separate table, so `orders` keeps its prices.
- **`.loc[2, "unit_price"] = None`** blanks the price at index 2, the third row. pandas stores the blank as `NaN`.
- **`.isna().sum()`** counts the blanks: one.

Filling with the mean of the prices that are there:

```python
print(orders2["unit_price"].fillna(orders2["unit_price"].mean()).tolist())
```

```
[320.0, 85.0, 393.0, 980.0, 260.0, 320.0]
```

The blank at index 2 became 393.0, the mean of the five known prices: (320 + 85 + 980 + 260 + 320) ÷ 5 = 1,965 ÷ 5 = 393. `.tolist()` prints the column as a plain list.

Dropping instead:

```python
print(orders2.dropna(subset=["unit_price"]).shape)
```

```
(5, 7)
```

`subset=["unit_price"]` drops only rows with a blank *price*; the result has 5 rows and all 7 columns.

| Tier | What to say |
|---|---|
| Passes | "Use `.fillna()` or `.dropna()`" with no discussion of when each fits |
| Strong | + explicitly: filling with a mean or median is reasonable when a value is plausibly missing at random and you need every row later; dropping is more honest when a blank means something you don't want to guess at, and losing a few rows doesn't bias the analysis |
| Extra points | **[+Business]** a silent fill can hide a real data-quality problem from everyone who reads the numbers later: pair a fill with a comment or a `was_imputed` column when it matters. **[+Edge cases]** the mean is computed from whatever rows exist *now*; fill before you've settled the final row set and you bake in a slightly wrong mean |

**Likely follow-ups:** When would forward fill (`.ffill()`) fit better than a mean? *(A reading that holds until it changes, such as a price list over time.)* How would you handle blanks in a text column? *(A label such as "(unknown)", as Chapter 18 does for missing reps.)*
**Red flag:** filling every missing value with 0 by default, whatever the column means.
**Learn it in:** Chapter 18, sections 18.3 (`.isna()`), 18.5 (`.fillna()`), and 18.10 (cleaning); Chapter 14 for deciding what to do with blanks.

### Rapid-fire, §72.6

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q72-049 | *Warm-up.* Extract the first word of each customer name using `.str`? | `df["customer"].str.split().str[0]` | **[+Validate]** run below: "Sharma Hardware" → "Sharma", "Metro Mart" → "Metro" |
| Q72-050 | *Warm-up.* Get the day of the week from a date column? | `df["date"].dt.day_name()`, or `.dt.dayofweek` for a number from 0 (Monday) to 6 | **[+Validate]** run below: 2025-01-05 → "Sunday", 2025-01-06 → "Monday" |
| Q72-051 | *Core.* What does `.str.contains("text")` give for a missing value? | **pandas 3.0+ (`str` dtype):** `False`. **Older pandas, or an `object` column:** a missing value (`None`/`NaN`), and using that result as a filter raises `ValueError: Cannot mask with non-boolean array containing NA / NaN values` | **[+Edge cases]** pass `na=False` and both versions behave the same: a missing value counts as "no match" |
| Q72-052 | *Core.* How would you process a file too large to fit in memory, using pandas? | `pd.read_csv(path, chunksize=100_000)` returns an iterator of DataFrame pieces, processed one at a time | **[+Scale]** the pandas version of Q72-029's generator idea: memory stays bounded however big the file is |

Q72-049 and Q72-050, run on the first two orders:

```python
print(orders["customer"].str.split().str[0].head(2).tolist())
print(orders["order_date"].dt.day_name().head(2).tolist())
```

```
['Sharma', 'Metro']
['Sunday', 'Monday']
```

Q72-051, the two behaviors side by side. The first Series gets pandas 3's `str` dtype; `dtype=object` makes the second behave like older pandas:

```python
names = pd.Series(["Sharma Hardware", None, "Metro Mart"])
old_style = pd.Series(["Sharma Hardware", None, "Metro Mart"], dtype=object)
print(names.dtype, names.str.contains("Mart").tolist())
print(old_style.dtype, old_style.str.contains("Mart").tolist())
print(old_style.str.contains("Mart", na=False).tolist())
```

```
str [False, False, True]
object [False, None, True]
[False, False, True]
```

- **`names`** is an ordinary Series of text, so pandas 3 gives it the `str` dtype, and the missing name gives `False`.
- **`dtype=object`** forces the older, generic type: now the missing name gives `None`, which is neither `True` nor `False`, so `old_style[old_style.str.contains("Mart")]` would stop with the `ValueError` in the table.
- **`na=False`** says "count a missing value as no match", and the result is the same in both versions.

**Learn it in:** Q72-049 Chapter 18, section 18.5 (the `.str` accessor; `.str.split` and `.str.contains` are Beyond the book) · Q72-050 section 18.9 · Q72-051 Beyond the book · Q72-052 section 18.13 (`chunksize` on a database read; the same option works on `read_csv`).

---

## 72.7 Debugging and live-coding walk-throughs

### Q72-053 · Fix this function: it's supposed to return each customer's share of total revenue, but it always returns 0 or 1

**Level:** Warm-up

**Remember it as:** *`//` throws away everything after the decimal point, and a share is always below 1, so it becomes 0.*

```python
# BROKEN
def revenue_share(customer_revenue, total_revenue):
    return customer_revenue // total_revenue

print(revenue_share(1960, 8230))
```

```
0
```

**What's wrong:** `//` is whole-number (floor) division, not ordinary division. Any `customer_revenue` smaller than `total_revenue` floors to 0, and a customer who is the whole total gets 1: it can never return a fraction like 0.24.

```python
# FIXED
def revenue_share(customer_revenue, total_revenue):
    return customer_revenue / total_revenue

print(revenue_share(1960, 8230))
```

```
0.23815309842041313
```

| Tier | What to say |
|---|---|
| Diagnosis | `//` floors instead of dividing |
| Fix | A one-character change, `//` to `/` |
| Extra points | **[+Validate]** test with real numbers: Sharma Hardware's 1,960 against the toy table's total of 8,230 (Q72-041: 4,900 + 1,370 + 1,960) gives `0` broken and about `0.238` fixed. **[+Edge cases]** check `total_revenue == 0` separately either way: both `/` and `//` raise `ZeroDivisionError` on a zero total, and a customer total of zero is worth investigating on its own |

**Likely follow-ups:** How is `/` in Python 3 different from Python 2's? *(In Python 2, `/` on two whole numbers floored, like `//`.)* How would the same bug look in pandas, on a whole column? *(`df["revenue"] // total`, and the same fix.)*
**Red flag:** not recognizing `//` as floor division at once, or hunting for something more complicated than the operator.
**Learn it in:** Chapter 17, section 17.3 (`//` is whole-number division).

### Q72-054 · Walk-through: clean and validate a messy, realistic order export

**Level:** Core

**What they're really testing:** whether you have a repeatable process for a messy real file, not just a single trick.

**Talked through live:** "I'll check shape and dtypes first, look for duplicates, check for missing values column by column, and only then start fixing anything, since fixing before I understand what's wrong risks masking a bigger problem."

A deliberately messy small export:

```python
messy = pd.DataFrame({
    "order_id": [1001, 1002, 1002, 1004, 1005],
    "customer": [" Sharma Hardware", "Metro Mart", "Metro Mart",
                 "Coastal Foods", "Home Plus"],
    "quantity": ["3", "10", "10", "ten", None],
})
print("duplicate order_ids:", messy.duplicated(subset=["order_id"]).sum())
print("quantity dtype:", messy["quantity"].dtype)
print("missing quantities:", messy["quantity"].isna().sum())
print("names with a leading space:", messy["customer"].str.startswith(" ").sum())
```

```
duplicate order_ids: 1
quantity dtype: str
missing quantities: 1
names with a leading space: 1
```

- **`.duplicated(subset=["order_id"])`** marks each row whose `order_id` appeared earlier: order 1002 is there twice.
- **The dtype is `str`**: `quantity` is stored as text, not numbers, because one value is the word "ten".
- **One quantity is missing** (order 1005).
- **`.str.startswith(" ")`** finds the leading space in " Sharma Hardware", which would break an exact-match join.

**The fix, applied in order:**

```python
clean = messy.drop_duplicates(subset=["order_id"]).copy()
clean["customer"] = clean["customer"].str.strip()
clean["quantity"] = pd.to_numeric(clean["quantity"], errors="coerce")
print(clean)
print(clean.dtypes)
```

```
   order_id         customer  quantity
0      1001  Sharma Hardware       3.0
1      1002       Metro Mart      10.0
3      1004    Coastal Foods       NaN
4      1005        Home Plus       NaN
order_id      int64
customer        str
quantity    float64
dtype: object
```

- **`.drop_duplicates(subset=["order_id"])`** keeps the first copy of order 1002. **`.copy()`** makes `clean` its own table on purpose; on pandas before 3.0 it also avoids the `SettingWithCopyWarning` of Q72-036 on the next two lines.
- **`.str.strip()`** removes the leading space.
- **`pd.to_numeric(..., errors="coerce")`** turns text into numbers, and anything it can't read, here "ten", into `NaN` instead of stopping. The missing quantity stays missing.
- **`quantity` is now `float64`** (3.0, 10.0): a column of whole numbers with a blank in it becomes decimal numbers, because `NaN` is a float.

To keep whole numbers alongside blanks, use pandas' nullable integer type, `"Int64"` with a capital I:

```python
print(clean["quantity"].astype("Int64").tolist())
```

```
[3, 10, <NA>, <NA>]
```

`.astype("Int64")` converts the column to that type: 3 and 10 are whole numbers again, and the two blanks show as `<NA>`, pandas' own missing-value marker. `.tolist()` prints the column as a list.

**Extra-points moves demonstrated:** **[+Signpost]** diagnosed before fixing, in a stated order. **[+Validate]** every claim (a duplicate, a text dtype, a missing value, a leading space) backed by a check that printed a number, not assumed. **[+Edge cases]** `errors="coerce"` turned the genuinely bad value "ten" into a `NaN` that can be counted and reported, instead of crashing the whole pipeline.

**Likely follow-ups:** How would you decide whether to keep the first or the last copy of a duplicate order? What would you do with the two `NaN` quantities now? *(Report them, with the order IDs, before deciding to fill or drop: Q72-048.)*
**Red flag:** starting to "fix" a file (dropping rows, filling values) before running any checks on what's wrong with it.
**Learn it in:** Chapter 18, section 18.10 (cleaning in pandas) and Chapter 14; Chapter 71's table-profiling walk-through (Q71-076, section 71.10) for the same discipline in SQL.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A mutable default argument (`def f(x, items=[])`) | Calls silently accumulate state across unrelated calls | Use `items=None`, then `if items is None: items = []` inside |
| Using `is` to compare values | `if x is []:` never matches, even for an empty list | Keep `is` for `None`/`True`/`False`; use `==` for values |
| Assuming `.copy()` fully isolates nested data | Changing a "copy" silently changes the original too | Use `copy.deepcopy()` when the container holds other mutable containers |
| Citing `SettingWithCopyWarning` as current pandas behavior with no version check | Confidently wrong on pandas 3.0+, where Copy-on-Write is always on | Say which pandas version the answer applies to |
| Chained assignment (`df[mask]["col"] = x`) | Nothing changes in `df`; pandas 3 warns `ChainedAssignmentError` | `df.loc[mask, "col"] = x` |
| `.apply(axis=1)` for simple row-wise arithmetic | Hundreds to thousands of times slower than the vectorized version | Direct column operations (`df["a"] * df["b"]`) whenever possible |
| Inner-joining without checking for dropped rows | Missing customers or records go unnoticed | Compare row counts before and after; use `how="left"` with `indicator=True` when rows shouldn't disappear |
| Filling every missing value with 0 by habit | Real "unknown" values are treated as real zeros in later math | Decide fill vs. drop based on *why* the value is missing |
| "Fixing" a messy file before diagnosing it | Over-correcting, or missing the real problem | Check shape, dtypes, duplicates, and missing values first, in that order |

---

## In the real world: the report that "randomly" gave different numbers each run

Karan is asked to debug a weekly revenue report that sometimes produces a slightly different, lower total for the same underlying data, whenever the report ran more than once in the same session. He traces it to a helper function with a mutable default argument, exactly Q72-001's bug, used to accumulate a running list of "already counted" order IDs. The list was meant to reset for every report run, but never did, since the default list was created once, when the module was first imported, so every later run skipped the orders the earlier runs had counted.

The fix was the one-line change Q72-001 already teaches (`orders_seen=None` instead of `orders_seen=[]`), but the part that mattered in the interview retelling wasn't the fix, it was how Karan found it: rather than guessing, he added a single `print(len(orders_seen))` at the top of the function and ran the report twice in the same Python session, watching the count grow between runs when it should have reset to zero each time. That one line of evidence turned a vague "it's inconsistent somehow" into an exact, provable diagnosis in under two minutes.

The lesson the hiring manager wrote in her notes afterward: *"Didn't guess. Added one line to make the invisible state visible, then the bug explained itself."* That's Chapter 69's Move 7 (validate), applied to debugging instead of a finished answer, and it's exactly the difference this chapter's format tries to model in every question: don't just know the fix, show the evidence.

---

## Project

**Goal:** find and fix a real instance of at least three of this chapter's core bugs, in your own code or a public repository.

### Tools you'll need

**Python** and the book's virtual environment from Chapter 17, section 17.0 (the book recommends Python 3.14; this chapter's snippets were run on Python 3.11.15, and the generator sizes of Q72-029 also on 3.12 and 3.13), and **pandas** 3.0 or later (run on 3.0.6). `%timeit` in a Jupyter notebook, or the `time.perf_counter()` pattern used in this chapter, for any performance claim you make in an interview, rather than quoting a speedup from memory. **pandas' own release notes** are worth skimming before an interview at a company that uses pandas heavily, since behavior (like Copy-on-Write, Q72-036) does change between major versions.

1. Search your own past projects for a mutable default argument (`def f(x, y=[])` or `y={}`) and fix it, the way Q72-001 does.
2. Take one place in your own code that uses `.apply(axis=1)` and rewrite it as a vectorized operation; measure the real speedup and check the results match, the way Q72-047 does.
3. Pick a merge in your own work and verify the row count is what you expect, catching any silently dropped or duplicated rows (Q72-042).
4. Run `.isna().sum()` on a real dataset you have access to, and for each column with missing data, decide and justify fill vs. drop, in one sentence each.
5. Write one decorator of your own (logging, timing, or retry logic) and apply it to a real function you use regularly (Q72-030).

---

## Key terms

mutable default argument · `is` vs. `==` · object identity · shallow copy · deep copy · closure · late binding · `*args` / `**kwargs` · keyword-only arguments (`*`) · list comprehension · generator · `tracemalloc` · decorator · `functools.wraps` · class attribute · walrus operator (`:=`) · pandas Series · pandas DataFrame · `.loc` vs. `.iloc` · Copy-on-Write · chained assignment · `ChainedAssignmentError` · `SettingWithCopyWarning` (legacy) · `groupby().agg()` · named aggregation · `merge` (join types) · `indicator=True` · `pivot_table` · `concat` · `.transform()` vs. `.agg()` · vectorization · `.apply(axis=1)` · `.isna()` / `.fillna()` / `.dropna()` · `.str` accessor · `.dt` accessor · `errors="coerce"` · nullable `Int64` · `chunksize` (large-file reading)

---

## Final-week revision list

Q72-001, Q72-002, Q72-003, Q72-004, Q72-029, Q72-030, Q72-035, Q72-036, Q72-041, Q72-042, Q72-047, Q72-048, Q72-053, Q72-054.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 71, SQL Question Bank,** already covered the join-cardinality and NULL-handling logic this chapter's pandas `merge` questions (section 72.5) reuse.
- **Chapter 72A, Data Structures & Algorithms Question Bank,** covers the classic algorithm problems (arrays, trees, graphs) this chapter leaves aside in favor of pandas-specific, data-role-shaped coding.
- **Chapter 74, Machine Learning Question Bank,** assumes this chapter's pandas fluency as a starting point, not something to re-teach.
