# Chapter 57. LLMOps

*Part 6 — Production ML, Generative AI & MLOps*

> **Chapter at a glance**
>
> **You will learn to:** name what LLMOps adds to Chapter 56's discipline, and why the model you depend on isn't yours · keep prompts in a registry as versioned code with a score attached · run a golden set in CI with a floor that fails the build · survive the day a provider ships a new model version · build a token meter and project a monthly bill · build a cache, and measure what it saves on real traffic · budget latency · retry, fall back, and degrade honestly when the provider fails · monitor a system that has no accuracy to monitor · keep logs that are useful and lawful · and run the human review loop that turns complaints into test cases.
>
> **Before you start:** Chapter 54 (prompting, structured output, token costs, the order-extraction golden set), Chapter 55 (the support assistant, its test questions, guardrails), Chapter 56 (versioning, serving, monitoring, retraining, incidents), Chapter 29 (classes, retries and backoff, exit codes), Chapter 45 (hashes).
>
> **Time needed:** 16–20 hours, spread over three weeks: sections 57.0 to 57.4 in the first, 57.5 to 57.8 in the second, and 57.9 to 57.11 with the project in the third.
>
> **Tools:** Python with the standard library only for this chapter's own code; Chapter 55's assistant, which uses NumPy and scikit-learn, in section 57.9. The provider is Chapter 54's local stand-in, extended so that a new model version and a failure rate can be simulated offline. No API key is needed.
>
> **Practice systems:** Chapter 54's order-extraction pipeline (60 emails with known answers) and Chapter 55's support assistant, plus eight weeks of incoming questions built by `questions_stream.py`.

---

## Why this matters

Chapter 56 kept a model alive that you trained, on data you own, with an accuracy you can measure. An LLM feature breaks all three of those assumptions:

- **You don't own the model.** It can change behind the same name, be deprecated with 60 days' notice, or rate-limit you at the worst moment.
- **There is no accuracy.** The output is text. For Riverstone's extraction pipeline you can build ground truth; for the support assistant, "was that a good answer?" is a judgment, and judgment doesn't come in a dashboard.
- **The cost is per request, forever.** A model you host has a fixed bill; a model you call has one that scales with success.

The discipline that answers this is the same shape as Chapter 56 and a different set of controls. It is also, right now, the difference between the AI features that are still running a year after the demo and the ones that were quietly switched off.

---

## In plain English

**You have built a business process on somebody else's engine, and you can't open the bonnet.**

That's not a reason to avoid it. It is a reason to build four things around it:

- **A test you trust.** A set of inputs with known right answers, run on every change, including changes you didn't make. It is the only way to notice that the engine was swapped.
- **A meter.** Tokens in, tokens out, per request, so the bill is a number you predicted rather than one that arrives.
- **A spare.** Retries, a cheaper model, and a degraded mode that still serves customers when the provider is down.
- **A way to hear complaints.** With no accuracy to measure, the fastest signal is the person who says "that answer was wrong", and the job is to make that cheap to say and impossible to lose.

The rest is Chapter 56's discipline with two extra things versioned: **the prompt**, and **the model you don't control**.

---

## 57.0 Setting up

Nothing new needs installing. This chapter's code uses only Python's standard library, and Chapter 55's assistant needs NumPy (Chapter 18) and scikit-learn (Chapter 35, section 35.9), which you already have. It also reuses two earlier companion folders, so they must be in place first: `companion/ch54` with its `order_data/` folder (made by `generate_order_emails.py` in section 54.0), and `companion/ch55` with its `corpus/` folder (made in section 55.0).

Open a terminal, activate the book's virtual environment (Chapter 17, section 17.0), go to `companion/ch57`, and start Jupyter there. Run every cell in this chapter in order, in one notebook: each uses names made by the cells before it. The folder holds four files:

| File | What it is |
|---|---|
| `provider.py` | the one function that talks to the model, `call`, wrapped around Chapter 54's stand-in, with this chapter's meter |
| `pipeline.py` | everything this chapter builds, cell by cell, saved as one module so a script can import it |
| `questions_stream.py` | eight weeks of questions arriving at Chapter 55's assistant |
| `ci_eval.py` | the golden set as a build step, for exercise 5 |

The first cell tells Python where the two earlier folders are and loads Chapter 54's golden set:

```python
import sys
from pathlib import Path

CH54 = Path("../ch54").resolve()
CH55 = Path("../ch55").resolve()
sys.path.insert(0, str(CH54))
sys.path.insert(0, str(CH55))

from extraction import NAIVE, INSTRUCTED, WITH_EXAMPLE, parse, mark, truth, emails
print(f"{len(truth)} emails with known answers, from {CH54.name}/order_data")
```

```
60 emails with known answers, from ch54/order_data
```

**Line by line:**

- `Path("../ch54")` is the folder next to this one: `..` means "one folder up" (Chapter 26, section 26.0). `.resolve()` turns it into the full path, so it still works if the notebook's working folder changes later.
- `sys.path` is the list of folders Python searches for modules (Chapter 54, section 54.6). `sys.path.insert(0, str(CH54))` puts the Chapter 54 folder at the front, so `import` finds its files; `str()` turns the path into the text form `sys.path` expects. The Chapter 55 folder goes in the same way, for section 57.9.
- `extraction.py` is Chapter 54's evaluation code saved as a module (Chapter 54, answer 14). From it come the three prompts of section 54.6 (`NAIVE`, `INSTRUCTED`, `WITH_EXAMPLE`), `parse` (find the JSON object in a reply), `mark` (the four checks against the truth), and the two dictionaries `truth` and `emails`, both keyed by email name.

### What the stand-in provider does

`provider.py` has one function every other piece calls, `call(prompt, model=...)`. It answers with Chapter 54's `mock_llm.complete`, so the replies behave exactly as they did in Chapter 54, and it adds three things a real provider has:

| The provider's feature | What it does here |
|---|---|
| **Model versions** | `"workhorse-001"` is the version Riverstone tested and pinned; `"workhorse-002"` is the provider's next version, with two new habits (section 57.4); `"volume-001"` is a cheaper model (section 57.8) |
| **A meter** | `call(..., meter=m)` records the tokens of every call in `m` (section 57.5) |
| **Failures** | `call(..., failure_rate=0.2)` makes about a fifth of calls fail with a rate limit or a timeout (section 57.8) |

**Prompt versions are ours; model versions are the provider's.** This chapter names prompts `v1`, `v2`, `v3` and models `workhorse-001` and so on, so the two can never be confused.

One call, to see the shape:

```python
from provider import call, PINNED_MODEL

reply = call(WITH_EXAMPLE + "\nEMAIL:\n" + emails["email_012"], model=PINNED_MODEL)
print(PINNED_MODEL)
print(reply)
```

```
workhorse-001
{
  "customer": "Green Leaf Hotels",
  "po_number": "PO-92544",
  "delivery_date": "2026-03-07",
  "items": [
    {
      "product_code": "106",
      "quantity": 75
    },
    {
      "product_code": "108",
      "quantity": 10
    }
  ]
}
```

- `PINNED_MODEL` is the text `"workhorse-001"`, kept in one place so the whole chapter changes version by changing one line.
- The prompt is built exactly as in Chapter 54: the instructions, the marker line `EMAIL:`, then the email. `\n` is a line break inside a string.
- The reply is bare JSON, because `WITH_EXAMPLE` asks for JSON only. It is the same answer Chapter 54 marked as fully correct for `email_012`.

---

## 57.1 What changes, and what doesn't

| Chapter 56 said version… | In an LLM system that is… |
|---|---|
| Data | the corpus and the index (Chapter 55), plus the golden set |
| Features | the chunking and retrieval configuration |
| Code | the application, the parser, the validators |
| Model artifact | **a model name and version string you do not control** |
| Config | temperature, max tokens, thresholds, and **the prompt** |

Two additions, and both are the source of most LLMOps incidents:

- **The prompt is config that behaves like code.** It changes the system's behavior, it can regress, and it needs a version, a review, and a test.
- **The model is a dependency with its own release schedule.** Treat it exactly as you treat a library you pin: name the version, test before upgrading, and keep the old one available while you can.

---

## 57.2 Prompts as code

A **prompt registry** is the one place where every version of a prompt lives, with the facts that make it usable: what it says, what it was tested with, how it scored, and whether production uses it. Riverstone's first registry is a Python dictionary. Its three versions are Chapter 54's three prompts, the naive one, the one with instructions, and the one with an example:

```python
PROMPTS = {
    "v1": {"text": NAIVE, "model": PINNED_MODEL, "max_tokens": 500,
           "author": "Meera", "status": "retired", "score": None},
    "v2": {"text": INSTRUCTED, "model": PINNED_MODEL, "max_tokens": 500,
           "author": "Meera", "status": "retired", "score": None},
    "v3": {"text": WITH_EXAMPLE, "model": PINNED_MODEL, "max_tokens": 500,
           "author": "Meera", "status": "live", "score": None},
}

print("v1:", PROMPTS["v1"]["text"])
print("v2 adds:", PROMPTS["v2"]["text"][len(NAIVE):])
print("v3 adds:", PROMPTS["v3"]["text"][len(INSTRUCTED):])
```

```
v1: Extract the order from this email.
v2 adds:  Return JSON only, no prose, with keys customer, po_number, delivery_date (YYYY-MM-DD), items (product_code, quantity). Use null when a value is missing.
v3 adds: 

EXAMPLE
Email: PO-12345: 101 x 20, 107 x 5
Answer: {"customer": null, "po_number": "PO-12345", "delivery_date": null,
 "items": [{"product_code": "101", "quantity": 20}, {"product_code": "107", "quantity": 5}]}
```

**Line by line:**

- `PROMPTS` is a dictionary of dictionaries: the outer key is the version, and each inner dictionary is one row of the registry.
- `"text"` is the prompt itself. `"model"` and `"max_tokens"` are what it was tested with: a prompt is only good *with* a model. `max_tokens` caps the length of the reply on a real call (section 54.13); the stand-in ignores it.
- `"status"` says which version production uses, so nobody has to guess. `"score"` starts as `None` and is filled in by the golden set below.
- `PROMPTS["v2"]["text"][len(NAIVE):]` slices off the part `v2` shares with `v1`, so the print shows only what each version added: the output instructions, then the worked example.

