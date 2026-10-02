# Part VIII: the predict-the-output work

*3 October 2026 — what was built, what was deliberately not, and the one decision I would like from you.*

## Why this happened

You asked for the interview material to be ground down "from very basic to very detailed," with
brain-racking questions of the `int("25", 4)` kind. I measured Part VIII before starting: of its
**619 questions, only 19 were output-prediction**, and **17 of those 19 were in a single section** —
Chapter 72's §72.2. Thirteen of the fourteen banks had none at all.

You read §71.11 and approved its depth. This is that standard applied across the rest.

## What was built

**Ten new sections. 202 new questions. Part VIII goes from 619 to 821.**

| Ch | Bank | New section | Core | Rapid | Was → Now |
|---|---|---|---|---|---|
| 70 | Excel, Sheets, VBA & BI | 70.9 What the grid does behind the number | 6 | 10 | 71 → 87 |
| 71 | SQL | 71.11 Predict the output | 16 | 16 | 76 → 108 |
| 72A | Data Structures & Algorithms | 72A.10 Predict the output | 16 | 16 | 30 → 62 |
| 73 | Statistics & Experimentation | 73.8 Arithmetic that quietly goes wrong | 8 | 11 | 37 → 56 |
| 74 | Machine Learning | 74.8 What the library did that you did not ask for | 10 | 10 | 36 → 56 |
| 75 | Product Sense & Metrics | 75.7 Metric arithmetic | 7 | 8 | 31 → 46 |
| 77 | Data Engineering | 77.8 What happens to rows on the way in | 9 | 12 | 35 → 56 |
| 78 | Automation & Integration | 78.7 Schedules, retries and defaults | 7 | 10 | 28 → 45 |
| 79 | GenAI, LLM & MLOps | 79.9 The arithmetic behind an AI system | 6 | 10 | 39 → 55 |
| 80 | Architecture & Leadership | 80.7 The arithmetic of a design | 6 | 8 | 29 → 43 |

Every section follows §71.11's shape: a memory hook, a one-line answer, the code, its real output,
a three-tier table, likely follow-ups, a red flag and a *Learn it in* pointer. A script checks that
every question has all five required parts, that no code is duplicated or skipped, and that no
table has a ragged row. All ten pass.

**Every answer was run.** Nothing was typed from memory.

## Three banks I did not touch, and why

This is the part I would most like you to look at, because it is a judgement call.

**Chapter 76A — Data Analyst & Data Scientist.** This bank is entirely about career positioning and
defending your own work: "walk me through a project you're proud of", "defend this number on your
resume", "why this role and not that one". There is no technical or numeric content for a
predict-the-output question to attach to. Adding one would be padding.

**Chapter 81 — Behavioural, HR & Offer Conversations.** Same reason for the behavioural part. The
one numeric topic — CTC against in-hand pay — **is already covered**, in Q81-024, with a worked
₹6 lakh breakup table. A second treatment would duplicate it.

**Chapter 82 — Take-Home Assignments & Mock Interviews.** It has no coded questions at all. It is a
different format — briefs and rubrics — and should stay that way.

## The one decision I would like from you

**Chapter 76B, the Business Analyst bank**, is the borderline case. Its content is requirements,
BRDs, user stories, BPMN and UAT — so "predict the output" does not fit it either.

But there *is* a genuine equivalent for a BA, and it is arguably the BA's core skill: **given a
written requirement, what is ambiguous, and what will break when it reaches a developer?** A section
of "here is a requirement as a stakeholder wrote it — find the three things that are undefined"
would drill exactly that.

It is a different format from the other ten, so I have not built it unilaterally. **Say the word and
I will.**

## What the work kept finding

Worth knowing, because it changed what got built:

**These banks were better covered than the headline number suggested.** Chapter 73 already simulated
peeking *and* the rare-disease Bayes problem. Chapter 74 already had leakage in four questions.
Chapter 70 was already the largest bank in the book. So rather than hitting a quota, each section
was aimed at what its chapter genuinely lacked — which is why Chapter 71 got 32 new questions and
Chapter 73 got 19.

**Four questions were cut for duplicating existing ones**, in Chapter 73. Keeping the peeking
question would have printed 26.2% beside the existing Q73-025's 16.3% — both correct for their own
number of looks, and together a contradiction a reader would have had to untangle for nothing.

**About a dozen drafted questions were wrong, and running them is the only reason they are not in
the book.** A few examples:

- `RANK` on the tied months gives 4, 4, 4, not the 1, 1, 1 I had written.
- `257 is 257` is `True` in Python 3.12 — the compiler folds the literals, so the obvious way to
  write that question teaches the opposite of the truth.
- Removing the even numbers from `[1,2,3,4,5,6]` while looping gives the *right* answer, so the
  famous skip bug is invisible on that data.
- `sum([0.1]*10) == 1.0` is `True`, and a million rupee amounts summed as floats matched the exact
  integer total — so the float-money question was cut rather than dressed up.
- pandas already treats `'N/A'` and `'NULL'` as missing, so that trap was backwards; the real one is
  a legitimate `NA` meaning *North America* being destroyed on the way in.
- Parquet was **slower** than CSV for a full read of a 300,000-row file. The question says so, and
  puts the real advantages where they belong.

Each of those is recorded in the chapter's changelog rather than quietly corrected.

## What is honestly outstanding

1. **Chapter 71's §71.11 has still not been run on PostgreSQL 16 and MySQL 8.4.** Neither is
   installed here. Its outputs are labelled *Run (riverstone_2025)* rather than *Verified*, and four
   questions are marked **Dialect split**.
2. **Chapter 70's §70.9 was not run in Excel**, for the same reason. Four questions carry a
   **Check in Excel** mark naming the documented behaviour and why it is worth confirming.
3. **Book 4's visual check should be redone.** It has grown substantially.

Neither of the first two is hidden in a changelog — both are stated in the chapter's own
at-a-glance box, so a reader is told before they rely on it.
