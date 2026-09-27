# New standard for all chapters: teach code line by line (instructions §6.5)

*Paste this whole note into the Part II-A chat, the Part III chat, and every new part chat when it starts. Coordinator, 18 September 2026.*

---

Abhishek has raised the book's most important quality gap so far, and it changes what "done" means for every chapter that contains code.

**The problem:** chapters show working code and correct output, but they do not teach it. A first-time reader looks at a block and cannot answer: what does each line do? what is that setting? what happens if I change it? what do I change to use my own data? Chapters read as *written for someone who already knows*, which is the opposite of the book's promise.

**The fix:** `planning/chapter-writing-instructions.md` now has **section 6.5 "Teaching code and formulas line by line (the beginner rule)"**, and the Definition of Done has a new required item. Re-read §6.5 before writing your next chapter. Summary:

## The five-part pattern for every first-time example

1. **The question, in plain words** — "Which customers are likely to stop ordering?"
2. **The plan in words before any code** — 2 to 5 sentences or a numbered list, in the order the code does it, followable without knowing the language.
3. **The code** — short enough to read on one screen (12 to 20 lines the first time an idea appears; split longer work into steps that each get their own explanation).
4. **The real output**, exactly as the tool prints it, plus a sentence on **how to read it**: what the columns mean, what "good" looks like.
5. **"How it works": one bullet per line or per clause.** Name the thing, say what it does *here*, say what it would do with different data. Never skip a line for looking obvious — `import pandas as pd` is new on someone's first day.

## Settings and parameters

The first time a function, verb, or model takes settings, include a table:

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `test_size=0.2` | share of rows held back to test the model | 0.2 (20%) | smaller: less reliable test; larger: less data to learn from |

Then **run at least one changed version and paste the real output**, so the effect is measured, not asserted. A small results table (setting value → result) is better still.

## Other rules

- **First use is explained use** — every function, keyword, argument, and file format gets its plain-English meaning the first time it appears, and goes in *Key terms*.
- **No silent magic** — no unexplained imports or helper functions; no "don't worry about this for now" unless you say exactly where it is explained.
- **Show the error** — run the wrong version, paste the real error, then fix it.
- **Predict before running** — at least once per teaching section.
- **A changed-line exercise** — every code-teaching section ends with one.
- **Class A and B chapters** keep a *"Code words you met in this chapter"* table (term, plain meaning, first section).
- **Statistics and ML chapters:** the same standard applies to the math. Every formula gets a plain-English sentence, a worked example with real numbers, and a statement of what happens when its inputs change. **A model is explained by what it does to one row of Riverstone data before any library is imported.**

## New Definition of Done item

```
- [ ] Every code block, formula, and query explained line by line (section 6.5);
      `python3 tools/check_code_teaching.py manuscript/chNN-….md` reports no unexplained blocks
```

`tools/check_code_teaching.py` is in the project (`tools/` folder). It reads a manuscript and flags code blocks with no prose before them, no explanation after them, low coverage of the identifiers used, or a length over 25 lines; it also flags parameters that appear in code but never in prose, and chapters with no "what happens if you change" and no "predict before you run" text.

**A flag is a question, not a verdict.** Deliberate exceptions (a repeated pattern already taught, an output-only block) are fine — list them in your chapter report with one line each saying why.

## What this means for chapters already approved: no rewrites now

Abhishek's instruction, 18 September 2026: **do not retrofit chapter by chapter now.** Finish building your part. When the part is complete, fix everything inside it in one pass, in place, so the teaching flow is not disturbed, and only after a proper review and a deeper understanding of each issue.

So:

- **Every new chapter from now on follows §6.5 as it is written.** This is not deferred. The checker item is part of the Definition of Done before you call a chapter finished.
- **Chapters already approved in your part stay as they are for now.** Do not open them.
- **When the last chapter of your part is approved, run the part-completion review pass** (new instructions **§15.1**). Read the part straight through as a reader would before editing anything; list the problems; work out the cause of each one at the level of the part (a missing sentence, a wrong teaching order, an unpaid promise) before making any fix; then fix in place, re-run every check and figure script for the chapters you touched, rebuild those PDFs, and report what you changed and what you deliberately left alone.
- A checker flag is a pointer to a place to read, never a reason on its own to edit. Read §15.1 in full before you start that pass.
- **Part IV (machine learning) must follow §6.5 from its first chapter.** This is where the gap hurts most: no `model.fit(X_train, y_train)` without the reader knowing what `fit` does, what `X` and `y` are, what the split did, and what changes if the split changes.
- **Part II-A:** you may run `tools/check_code_teaching.py` over Ch 10, 11, 14, 15 now and send the counts with your next status update, as input to your later review pass. Do not rewrite anything yet.

## Current baseline (coordinator's run over chapters already in the project)

| Chapter | Code blocks | Flagged |
|---|---|---|
| Ch 12 Databases and SQL Foundations | 167 | 33 |
| Ch 13 SQL for Real Analysis | 45 | 21 |
| Ch 6 Setting Up to Learn | 5 | 3 |

These three sit in Part 0 and Part II and are the chapters other chats copy from. They stay as they are for now. The coordinator will fix them inside their own parts' review passes, under the same rule: read first, find the cause, then fix in place.