Every call now builds its prompt the same way, so that job gets one small function:

```python
def build_prompt(version, email):
    """The instructions of one prompt version, then the marker line, then the email (Chapter 54)."""
    return PROMPTS[version]["text"] + "\nEMAIL:\n" + email

print(build_prompt("v1", emails["email_012"])[:100])
```

```
Extract the order from this email.
EMAIL:
From: accounts@green.example
To: orders@riverstone.example
```

`build_prompt("v1", ...)` looks up the version's text in the registry and joins the email on after the marker line. `[:100]` prints only the first 100 characters.

Next, the function that scores a version on the golden set. It is Chapter 54's `evaluate` (section 54.6) with three changes: it takes a prompt *version* rather than a text, it says which model to call, and it returns a dictionary so each number has a name:

```python
def evaluate(version, model=PINNED_MODEL, parser=parse, meter=None):
    """Run the golden set: every email, one call each, marked against the truth."""
    exact = unparseable = 0
    for name in truth:
        reply = call(build_prompt(version, emails[name]), model=model, meter=meter)
        order = parser(reply)
        if order is None:
            unparseable += 1
            continue
        exact += all(mark(order, truth[name]))
    return {"exact": exact, "of": len(truth), "accuracy": exact / len(truth),
            "unparseable": unparseable}
```

- `model=PINNED_MODEL` means "the pinned version unless you say otherwise". Section 57.4 says otherwise.
- `parser=parse` passes a *function* as a setting, the way `.apply(function)` took one in Chapter 18. The default is Chapter 54's `parse`; section 57.4 passes a better one.
- `meter=None` is handed straight to `call`. `None` means "don't count tokens"; section 57.5 builds the meter.
- As in Chapter 54, an unparseable reply is counted and skipped with `continue`, and `all(mark(...))` is 1 only when all four checks pass.
- The result has four keys: `exact` (fully correct emails), `of` (how many were scored), `accuracy` (the share), and `unparseable`.

Before you run the next cell, write down what you expect for each version. Then score all three and write each score back into the registry:

```python
for version in PROMPTS:
    result = evaluate(version)
    PROMPTS[version]["score"] = result["exact"]
    print(f"prompt {version}: {result['exact']:>2} of {result['of']} correct "
          f"({result['accuracy']:.0%}), {result['unparseable']} unparseable")
```

```
prompt v1: 13 of 60 correct (22%), 3 unparseable
prompt v2: 35 of 60 correct (58%), 0 unparseable
prompt v3: 47 of 60 correct (78%), 0 unparseable
```

These are Chapter 54's numbers exactly, as they should be: the same prompts, the same stand-in, the same parser. `:>2` right-aligns a number in two places (Chapter 17, section 17.8) and `:.0%` prints a share as a percentage with no decimals (Chapter 22 used `:.1%` for one decimal). The loop fills the registry's score column, so the registry now answers "was last month's version better?" with a number:

```python
print(f"{'version':<9}{'status':<9}{'model':<15}{'score':>9}")
for version, entry in PROMPTS.items():
    print(f"{version:<9}{entry['status']:<9}{entry['model']:<15}{entry['score']:>4} of 60")
```

```
version  status   model              score
v1       retired  workhorse-001    13 of 60
v2       retired  workhorse-001    35 of 60
v3       live     workhorse-001    47 of 60
```

**What a prompt registry needs**, whether it is a dictionary, a YAML file, or a product:

| Field | Why |
|---|---|
| Version | so a rollback names something |
| The text itself, in Git | so changes are reviewed and diffable, and Git records the date and author of every change |
| Model and settings it was tested with | a prompt is only good *with* a model and its settings |
| Golden-set score | the reason to prefer it |
| Author | the incident question is always "what changed, when, and who knows why?" |
| Status: draft, live, retired | so nobody guesses which one production uses |

A dictionary in a `.py` file is a fine first registry, because it lives in Git. When non-programmers start editing prompts, the same rows move to a YAML file, read with `yaml.safe_load` into exactly this dictionary.

> **Watch out: a prompt change is a release, not an edit.** The most common LLMOps incident is somebody improving a prompt in a dashboard on Friday afternoon. Same review, same test, same rollback plan as code, because it *is* code: it changes what the system does to customers.

---

## 57.3 The golden set as a build step

Chapter 54 built this evaluation set (60 emails with correct answers), and Chapter 55 built a second one for the assistant; here the first becomes a gate:

```python
FLOOR = 0.70

result = evaluate("v3")
passed = result["accuracy"] >= FLOOR and result["unparseable"] == 0
status = "PASS" if passed else "FAIL"
print(f"golden set: {result['exact']} of {result['of']} ({result['accuracy']:.0%}), "
      f"unparseable {result['unparseable']}, floor {FLOOR:.0%} -> {status}")
print(f"a build script would exit with code {0 if passed else 1} (Chapter 29's exit codes)")
```

```
golden set: 47 of 60 (78%), unparseable 0, floor 70% -> PASS
a build script would exit with code 0 (Chapter 29's exit codes)
```

**Line by line:**

- `passed` needs two conditions, not one. Accuracy above a floor is obvious; **`unparseable == 0` is the condition that actually saves you**, because a formatting change breaks every record at once, while accuracy computed on the replies that did parse can look fine.
- `"PASS" if passed else "FAIL"` is Python's one-line choice between two values: the first if the condition is true, the second if not. `0 if passed else 1` does the same for the exit code.

**Where the floor comes from.** Set it a little below the live version's score, so that noise doesn't fail the build but a real regression does. `v3` scores 47 of 60 (78%); a floor of 70% is 42 of 60, five emails of slack. That slack is also the weakness: a new prompt scoring 43 is a real step backwards and still passes. So raise the floor whenever the live score rises, or better, fail the build if the score falls more than a few emails below the last release's.

**What it costs to run.** One pass over the 60 emails costs under five rupees at Chapter 54's workhorse prices, as section 57.5 will measure, and a ten-email **smoke test** (a quick run on a few cases that only checks nothing is badly broken) under a rupee. Running it on every commit and nightly against the live provider is affordable at any volume a mid-sized company has, and the nightly run is the one that catches the next section's problem.

---

## 57.4 The day the provider changes the model

Providers ship improvements. Usually nothing happens. Occasionally your parser stops working, and the first you hear of it is from a customer.

The stand-in's `"workhorse-002"` is such an update: the same task, slightly different habits. Score the live prompt on it, with the parser Riverstone has today:

```python
from provider import NEW_MODEL

result = evaluate("v3", model=NEW_MODEL)
print(f"{NEW_MODEL} with Chapter 54's parse: {result['exact']} of {result['of']} correct, "
      f"{result['unparseable']} unparseable")
```

```
workhorse-002 with Chapter 54's parse: 0 of 60 correct, 60 unparseable
```

**Zero of sixty.** Not one reply could be read. Look at one to see why:

```python
print(call(build_prompt("v3", emails["email_012"]), model=NEW_MODEL))
```

```
{
  // fields extracted from the email body
  "customer": "Green Leaf Hotels",
  "po_number": "PO-92544",
  "delivery_date": "07-03-2026",
  "items": [
    {
      "product_code": "106",
      "quantity": 75
    },
    {
      "product_code": "108",
      "quantity": 10
    }
  ]
}
```

Two habits changed. The new version puts a **comment line** inside its JSON, starting with `//`; JSON has no comments, so `json.loads` rejects the whole reply. And on some emails it writes the delivery date **day first**, `07-03-2026`, which the marking compares with `2026-03-07` and calls wrong. The first habit alone is enough to make every reply unparseable.

**The fix is not a better prompt.** It is defensive parsing in *your* code, in two small functions. First, the date. The pattern language is Chapter 14's (section 14.2), and `re.fullmatch` with groups is how Chapter 28 read migration file names:

```python
import re

def normalize_date(value):
    """Turn a day-first DD-MM-YYYY date into YYYY-MM-DD; leave anything else as it was."""
    if not isinstance(value, str):
        return value
    match = re.fullmatch(r"(\d{2})-(\d{2})-(\d{4})", value)
    if match:
        return f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
    return value

for raw in ["2026-03-07", "07-03-2026", "7 March", None]:
    print(f"{raw!r:<14} -> {normalize_date(raw)!r}")
```

```
'2026-03-07'   -> '2026-03-07'
'07-03-2026'   -> '2026-03-07'
'7 March'      -> '7 March'
None           -> None
```

**Line by line:**

- `isinstance(value, str)` lets anything that isn't text (a missing date is `None`) pass through untouched.
- `r"(\d{2})-(\d{2})-(\d{4})"` means two digits, a dash, two digits, a dash, four digits. `\d{2}` is "exactly two digits". Each pair of brackets is a **group**: a part of the match you can take out afterwards.
- `re.fullmatch` succeeds only if the **whole** value fits the pattern, not just part of it (`re.search` would accept a match anywhere inside). It returns a match object, or `None`.
- `match.group(3)` is the text the third group matched (the year), `group(2)` the month, `group(1)` the day. The f-string puts them back together year first.
- Anything else, including a date that is already right and a date like `"7 March"`, comes back unchanged. Changing only what you understand is deliberate: Chapter 54's validator (section 54.7) then rejects `"7 March"` with a reason, rather than this function guessing.
- `!r` in the f-string prints each value with its quotes, so `None` and the text `'None'` would look different.

`07-03-2026` is read as 7 March because Riverstone's customers write the day first. A customer who writes month first would have `03-07-2026` read as 3 July, and nothing here would notice. That is why the validator's plausible-date window still matters.

Second, the parser. It is Chapter 54's `parse`, run after the comment lines are removed, with the date put right afterwards:

```python
def tolerant_parse(reply):
    """Chapter 54's parse, after removing comment lines, with the delivery date put right."""
    lines = [line for line in reply.splitlines() if not line.strip().startswith("//")]
    order = parse("\n".join(lines))
    if order is not None and "delivery_date" in order:
        order["delivery_date"] = normalize_date(order["delivery_date"])
    return order

replies = {
    "clean": '{"po_number": "PO-1", "delivery_date": "2026-03-07"}',
    "fence and comment": 'Here it is:\n```\n{\n  // from the email\n  "po_number": "PO-1"\n}\n```',
    "day-first date": '{"po_number": "PO-1", "delivery_date": "07-03-2026"}',
    "a list, not an order": '[{"po_number": "PO-1"}]',
    "no JSON at all": "Sorry, I could not find an order in this email.",
}
for label, reply in replies.items():
    print(f"{label:<21} -> {tolerant_parse(reply)}")
```

```
clean                 -> {'po_number': 'PO-1', 'delivery_date': '2026-03-07'}
fence and comment     -> {'po_number': 'PO-1'}
day-first date        -> {'po_number': 'PO-1', 'delivery_date': '2026-03-07'}
a list, not an order  -> {'po_number': 'PO-1'}
no JSON at all        -> None
```

**Line by line:**

- `reply.splitlines()` cuts the reply into lines. The list comprehension keeps every line except those whose first non-space characters are `//`: `line.strip()` removes the spaces around a line, and `.startswith("//")` tests how it begins.
- `"\n".join(lines)` glues the kept lines back into one string, and Chapter 54's `parse` does the rest. It already finds the JSON between the first `{` and the last `}`, so chat before and after, and markdown fences with or without the word `json`, never reach `json.loads`. It already returns `None` for invalid JSON and for anything that isn't an object, like the list in the fourth test, so a bad reply is a counted event, not a crash.
- `"delivery_date" in order` checks the key is there before touching it. Without that check, the function would add a `delivery_date` of `None` to an order that never had one.

This handles comments on **their own line**, which is the new version's habit. A comment at the end of a line, `"quantity": 20, // twenty cartons`, still breaks `json.loads`. The fix for that is not a longer parser but the provider's JSON or structured-output mode (Chapter 54, section 54.7), which stops the model writing comments at all.

Now the same golden set, three ways:

```python
runs = [(NEW_MODEL, parse, "new version, Chapter 54's parse"),
        (NEW_MODEL, tolerant_parse, "new version, tolerant_parse"),
        (PINNED_MODEL, tolerant_parse, "pinned version, tolerant_parse")]
for model, parser, label in runs:
    result = evaluate("v3", model=model, parser=parser)
    print(f"{label:<32} {result['exact']:>2} of {result['of']} correct, "
          f"{result['unparseable']:>2} unparseable")
```

```
new version, Chapter 54's parse   0 of 60 correct, 60 unparseable
new version, tolerant_parse      47 of 60 correct,  0 unparseable
pinned version, tolerant_parse   47 of 60 correct,  0 unparseable
```

![Three bars: the pinned model scores 47 of 60, the new model version with Chapter 54's parser gives 60 unparseable replies, and with a tolerant parser it is back to 47](figures/fig57-1-provider-upgrade.svg)

*Figure 57.1 — A provider update nobody at Riverstone triggered, and the twenty-minute fix that was always in their own code.*

**Read the first line again.** A version change nobody at Riverstone triggered takes the pipeline from 78% to nothing, because two habit changes made every reply unparseable. With the tolerant parser, the new version scores the same 47 of 60 as the pinned one, and the tolerant parser costs nothing on the pinned version either. The failure was never the model's understanding; it was a contract Riverstone assumed and never enforced. What happens if you change `tolerant_parse` to skip `normalize_date`? Try it: the replies parse again, but the emails with day-first dates are marked wrong, and the score drops to 27 of 60 without a single unparseable reply to warn you.

**The playbook for a model upgrade:**

1. **Pin the version** in config. Never use a **floating alias** in production: a model name like `workhorse-latest` that the provider re-points to each new version.
2. **Run the golden set against the new version** in a scheduled job, before you switch.
3. **Compare on the business metric**, not a vendor benchmark.
4. **Shadow it** (Chapter 56) if the volume justifies it.
5. **Switch with a rollback ready**, and keep the old version pinned until the new one has a week of clean numbers.
6. **Re-check the cost**: a newer model with a different tokenizer or a chattier style can change the bill without changing the price.

---

## 57.5 Tokens, cost, and the meter

Every call goes through one function, and that function counts. The counting lives in a small class (Chapter 29, section 29.5). First, the price table it will use:

```python
PRICES = {                      # US dollars per million tokens: (input, output)
    "workhorse-001": (2.00, 10.00),
    "workhorse-002": (2.00, 10.00),
    "volume-001": (0.75, 3.75),
}
USD_TO_INR = 88.0               # rupees per US dollar; check today's rate before you quote a bill

for model, (price_in, price_out) in PRICES.items():
    print(f"{model:<14} ${price_in:.2f} in, ${price_out:.2f} out per million tokens")
```

```
workhorse-001  $2.00 in, $10.00 out per million tokens
workhorse-002  $2.00 in, $10.00 out per million tokens
volume-001     $0.75 in, $3.75 out per million tokens
```

- `PRICES` holds each model's price per million tokens, input first. The workhorse prices are Chapter 54's workhorse tier and the volume model's are its volume tier (section 54.12, checked 29 September 2026). The new version costs the same per token as the old one.
- `USD_TO_INR = 88.0` converts dollars to rupees. Exchange rates move, so it is a named setting in one place, not a number buried in a formula.

Now the meter itself:

```python
class Meter:
    """Every call, counted: tokens in and out per model, and every provider error by kind."""

    def __init__(self):
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.by_model = {}          # model -> [tokens in, tokens out]
        self.errors = {}            # kind of error -> how many

    def record(self, model, prompt, reply):
        tokens_in, tokens_out = len(prompt) // 4, len(reply) // 4
        self.calls += 1
        self.input_tokens += tokens_in
        self.output_tokens += tokens_out
        if model not in self.by_model:
            self.by_model[model] = [0, 0]
        self.by_model[model][0] += tokens_in
        self.by_model[model][1] += tokens_out

    def record_error(self, kind):
        self.errors[kind] = self.errors.get(kind, 0) + 1

    def cost_rupees(self):
        dollars = 0.0
        for model, (tokens_in, tokens_out) in self.by_model.items():
            price_in, price_out = PRICES[model]
            dollars += tokens_in / 1_000_000 * price_in + tokens_out / 1_000_000 * price_out
        return dollars * USD_TO_INR
```

**Line by line:**

- `__init__` starts every count at zero. `by_model` keeps tokens per model, because two models on one bill have two prices; `errors` counts failures by kind for section 57.8.
- `record` is what `call` runs after every successful reply. `len(prompt) // 4` is Chapter 54's rule of about four characters a token (`//` divides and drops the remainder). The stand-in has no tokenizer, so this estimate *is* its token count; with a real provider you record the counts the reply reports (section 54.13).
- `record_error` adds one to a kind of error. `self.errors.get(kind, 0)` gives the count so far, or 0 the first time.
- `cost_rupees` walks through the models: `for model, (tokens_in, tokens_out) in ...items()` unpacks each model's pair of counts. `1_000_000` is one million; the underscores are only there to make it readable. Tokens divided by a million, times the price per million, is dollars; the total times `USD_TO_INR` is rupees.

`call` accepts any object with `record` and `record_error` methods as its `meter`, so this class plugs straight in. Meter one golden-set run:

```python
meter = Meter()
result = evaluate("v3", meter=meter)
print(f"{meter.calls} calls, {meter.input_tokens:,} tokens in, {meter.output_tokens:,} tokens out")
print(f"per call: about {meter.input_tokens // meter.calls} in and {meter.output_tokens // meter.calls} out")
print(f"cost of one golden-set run: ₹{meter.cost_rupees():.2f}")
```

```
60 calls, 10,844 tokens in, 3,184 tokens out
per call: about 180 in and 53 out
cost of one golden-set run: ₹4.71
```

`:,` prints a number with thousands separators. About 180 tokens in and 53 out per call is what Chapter 54 estimated for the same prompt in its answer 13 (about 179 and 53), because it is the same rule of four characters a token applied to the same text.

Check the cost by hand, once, so you trust the meter afterwards:

- input: 10,844 tokens × $2 ÷ 1,000,000 = $0.0217
- output: 3,184 tokens × $10 ÷ 1,000,000 = $0.0318
- total: $0.0535 × ₹88 = **₹4.71**

The output is less than a third of the tokens and well over half the cost, because output tokens cost five times as much here.

Now the number worth quoting to a manager, the cost per email, and a month. Riverstone works 22 days a month; on most of them about 40 order emails arrive, and on the three days of month-end about 120:

```python
per_email = meter.cost_rupees() / meter.calls
normal_days, month_end_days = 19, 3
emails_a_month = 40 * normal_days + 120 * month_end_days

print(f"cost per email: ₹{per_email:.3f}")
rows = [("a normal day, 40 emails", per_email * 40),
        ("a month-end day, 120 emails", per_email * 120),
        (f"a month, {emails_a_month:,} emails", per_email * emails_a_month),
        ("ceiling, 120 emails × 30 days", per_email * 120 * 30)]
for label, rupees in rows:
    print(f"{label:<31} ₹{rupees:6.2f}")
```

```
cost per email: ₹0.079
a normal day, 40 emails         ₹  3.14
a month-end day, 120 emails     ₹  9.42
a month, 1,120 emails           ₹ 87.93
ceiling, 120 emails × 30 days   ₹282.63
```

- `per_email` divides the run's cost by its 60 calls. `rows` is a list of (label, rupees) pairs, and the loop prints each label padded to 31 characters so the amounts line up.
- The month is 19 ordinary days plus 3 month-end days, 1,120 emails in all. That is the forecast.
- The last line multiplies a month-end day by 30, as if every day of the month were month-end and weekends too. It is a **ceiling**, useful for "what is the most this could cost?", and three times the forecast. Label each number for what it is: a ceiling quoted as a forecast is how budgets get cut for the wrong reason.

**Where the money actually goes**, in order of how often it surprises people:

| Cause | Typical size | Fix |
|---|---|---|
| A long system prompt re-sent on every call | the largest line on most bills | prompt caching (section 54.12: only for prompt starts above the provider's minimum length), or shorten it |
| Retrieval pasting too many chunks | grows silently as the corpus grows | retrieve fewer, rerank better (Chapter 55) |
| Retries | multiplies the failure rate by the cost | cap attempts; fall back to a cheaper model |
| Verbose answers | output costs five to six times input (section 54.12) | ask for a length limit and enforce it |
| Development and evaluation runs | small per run, large per month | cache, and run the full set nightly rather than per keystroke |

---

## 57.6 Caching

Some traffic repeats. Customers resend an order when they haven't had a reply, an operator retries a batch, and support customers ask the same questions. An **exact-match cache** keeps each reply against the prompt that produced it, and answers a repeated prompt from the store with no call and no cost. The key is a **hash** of the prompt: a fixed-length fingerprint of the text (Chapter 45, section 45.5), so the same text always gives the same key:

```python
import hashlib

class Cache:
    """The same prompt to the same model returns the stored reply, with no call and no cost."""

    def __init__(self):
        self.store = {}
        self.hits = 0
        self.misses = 0

    def get_or_call(self, prompt, model, meter):
        key = hashlib.sha256((model + "\n" + prompt).encode("utf-8")).hexdigest()
        if key in self.store:
            self.hits += 1
            return self.store[key]
        self.misses += 1
        reply = call(prompt, model=model, meter=meter)
        self.store[key] = reply
        return reply

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0
```

- `store` is a dictionary from key to reply. `hits` counts answers served from it; `misses` counts real calls.
- The key is the SHA-256 hash of the model name and the prompt together. The model is part of the key because a different model can give a different answer to the same prompt. `.encode("utf-8")` turns the text into bytes, which is what `hashlib` reads, and `.hexdigest()` gives the fingerprint as 64 hexadecimal characters.
- On a hit, the stored reply comes back and nothing is called. On a miss, it calls the provider, stores the reply, and returns it.
- `hit_rate` is hits over all requests. `if total else 0.0` avoids dividing by zero before the first request.

Three requests show the rule. Predict the counts after each before you run it:

```python
cache, demo_meter = Cache(), Meter()
prompt = build_prompt("v3", emails["email_012"])
for label, text in [("first time", prompt), ("same prompt again", prompt), ("one extra space", prompt + " ")]:
    cache.get_or_call(text, PINNED_MODEL, demo_meter)
    print(f"{label:<18} hits {cache.hits}, misses {cache.misses}, calls paid for {demo_meter.calls}")
```

```
first time         hits 0, misses 1, calls paid for 1
same prompt again  hits 1, misses 1, calls paid for 1
one extra space    hits 1, misses 2, calls paid for 2
```

The repeat is free. The same prompt with one extra space is a different text, so it has a different hash, and it is a miss. That is the whole strength and the whole weakness of exact matching.

**How much does it save on a real day?** A normal day at Riverstone is about 40 new order emails. Suppose one request in six is a resend or a retry of an email already seen that day, 8 on top of the 40:

```python
import random

rng = random.Random(57)
day = rng.sample(list(truth), 40)
resends = [rng.choice(day) for _ in range(8)]
traffic = day + resends
rng.shuffle(traffic)

cache, cached_meter, plain_meter = Cache(), Meter(), Meter()
for name in traffic:
    prompt = build_prompt("v3", emails[name])
    cache.get_or_call(prompt, PINNED_MODEL, cached_meter)
    call(prompt, model=PINNED_MODEL, meter=plain_meter)

print(f"{len(traffic)} requests: {cache.hits} hits, {cache.misses} misses, "
      f"hit rate {cache.hit_rate():.0%}")
print(f"cost without cache: ₹{plain_meter.cost_rupees():.2f}")
print(f"cost with cache:    ₹{cached_meter.cost_rupees():.2f} "
      f"({1 - cached_meter.cost_rupees() / plain_meter.cost_rupees():.0%} saved)")
```

```
48 requests: 8 hits, 40 misses, hit rate 17%
cost without cache: ₹3.82
cost with cache:    ₹3.19 (17% saved)
```

**Line by line:**

- `random.Random(57)` is a random generator with a fixed **seed**, as in Chapter 29, so every run picks the same emails. `rng.sample(list(truth), 40)` picks 40 *different* emails: the day's new orders. `rng.choice(day)` picks one of them, so the 8 `resends` repeat emails already in the day. `rng.shuffle(traffic)` mixes them into a random order.
- Each request goes twice: once through the cache (metered by `cached_meter`) and once straight to the provider (metered by `plain_meter`), so the two costs compare the same traffic.

A 17% hit rate, and 17% of the cost saved: exactly the share of requests that repeat. **An exact-match cache can never save more than the share of your traffic that repeats**, and for order emails, where almost every email is new, that share is small. The hit rate depends on your traffic, not on the cache, so measure it on your own logs rather than borrowing anyone's number.

Support questions are where repetition is real. `questions_stream.py` builds eight weeks of 40 questions a week to Chapter 55's assistant, drawn from Chapter 55's 65 test questions (plus some new ones from week 5, which section 57.9 is about), with a fixed seed, 57:

```python
from questions_stream import build

stream = build()
week_one = [q["question"] for q in stream if q["week"] == 1]
all_weeks = [q["question"] for q in stream]
for label, questions in [("one week", week_one), ("eight weeks", all_weeks)]:
    distinct = len(set(questions))
    print(f"{label:<12}{len(questions):>4} questions, {distinct:>2} different: "
          f"an exact cache would hit {1 - distinct / len(questions):.0%}")
```

```
one week      40 questions, 29 different: an exact cache would hit 28%
eight weeks  320 questions, 71 different: an exact cache would hit 78%
```

- `stream` is a list of dictionaries, one per question, each with its `week`, its `question` text, and a `topic`.
- `set(questions)` keeps one copy of each different question. An exact cache misses once per different question and hits on every repeat, so its hit rate is one minus different over total.

A cache kept for eight weeks would answer most questions from the store, but only because this stream draws from a fixed list of 65 questions. A real support inbox, with thousands of ways to ask, repeats far less exactly. That is where **semantic** caching comes in, and it has its own risk:

| Kind | Matches on | Good for | Watch out |
|---|---|---|---|
| **Exact** | the whole prompt | resent emails, repeated questions, retries | one extra space is a miss |
| **Semantic** | an embedding within a distance (Chapter 55) | support questions phrased differently | a near-match is not the same question; test the distance threshold |
| **Provider prompt caching** | a shared prefix | long system prompts and few-shot blocks | only helps the input side; needs the stable part first |

> **Watch out: cache invalidation is a business rule.** A cached answer about the delivery policy is wrong the day the policy changes. Key the cache on the prompt *and* the corpus version, expire it on a schedule you choose deliberately, and never cache anything that includes live data (an order status) at all.

---

## 57.7 Latency

A support answer should arrive in about two seconds; an extraction job that runs overnight can take minutes. The budget is made of parts you can measure and parts you can only manage.

| Part | Typical | What to do about it |
|---|---|---|
| Your code (retrieval, validation, parsing) | 1–50 ms | measure it; it is rarely the problem |
| Network to the provider | 20–200 ms | use a **regional endpoint** (the provider's servers nearest you, Mumbai rather than Virginia), and **keep connections alive** (reuse one network connection for many calls, as Chapter 29's session did) |
| **Time to first token** (how long until the first word of the answer arrives) | 200 ms – 2 s | stream, so the user sees words immediately |
| Generation | 10–100 tokens per second | ask for shorter answers; use a smaller model |
| Retries | doubles or triples the whole thing | cap attempts, and time out before the user does |

Two rules that matter more than tuning. **Stream anything a human waits for**: with **streaming**, the provider sends the answer word by word as it is generated, so the user starts reading at once, and perceived latency is the time to the first word, not the last. And **do not put a model call in a path that must be fast**: Riverstone's order extraction runs as a batch every morning, so a four-second call is irrelevant, and that architectural choice is worth more than any optimization.

---

## 57.8 Failure and fallback

Providers fail. Rate limits, timeouts, 500s, and occasional regional outages are normal operating conditions, not emergencies, and the difference between a system that survives them and one that doesn't is about thirty lines.

The stand-in fails on purpose when you pass it a `failure_rate`. These are the lines of `provider.py` that decide it:

<!-- run: none -->
```python
class RateLimitError(Exception):
    """429: the provider is throttling us. Wait, then try again."""

class ProviderTimeout(Exception):
    """The call took longer than the time we allow. Retrying at once rarely helps."""

# inside call(): a number between 0 and 1 fixed by the model and the prompt
share = _share(model, prompt, "failure")
if share < failure_rate * 0.6:                    # three failures in five are rate limits
    if meter is not None:
        meter.record_error("rate limit")
    raise RateLimitError("429 too many requests")
if share < failure_rate:                          # the other two are timeouts
    if meter is not None:
        meter.record_error("timeout")
    raise ProviderTimeout("no reply within 10 seconds")
```

- `class RateLimitError(Exception)` makes a new kind of error (Chapter 29): nothing inside but its docstring, and a name your code can catch on its own.
- `_share` hashes the model name and the prompt into a number between 0 and 1. With `failure_rate=0.2`, numbers below 0.12 are rate limits and numbers from 0.12 to 0.2 are timeouts; everything else succeeds.
- **The failures are deterministic.** The same prompt to the same model always fails, or succeeds, the same way, so every run of this chapter prints the same numbers. A real rate limit is usually gone a second later; this one never is, which matters for exercise 8.

Now the function that absorbs them:

```python
import time
from provider import RateLimitError, ProviderTimeout, FALLBACK_MODEL

BACKOFF_SECONDS = 0.5

def call_with_fallback(prompt, meter, failure_rate=0.0, attempts=3, backoff=BACKOFF_SECONDS):
    """Retry the pinned model, then try the cheaper one, then give up honestly."""
    for attempt in range(attempts):
        try:
            return call(prompt, model=PINNED_MODEL, meter=meter, failure_rate=failure_rate), "primary"
        except RateLimitError:
            if attempt < attempts - 1:
                time.sleep(backoff * 2 ** attempt)      # 0.5 s, then 1 s (Chapter 29)
        except ProviderTimeout:
            break                                       # one timeout: the prompt is slow; stop waiting
    try:
        return call(prompt, model=FALLBACK_MODEL, meter=meter, failure_rate=failure_rate), "fallback"
    except (RateLimitError, ProviderTimeout):
        return None, "failed"

print(f"primary {PINNED_MODEL}, fallback {FALLBACK_MODEL} at ${PRICES[FALLBACK_MODEL][0]} / "
      f"${PRICES[FALLBACK_MODEL][1]} per million tokens")
```

```
primary workhorse-001, fallback volume-001 at $0.75 / $3.75 per million tokens
```

**Line by line:**

- `import time` gives `time.sleep(seconds)`, which pauses. `FALLBACK_MODEL` is `"volume-001"`, the cheaper model.
- **Different errors deserve different responses.** A rate limit means "wait and try again", so it retries with **exponential backoff**, each wait twice the last: `2 ** attempt` is 1, 2, 4 for attempts 0, 1, 2, so the waits are 0.5 s, then 1 s, as in Chapter 29. `if attempt < attempts - 1` skips the pointless wait after the last try.
- A timeout usually means the request itself is slow, so retrying it at once just burns another ten seconds; `break` leaves the loop after one timeout and moves to the fallback.
- **The fallback is a cheaper, smaller model.** A degraded answer now beats a perfect answer after the shift ends. `except (RateLimitError, ProviderTimeout):` catches either kind, written as a tuple.
- The function returns a pair: the reply and the **route** that produced it, so the caller, and the monitoring, know which model answered. **`None, "failed"`** is a real outcome, not an exception to swallow: the item goes to the human queue (Chapter 54's escalation path) with a reason.

Run the golden set's 60 emails through it with the provider failing a fifth of calls. `backoff=0.001` shortens the waits to milliseconds so the cell finishes at once; the logic is the same:

```python
fallback_meter = Meter()
routes = {"primary": 0, "fallback": 0, "failed": 0}
for name in truth:
    _, route = call_with_fallback(build_prompt("v3", emails[name]), fallback_meter,
                                  failure_rate=0.2, backoff=0.001)
    routes[route] += 1

print(f"with the provider failing 20% of calls, over {len(truth)} emails:")
for route, count in routes.items():
    print(f"  {route:<9} {count:>3} ({count / len(truth):.0%})")
print(f"provider errors absorbed: {fallback_meter.errors}")
print(f"served one way or another: {(routes['primary'] + routes['fallback']) / len(truth):.0%}")
```

```
with the provider failing 20% of calls, over 60 emails:
  primary    44 (73%)
  fallback   13 (22%)
  failed      3 (5%)
provider errors absorbed: {'rate limit': 35, 'timeout': 6}
served one way or another: 95%
```

- `_, route = ...` unpacks the pair and throws the reply away: `_` is the usual name for a value you don't need.
- `routes[route] += 1` counts each route in a dictionary, as Chapter 17 (section 17.7) counted order statuses.

The 41 errors add up. Sixteen emails failed on the pinned model: eleven were rate-limited on all three attempts (33 errors) and five timed out once (5 errors). All sixteen went to the fallback, which failed on three of them, twice with a rate limit and once with a timeout (3 errors). That makes 33 + 2 = 35 rate limits and 5 + 1 = 6 timeouts, 41 in all, and 44 + 13 + 3 = 60 emails.

![Two panels: an exact-match cache on a normal day of 48 requests saves 17% of the cost, and with a 20% provider failure rate 44 emails go to the primary model, 13 to the fallback and 3 to a human](figures/fig57-2-cost-and-failure.svg)

*Figure 57.2 — The two pieces of operational work that decide the bill and the uptime.*

**95% served, 5% escalated honestly, through 41 provider errors.** That is what "resilient" means in practice: not that nothing failed, but that the failures were absorbed, counted, and the remainder handed to a person with a reason.

**The rest of the resilience checklist:**

- **Timeouts on every call.** A hung request holds a worker until something kills it.
- **A circuit breaker.** After *n* consecutive failures, stop calling for a minute. Hammering a struggling provider makes it worse and burns your rate limit.
- **Idempotency.** Chapter 29's rule: a retried extraction must not create two orders. Key the write on the email id.
- **A queue in front of anything batch.** If the provider is down at 6 a.m., the work waits and runs at 7.
- **A degraded mode you have designed.** For the assistant: retrieval still works, so show the top three documents with "I can't summarize these right now". That is far better than an error page, and it needs no model at all.

---

## 57.9 Monitoring without ground truth

Chapter 56's monitoring layers still apply (service, input, and output and outcome, section 56.7), and the last one, outcome, is the problem: for an assistant there is no label. What you have instead is a set of **proxies**, each blind in its own way.

| Signal | What it catches | Blind to |
|---|---|---|
| **Refusal rate** | questions the corpus can't answer; a threshold set wrong | wrong answers given confidently |
| **Citation rate** | answers that escaped grounding | a citation to the wrong document |
| **Answer length distribution** | a model that has started rambling, or truncating | subtle quality changes |
| **Thumbs-down rate** | user-visible failures | everything users don't bother reporting |
| **Escalation rate** | the pipeline's own honesty: every failure it noticed | wrong answers that pass validation (Chapter 54's dozen well-formed, wrong orders); still the best single number you have for the failures the system can see |
| **Topic drift** | questions arriving about things you have no documents for | quality on the questions you do cover |
| **Cost and latency per request** | a prompt or retrieval change that quietly grew | quality entirely |

The one worth building first is **topic drift**, because it is the LLM equivalent of Chapter 56's new mould: nothing looks broken, and the system slowly stops being useful. Section 57.6's `stream` has eight weeks of questions; Chapter 55's assistant answers them. The first three questions of week 1:

```python
from assistant import SupportAssistant

assistant = SupportAssistant()
for q in stream[:3]:
    print(q)
```

```
{'week': 1, 'question': 'How long is the lead time for the Storage Box 10L?', 'topic': 'known'}
{'week': 1, 'question': 'What is the list price of the Industrial Crate?', 'topic': 'known'}
{'week': 1, 'question': 'How many garden chairs are in a standard carton?', 'topic': 'known'}
```

- `SupportAssistant` is Chapter 55's class (section 55.6), imported from `assistant.py` in the Chapter 55 folder that the setup cell put on `sys.path`. It finds its own documents, so the notebook doesn't have to change folder.
- Each question carries a `topic`: `"known"` for questions the corpus was built for, `"new"` for the ones that start arriving in week 5. The assistant never sees the topic; the stream keeps it so you can check the monitor afterwards.

Now each week's questions through the assistant, with the two numbers a monitor would plot:

```python
print(f"{'week':>5}{'questions':>11}{'refusal rate':>14}{'mean confidence':>17}")
for week in range(1, 9):
    rows = [q for q in stream if q["week"] == week]
    results = [assistant.answer(q["question"]) for q in rows]
    refusals = sum(1 for r in results if not r["grounded"])
    confidence = sum(r["score"] for r in results) / len(results)
    print(f"{week:>5}{len(rows):>11}{refusals / len(rows):>13.0%}{confidence:>17.3f}")
```

```
 week  questions  refusal rate  mean confidence
    1         40          15%            0.587
    2         40          18%            0.577
    3         40          20%            0.577
    4         40          15%            0.584
    5         40          32%            0.573
    6         40          25%            0.545
    7         40          42%            0.450
    8         40          38%            0.481
```

**Line by line:**

- `[q for q in stream if q["week"] == week]` keeps the week's 40 questions, and the second list comprehension answers each one.
- `assistant.answer` returns a dictionary (Chapter 55, section 55.6): `grounded` is `False` when it refused, and `score` is its retrieval confidence, the smaller of its two confidence signals. `sum(1 for r in results if not r["grounded"])` adds 1 for every refusal.
- The last column is the week's average `score`. From week 5 a growing share of questions ask about a new pallet range that has no documentation; the assistant is unchanged throughout.

![A chart of refusal rate rising from 15% to 42% over eight weeks, with mean retrieval confidence on its own scale falling from 0.59 to 0.45, marked at week 5 where customers start asking about a new product line](figures/fig57-3-topic-drift.svg)

*Figure 57.3 — Nothing broke. The corpus stopped covering what people ask.*

**Read the two columns.** Refusals sit around 15–20% for four weeks, then climb to 42% in week 7. Mean confidence drifts down from about 0.59 to 0.45. **Nothing is broken**: the prompt is the same, the model is the same, the code is the same. Customers have started asking about something Riverstone never wrote down, and the monitor that sees it is the assistant's own honesty.

The action is not a model change. It is **three new documents**, which is Chapter 55's content backlog arriving through a metric instead of a complaint.

> **Watch out: refusal rate is two signals wearing one coat.** It rises when the corpus is missing content (fix the corpus) and when the threshold is too strict (fix the threshold). Split it: refusals where retrieval found *nothing* close are content gaps; refusals where it found something just below the floor are threshold problems. Riverstone's week-7 spike is overwhelmingly the first kind, and looking at ten refused questions by hand tells you which you have in about five minutes.

---

## 57.10 Safety and logs in production

Chapters 54 and 55 covered the risks; this is what they look like as operations.

**What to log for every request:**

| Field | Why |
|---|---|
| Request id, timestamp | to join everything else together |
| Prompt version, model name and version | the first question in every incident |
| Retrieved chunk ids (Chapter 55) | traces a bad answer to its document in a minute |
| Tokens in and out, latency, route (primary or fallback) | cost and performance monitoring |
| Validation result and escalation reason | the quality signal you actually have |
| A hash of the user's text (and the text itself only under a stated retention rule, below) | enough to spot repeats without storing the words |

A hash works here for the same reason it keys the cache: the same text always gives the same fingerprint, so repeats can be counted without keeping the words. It is not a hiding place for everything, though. A short, guessable value, like a phone number or an order id, can be recovered by hashing every possible candidate until one matches, so strip such values out before you hash.

**Storing the user's words is a decision, not a default.** Support questions contain names, phone numbers, and order details. Store them only if you need them, say so, set a retention period, and keep them out of anything sent to a provider you have not checked the terms of (Chapter 54's section 54.11). Riverstone's rule: full text kept for 30 days for debugging, hashes kept for a year for deduplication and trend analysis.

**Injection attempts belong in monitoring**, not just in the guardrail. Count them, log the source document or email, and alert if the rate jumps: a rise usually means either a new attacker or a new integration that is passing untrusted content into a prompt without anyone realizing.

**The audit trail that matters.** If an automated answer ever costs a customer money, you will be asked: what did the system say, on what basis, under which version, and who could have caught it? A log line with the prompt version, the model version, the retrieved chunks, and the validation result answers all four. Chapter 64 covers the governance around it.

A **trace** is the same idea across steps: one record that follows a single request through retrieval, the model call, validation and escalation, with the time each step took, all tied together by the request id.

---

## 57.11 The human loop

With no accuracy metric, **the humans are the metric**, and the job is to make their signal cheap to give and impossible to lose.

1. **A thumbs-down on every answer**, with an optional one-line reason. No form, no login.
2. **An escalation queue** with the reason attached, from the pipeline's own validation (Chapter 54's section 54.7).
3. **A weekly review of a sample**, including successes. Reviewing only failures gives a distorted picture of the system and of your own progress.
4. **Every complaint becomes a golden-set case**, with the correct answer written by whoever resolved it. This is the single highest-value habit in the chapter: the test suite grows out of real failures, so the same failure cannot recur quietly.
5. **A content backlog** from refusals and unanswerable questions, sent to document owners by name.
6. **A monthly report** with the numbers from this chapter: golden-set score by prompt version, cost per request, refusal and escalation rates, and what changed.

**What this looks like after six months:** an extraction golden set that started at Chapter 54's 60 emails and holds 150, a prompt at version 9 with a score attached to each version, a cost per email that has fallen as caching improved, and a support lead who trusts the system because they have seen it refuse rather than guess. None of that is model work.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A floating model alias in production | Behavior changes on a day you shipped nothing | Pin the version; upgrade deliberately |
| No golden set | A provider change is discovered by a customer | A few dozen cases with known answers (Chapter 54's 60 emails), run nightly and in CI |
| Measuring accuracy only on parseable replies | 100% "accuracy" on the four replies that parsed | Count unparseable separately, and fail the build on any |
| Trusting the model's formatting | Every record breaks when a habit changes | Normalize dates, numbers, and IDs in your own code |
| Editing prompts in a dashboard | Nobody knows what changed or when | Prompts in Git, versioned, reviewed, scored |
| No token meter | The bill is a surprise | Count per call; project monthly; review at each release |
| Quoting a ceiling as a forecast | A budget built on every day being month-end | Project from a realistic month; label the ceiling as one |
| No cache | Paying five times for the same question | Exact-match first; it is an afternoon's work |
| Expecting a cache to fix everything | A hit rate borrowed from someone else's traffic | Measure the repeat share on your own logs first |
| Caching live data | Confidently stale order statuses | Never cache tool results; key document answers on corpus version |
| Retrying everything the same way | Timeouts retried instantly, rate limits hammered | Backoff for rate limits, fallback for timeouts, caps on both |
| No fallback | The provider's outage is your outage | A cheaper model, then a degraded mode that still serves |
| Swallowing failures | Silent gaps in the data nobody notices | `failed` is an outcome: count it, escalate it |
| Monitoring only uptime | A system that is up and useless | Refusal, escalation, citation, length, cost, topic drift |
| Ignoring refusal rate | The corpus goes stale while the code looks healthy | Split content gaps from threshold problems; feed the backlog |
| Logging full user text by default | A privacy problem in a log file | Log ids, hashes, versions, and decisions; set retention |
| Complaints that go nowhere | The same failure recurs monthly | Every complaint becomes a golden-set case |

---

## In the real world: the Monday the drafts were empty

Riverstone's order intake runs at 06:00 every weekday in assisted mode: the pipeline drafts an order from each email, and a coordinator confirms every draft before anything reaches the ERP (Chapter 58 tells how that pilot was set up). One Monday the run finishes, exits with status 0, and drafts nothing. All 52 emails, the weekend's orders included, went to the exception queue with the reason "unparseable reply". An empty review screen on a Monday morning looks like a slow start, and the exception queue is normally worked after lunch. Nobody notices until 11:00, when the dispatch team asks why the morning's orders are missing.

The cause takes four minutes to find, because every run logs its model version and its validation counts: 52 emails read, **52 unparseable**, 0 drafted. The version Meera had pinned in Chapter 54 had reached its retirement date on the Saturday. The configuration named the provider's floating alias as a fallback for exactly that day, and the alias now pointed at a new version nobody at Riverstone had tested. The new version puts comments inside its answers and prefers a different date format, and Riverstone's parser expected neither.

Two things went right, and both were built in this chapter and in Chapter 54:

- **Nothing wrong was drafted.** Every email went to the exception queue with a reason, and no order was built from a misread reply.
- **The fix was twenty minutes.** Strip comment lines, normalize the date, rerun the golden set: 47 of 60, exactly as before. The morning's emails were reprocessed by lunchtime.

Four things went wrong, and all four were process:

- **The run should have failed.** A run in which more than one reply in five is unparseable must exit non-zero and alert, rather than report success with nothing done: the batch circuit breaker Chapter 58 adds.
- **The nightly golden-set run had been switched off a month earlier** because it "kept failing" during a prompt experiment. It would have caught this on Saturday night, with nobody waiting.
- **Nobody had put the retirement date in a calendar.** The provider had announced it, and the new version, weeks before.
- **The alert on "unparseable rate above 5%" existed and went to an unmonitored mailbox.**

**What Meera writes in the post-mortem:** *"The model changed under us, which will happen again. What failed was that our run reported success, our test wasn't running, and our alert wasn't reaching a person. The parser fix took twenty minutes; the four process fixes (fail the run above 20% unparseable, re-enable the nightly run, put retirement dates in the calendar, route the alert to a phone) took ten minutes each. We now pin a version and never fall back to an alias: when a pinned version is retired, the run stops and says so. The golden set runs nightly against both the pinned and the latest version, and the alert goes to my phone."*

The habit worth taking from this: **assume the model will change without telling you, and make that a Tuesday-morning inconvenience rather than a Monday-morning incident.**

---

## Project: instrument an LLM feature

**Goal:** take an LLM feature (yours or Chapter 54's) and give it the operational apparatus to survive a year.

### Tools you'll need

Checked in September 2026; this area changes faster than any other in the book.

- **Python** (the book's outputs come from Python 3.11), standard library only for this chapter's code; **Chapter 55's assistant**, which uses NumPy and scikit-learn, for section 57.9.
- **Prompt and evaluation management**: LangSmith, Langfuse, Braintrust, Weights & Biases Weave, plus MLflow's LLM tracking (Chapter 56's tool, extended for prompts and traces). A YAML file in Git and a golden set in a script beat all of them for a first system.
- **Gateways and routing**: LiteLLM, OpenRouter, or a provider's own gateway, which give one interface, retries, fallbacks, key management, and a per-team spend limit in one place.
- **Caching**: Redis for exact matches, a vector store for semantic caching (Chapter 55), and the providers' own prompt caching for long stable prefixes.
- **Observability**: OpenTelemetry for traces (a request that fans out to retrieval, model, and tools is a **distributed trace**: one trace whose steps run in different services), plus whatever your team already uses for metrics and alerts.
- **Guardrails and safety**: NeMo Guardrails, Guardrails AI, and the providers' moderation endpoints. Validate outputs against business rules regardless (Chapter 55).
- **Companion files** in `companion/ch57/`: `provider.py` (the metered, failure-simulating wrapper around Chapter 54's stand-in), `pipeline.py` (the registry, `evaluate`, the tolerant parser, the cache and the fallback, exactly as built in this chapter), `questions_stream.py` (eight weeks of questions with topic drift), and `ci_eval.py` (exercise 5).

> **Simplification note.** The provider here is a local stand-in with a simulated version change and a simulated failure rate, because no reader should need a paid key. What that changes: real providers fail in more varied ways, their rate limits clear after a wait, and a real model upgrade can shift meaning as well as format. What it doesn't change: pinning versions, golden sets in CI, tolerant parsing, metering, caching, backoff and fallback, and every monitoring signal in section 57.9.

**Steps:**

1. **Move the prompt into a registry** with versions, and score each version on your golden set.
2. **Put the golden set in CI** with a floor and a zero-unparseable condition, and make it fail the build.
3. **Pin the model version** in config, and add a scheduled job that runs the golden set against the latest version too.
4. **Make the parser tolerant**: fences, comment lines, and normalized dates, numbers, and identifiers.
5. **Add a meter**: tokens in and out per call, cost per request, and a monthly projection at two price points.
6. **Add an exact-match cache** and measure the hit rate on a realistic day of traffic.
7. **Add retries with backoff, a cheaper fallback, and a degraded mode.** Test them by making the provider fail.
8. **Build the monitoring digest**: refusal rate, escalation rate, unparseable rate, cost, latency, and topic drift.
9. **Add the human loop**: thumbs-down, an escalation queue with reasons, and a rule that every complaint becomes a golden-set case.
10. **Write the runbook**: what to check when the numbers move, how to roll back a prompt, and how to pin an older model.

**Deliverables:** the versioned prompts with scores, the CI job, the cost projection, the cache measurement, the failure test, the digest, and the runbook.

**Stretch goals:**

- Add semantic caching and measure the extra hit rate, then find a case where it returns a wrong answer.
- Implement a circuit breaker and demonstrate it opening and closing under a simulated outage.
- Split refusals into content gaps and threshold problems automatically.
- Route easy requests to a cheap model and hard ones to an expensive one, and measure accuracy per rupee.
- Add a trace id that follows a request through retrieval, model call, validation, and escalation.

---

## Recap

- LLMOps is Chapter 56's discipline plus two things to version: **the prompt**, and **a model you don't control**.
- **Prompts are code**: kept in a registry, versioned, reviewed, scored. Riverstone's went 13 → 35 → 47 of 60 across three versions, Chapter 54's numbers.
- **The golden set belongs in CI**, with an accuracy floor set just below the live score *and* a zero-unparseable condition. One run costs about ₹4.71.
- **A provider can change the model.** In this chapter's simulation a new version took the pipeline from 47 of 60 to **0 of 60**, and a tolerant parser restored it to 47. Pin versions, test the next one on a schedule, and never trust a model's formatting.
- **Meter every call.** Cost per email, times a realistic month's volume, is the projection worth quoting: about ₹88 a month here, against a ceiling of ₹283. Long prompts, retrieved chunks, retries, and verbose answers are where the money goes.
- **A cache saves exactly the share of traffic that repeats**: 17% on a normal day of order emails, far more on repeated support questions. Measure it on your own logs, and never cache live data.
- **Stream what a human waits for**, and keep model calls out of fast paths.
- **Retry rate limits with backoff, fall back on timeouts, degrade honestly.** With the provider failing 20% of calls, 95% of emails were still served.
- **There is no accuracy to monitor**, so watch proxies: refusal, escalation, citation, length, cost, and **topic drift**. Riverstone's refusal rate went from about 15% in weeks 1–4 to 42% by week 7 because customers started asking about a product with no documentation.
- **Log versions, chunk ids, and decisions; store user text deliberately.**
- **The humans are the metric.** Every complaint becomes a golden-set case, and the test suite grows out of real failures.

---

## Key terms

LLMOps · prompt registry · prompt version · golden set · smoke test · evaluation floor · unparseable rate · pinned model version · floating alias · provider upgrade · tolerant parsing · output normalization · token meter · cost per request · monthly projection · ceiling · prompt caching · exact-match cache · hit rate · semantic cache · cache invalidation · corpus version key · latency budget · regional endpoint · time to first token · streaming · rate limit · exponential backoff · timeout · circuit breaker · fallback model · degraded mode · idempotency · escalation queue · refusal rate · citation rate · thumbs-down rate · topic drift · content gap · proxy metric · trace · distributed trace · structured log · retention period · injection monitoring · audit trail · human review loop · complaint-to-test-case

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] My prompts are versioned in Git, each with a golden-set score.
- [ ] The golden set runs in CI with a floor, and fails on any unparseable reply.
- [ ] The model version is pinned, and a scheduled job tests the next version before I switch.
- [ ] My parser survives fences, comments, and a changed date format.
- [ ] I can state the cost per request and the monthly projection without looking anything up.
- [ ] I cache what repeats, I know how much of my traffic that is, and I know what must never be cached.
- [ ] I retry rate limits with backoff, fall back for timeouts, and have a degraded mode.
- [ ] `failed` is a counted outcome that reaches a person with a reason.
- [ ] I monitor refusal, escalation, citation, length, cost, and topic drift.
- [ ] I log versions, chunk ids and decisions, not customer text by default.
- [ ] Every complaint becomes a test case.

---

## Exercises

Work in `companion/ch57`, in the same notebook as the chapter.

### Warm-up

1. Score all three prompt versions and record the token cost of each run. Which version gives the best accuracy per rupee?
2. Run the golden set against `workhorse-002` with Chapter 54's `parse` and then with `tolerant_parse`. Explain both numbers to a non-technical manager in two sentences.
3. What is the cost per email at Chapter 54's four price tiers, and what does section 57.5's month of 1,120 emails cost at each? Does any tier pass ₹1,000 a month?
4. Change the number of resends in section 57.6's day from 8 to 2, and then to 40. What happens to the hit rate and the saving?

### Core

5. Write the CI script: run the golden set, print the numbers, and exit non-zero if accuracy is below 0.70 or any reply is unparseable. Test it against both model versions.
6. Add a fourth prompt version of your own that beats 47 of 60, and record its score and token cost in the registry.
7. Extend `normalize_date` to handle `04 Mar 2026` and `2026/03/04`, and prove with a test that the extraction survives all four formats.
8. Measure the effect of `attempts` in `call_with_fallback`: try 1, 3 and 5 at a 20% failure rate and report served, failed, and cost.
9. Split the week-7 refusals from section 57.9 into content gaps and threshold problems, and say which dominates.
10. Build the weekly digest as a script: golden-set score, cost, cache hit rate, refusal rate, and topic drift, written to a text file.

### Stretch

11. Implement semantic caching with Chapter 55's embeddings. Measure the extra hit rate, then find a pair of questions it wrongly treats as the same.
12. Implement a circuit breaker: after three consecutive failures, skip calling for a fixed period. Show it opening and closing.
13. Route requests by difficulty: short, well-formatted emails to the cheap model, everything else to the pinned one. Report accuracy and cost against sending everything to one model.
14. Simulate a model upgrade that changes *meaning* rather than format (for example, it starts returning quantities as strings). Which of your defenses catches it?

### Think about it (no code needed)

15. Your provider deprecates your pinned model with 60 days' notice. Write the plan.
16. The golden set has been passing for three months. What should make you suspicious?
17. Finance asks you to cut the AI bill by half. Name four levers, in the order you would pull them.
18. When is an LLM feature *not* worth operating, even though it works?

---

## Answers

**1.**

```python
for version in PROMPTS:
    run_meter = Meter()
    result = evaluate(version, meter=run_meter)
    cost = run_meter.cost_rupees()
    print(f"prompt {version}: {result['exact']:>2}/60  cost ₹{cost:5.2f}  "
          f"{result['exact'] / cost:5.1f} correct extractions per rupee")
```

```
prompt v1: 13/60  cost ₹ 4.91    2.6 correct extractions per rupee
prompt v2: 35/60  cost ₹ 3.89    9.0 correct extractions per rupee
prompt v3: 47/60  cost ₹ 4.71   10.0 correct extractions per rupee
```

`v3` is the most accurate and, surprisingly, cheaper than `v1`: its instructions make the model reply with bare JSON instead of a chatty paragraph around it, and output tokens cost five times input, so fewer words out outweigh the extra words in. That is why "shorten the prompt to save money" is the wrong first lever (answer 17 gives the right order).

**2.** *"With the new model version our software couldn't read a single one of the sixty replies, so nothing would have loaded and every order would have gone to a person. After a twenty-minute change to how we read the answer, we're back to forty-seven of sixty, exactly where we were."* The second sentence matters as much as the first: the model was not worse, our assumptions about its output were.

**3.** Price the measured tokens per email at each tier of section 54.12 (the lower price where a tier gives a range):

```python
tokens_in = meter.input_tokens / meter.calls
tokens_out = meter.output_tokens / meter.calls
tiers = [("volume", 0.75, 3.75), ("workhorse", 2, 10), ("strong", 4, 20), ("frontier", 10, 50)]
for tier, price_in, price_out in tiers:
    per_email = (tokens_in * price_in + tokens_out * price_out) / 1_000_000 * USD_TO_INR
    print(f"{tier:<10} ₹{per_email:.3f} an email, ₹{per_email * emails_a_month:5.0f} a month, "
          f"ceiling ₹{per_email * 120 * 30:5.0f}")
```

```
volume     ₹0.029 an email, ₹   33 a month, ceiling ₹  106
workhorse  ₹0.079 an email, ₹   88 a month, ceiling ₹  283
strong     ₹0.157 an email, ₹  176 a month, ceiling ₹  565
frontier   ₹0.393 an email, ₹  440 a month, ceiling ₹ 1413
```

The workhorse tier costs about 8 paise an email and ₹88 for the month. The frontier tier costs five times as much, and even its month, ₹440, stays under ₹1,000; only the ceiling, every day a month-end day, passes it (₹1,413). **The interesting conclusion is that model choice barely matters to this bill.** The human exception queue costs more than every tier: at Chapter 54's nine exception emails a day, say two minutes each, and Riverstone's loaded cost of ₹300 an hour, that is 18 minutes, ₹90 a day, and about ₹1,980 over 22 working days. Do this arithmetic before anyone proposes a cheaper model to save money.

**4.**

```python
for extra in (2, 8, 40):
    rng = random.Random(57)
    day = rng.sample(list(truth), 40)
    traffic = day + [rng.choice(day) for _ in range(extra)]
    cache, cached, plain = Cache(), Meter(), Meter()
    for name in traffic:
        prompt = build_prompt("v3", emails[name])
        cache.get_or_call(prompt, PINNED_MODEL, cached)
        call(prompt, model=PINNED_MODEL, meter=plain)
    print(f"{extra:>2} resends: hit rate {cache.hit_rate():.0%}, "
          f"saved {1 - cached.cost_rupees() / plain.cost_rupees():.0%}")
```

```
 2 resends: hit rate 5%, saved 5%
 8 resends: hit rate 17%, saved 17%
40 resends: hit rate 50%, saved 50%
```

The hit rate is exactly the resends over all requests: 2 of 42, 8 of 48, 40 of 80. The cache cannot create repetition, only exploit it. **That is the honest caveat on any hit rate**: it depends entirely on how much your traffic repeats, and you must measure it on your own logs. A support inbox with thousands of distinct questions may see 20%, which is still worth having; an order inbox where every email is new sees only its resends and retries.

**5.** The companion file `ci_eval.py`:

<!-- run: none -->
```python
#!/usr/bin/env python3
"""ci_eval.py - the golden set as a build step. Exits non-zero if the feature regressed."""
import argparse
import sys

from pipeline import evaluate, parse, tolerant_parse

FLOOR = 0.70
parser = argparse.ArgumentParser()
parser.add_argument("--model", default="workhorse-001")
parser.add_argument("--parser", choices=["strict", "tolerant"], default="tolerant")
args = parser.parse_args()

result = evaluate("v3", model=args.model, parser=tolerant_parse if args.parser == "tolerant" else parse)
print(f"{args.model}, {args.parser} parser: {result['exact']}/{result['of']} ({result['accuracy']:.0%}), "
      f"unparseable {result['unparseable']}, floor {FLOOR:.0%}")
sys.exit(0 if result["accuracy"] >= FLOOR and result["unparseable"] == 0 else 1)
```

`argparse` reads the two settings from the command line (Chapter 18, section 18.15); `choices=["strict", "tolerant"]` rejects any other value for `--parser`, and `default` is used when the setting is left out, and `sys.exit` hands the result to whatever ran the script: 0 for pass, 1 for fail. `parse` is Chapter 54's, which `pipeline.py` imports and passes on. In the terminal, `echo $?` prints the exit code of the last command (Chapter 26):

```
# terminal
$ python ci_eval.py --model workhorse-001; echo "exit code $?"
workhorse-001, tolerant parser: 47/60 (78%), unparseable 0, floor 70%
exit code 0
$ python ci_eval.py --model workhorse-002 --parser strict; echo "exit code $?"
workhorse-002, strict parser: 0/60 (0%), unparseable 60, floor 70%
exit code 1
$ python ci_eval.py --model workhorse-002; echo "exit code $?"
workhorse-002, tolerant parser: 47/60 (78%), unparseable 0, floor 70%
exit code 0
```

The pinned version passes; the new version with the old parser fails on both conditions; with the tolerant parser it passes. Two refinements real teams add: run it nightly against the *latest* provider version as well as the pinned one, and post the numbers to the team channel on success as well as failure, so the absence of a message is never mistaken for a pass.

**6.** Things that help on this data: a second example covering the prose style, an explicit instruction to list every item including several on one line, and a short list of valid product codes. Add the new text to `PROMPTS` as `"v4"` with status `"draft"`, score it with `evaluate("v4", meter=...)`, and record the score *and* the token cost, because a prompt that adds 400 tokens per call to gain one email is a bad trade at 1,120 calls a month and a good one at 12.

**7.**

```python
def normalize_date_extended(value):
    if not isinstance(value, str):
        return value
    value = value.strip()
    if re.fullmatch(r"\d{4}[-/]\d{2}[-/]\d{2}", value):
        return value.replace("/", "-")
    months = {m: i for i, m in enumerate(
        ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}
    match = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]{3,})\s+(\d{4})", value)
    if match and match.group(2)[:3].lower() in months:
        return f"{match.group(3)}-{months[match.group(2)[:3].lower()]:02d}-{int(match.group(1)):02d}"
    return normalize_date(value)

for raw in ["2026-03-04", "04-03-2026", "04 Mar 2026", "2026/03/04"]:
    print(f"{raw:<14} -> {normalize_date_extended(raw)}")
```

```
2026-03-04     -> 2026-03-04
04-03-2026     -> 2026-03-04
04 Mar 2026    -> 2026-03-04
2026/03/04     -> 2026-03-04
```

- `[-/]` is one character that is either a dash or a slash, so the first pattern accepts both year-first shapes; `.replace("/", "-")` makes them the same.
- `months` is a dictionary comprehension: `enumerate(..., start=1)` numbers the month abbreviations from 1, giving `{"jan": 1, "feb": 2, ...}`.
- `\s+` is one or more spaces and `[A-Za-z]{3,}` three or more letters, so `04 Mar 2026` and `4 March 2026` both match; `[:3].lower()` reduces the month name to its key. `:02d` writes a number in two digits with a leading zero.
- Anything else goes on to section 57.4's `normalize_date`.

Four formats, one canonical output, and the validator downstream (Chapter 54's section 54.7) rejects anything that still isn't `YYYY-MM-DD`. Write this as a pure function with a table of test cases: it is the cheapest unit test in the system and it protects against the exact failure in section 57.4.

**8.**

```python
for attempts in (1, 3, 5):
    sweep_meter = Meter()
    routes = {"primary": 0, "fallback": 0, "failed": 0}
    for name in truth:
        _, route = call_with_fallback(build_prompt("v3", emails[name]), sweep_meter,
                                      failure_rate=0.2, attempts=attempts, backoff=0.001)
        routes[route] += 1
    errors = sum(sweep_meter.errors.values())
    print(f"attempts={attempts}: primary {routes['primary']:>2}, fallback {routes['fallback']:>2}, "
          f"failed {routes['failed']:>2}, provider errors {errors:>3}, cost ₹{sweep_meter.cost_rupees():.2f}")
```

```
attempts=1: primary 44, fallback 13, failed  3, provider errors  19, cost ₹3.87
attempts=3: primary 44, fallback 13, failed  3, provider errors  41, cost ₹3.87
attempts=5: primary 44, fallback 13, failed  3, provider errors  63, cost ₹3.87
```

Because this stand-in fails *deterministically* on a given prompt, extra attempts don't rescue it: a prompt that is rate-limited stays rate-limited, and the fallback does the work. Each extra attempt only adds one more error per rate-limited email. Real rate limits are transient, so retries help more than they do here, but the shape of the lesson survives: **most of the benefit is in the first retry and the fallback, and attempts beyond three mostly buy latency.** Measure it on your own provider rather than assuming.

**9.** Take the questions refused in week 7 and look at the top retrieval score for each. Refusals where the best chunk scored far below the floor are **content gaps** (nothing in the corpus is close); refusals where it scored just below are **threshold problems** (the answer was probably there). In this stream the first kind dominates, because the pallet questions have no matching document at all. The two need opposite responses, which is why reporting a single refusal rate is misleading.

**10.** The digest should be one screen: golden-set score with last week's beside it, cost per request and the monthly projection, cache hit rate, refusal and escalation rates, topic-drift indicator, and the prompt and model versions in force. Add one line at the top stating whether anything needs action, and send it to a named person. This is Chapter 56's rule (section 56.7), a daily or weekly digest with a named owner, plus one of its own: **write it for the reader, not for the author, or it stops being read.**

**11.** Embed the question, compare with cached questions, and return a cached answer above a similarity threshold. It buys hit rate on paraphrases ("how long is the warranty" against "what is the warranty period"). The failure to find is a near-neighbour pair with different answers: *"what is the warranty on the crate?"* and *"what is the warranty on the chair?"* are textually close and have different answers. That is why the threshold must be tuned against a set of near-miss pairs, and why semantic caching is inappropriate for anything where a small wording change flips the answer.

**12.** Keep a counter of consecutive failures and a timestamp. Above the threshold, return the fallback immediately without calling the primary for the next *n* seconds, then allow one trial call through ("half-open"). If it succeeds, close the breaker. The effect to demonstrate: with the breaker, a sustained outage costs one failed call per cooldown period instead of three per request. The wider benefit is on the provider's side, and being a good client is also self-interest when rate limits are shared.

**13.** Route by a cheap signal: email length, whether it matched the table format, whether a PO number is present. Expect the cheap model to handle the tidy majority and the expensive one to earn its cost on the messy minority. Report **accuracy per rupee** for three strategies (all cheap, all expensive, routed). The routed strategy usually wins, and the risk to watch is that the router itself becomes a thing to maintain and evaluate: a bad routing rule silently sends hard cases to the weak model.

**14.** Quantities returned as `"20"` instead of `20` pass JSON parsing, pass a tolerant parser, and fail Chapter 54's **validation** (`isinstance(quantity, int)`), which is the defense that catches it, and the golden-set comparison, which would show accuracy collapsing while `unparseable` stayed at zero. That combination is the signature of a meaning change rather than a format change, and it is why both signals belong in the CI output rather than one summary number.

**15.** Day 1: run the golden set against the replacement and record the delta. If it passes, pin the new version in a branch, run a week of nightly comparisons, then switch with the old version still pinnable. If it fails, spend the time on tolerant parsing and prompt adjustments rather than panicking, because most regressions are format drift. Also re-check cost and latency, since a new model can change both without changing the price, and tell the business what to expect. **Sixty days is comfortable if the test exists, and impossible if it doesn't**, which is the argument for building it now.

**16.** Be suspicious of a test that never fails. Likely causes: the golden set is too easy, it has not grown as new failure modes appeared, or it is being run against a cached response rather than the live provider. Check three things: when the last case was added (it should grow with every complaint), whether a deliberately broken prompt still fails it, and whether the nightly job is actually calling the provider. **A green test that cannot go red is a decoration.**

**17.** In order: (1) **cache**, the largest single lever where traffic repeats, and it changes nothing about quality; (2) **shorten what is re-sent every call**, meaning the system prompt and the number of retrieved chunks, with the golden set confirming quality holds; (3) **cap output length**, since output costs several times input; (4) **route easy requests to a cheaper model**, measured for accuracy per rupee. Only then consider a cheaper model for everything, and re-run the golden set before promising anything. Also check the boring possibility: development and evaluation runs are sometimes most of a small bill.

**18.** When the volume is so low that a person does it in ten minutes a week; when a wrong answer is expensive and the failure is silent, and no validation can catch it; when nobody will own the golden set, the prompts, or the complaints, so the system will decay unobserved; when the data cannot leave the building and a local model is not viable; and when the process it automates is broken, because automating a broken process just produces wrong answers faster. **The operating cost of an LLM feature is mostly human attention**, and a feature nobody has time to watch should not be running.

---

## Where this leads

- **Chapter 58, Intelligent Automation,** connects this pipeline to systems that write, where a wrong answer creates a record rather than a sentence.
- **Chapter 56, MLOps,** is the same discipline for models you own; read the two together.
- **Chapter 55, Building AI Applications,** built the assistant and the test questions this chapter monitors.
- **Chapter 54, Generative AI & Large Language Models,** is where the prompts, the golden set, tokens, and prices come from.
- **Chapter 47, Data Quality, Observability & Contracts,** treats the corpus as data with owners, statuses, and freshness.
- **Chapter 64, Security, Privacy, Governance & Responsible AI,** covers disclosure, retention, and accountability for automated answers.
- **Chapter 79, GenAI, LLM & MLOps Question Bank** (sections 79.5 and 79.7), has the interview questions on LLM cost, caching and evaluation.
