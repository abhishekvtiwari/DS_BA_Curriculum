# Chapter 69A changelog (Why This, Not That: Tool Choice & Judgement)

# 3 October 2026 · New chapter

**Why.** Abhishek's observation, and a correct one: the book is heavy on *how* and thin on *why
would you*. 767 questions that mostly assume the tool has already been chosen — while the first ten
minutes of a real interview are exactly that conversation, and it is where a candidate sounds like
a professional or like someone who learned a syllabus.

His examples were the right ones: why Python and not Excel, why Postgres and not MySQL, what the
difference between SQL and Postgres even is.

**Chapter 69A, "Why This, Not That: Tool Choice & Judgement."** 10,157 words, 12 core questions and
48 rapid-fire rows — **60 questions**, Q69A-001 to 060. Placed between Chapter 69 (how to answer)
and Chapter 70 (the tool banks), because judgement comes before depth.

Nothing was renumbered. The chapter uses the letter-suffix convention the book already has for 72A,
76A and 76B, and was added to `PART_PACKAGES['8']` in `tools/pdf/build.py`.

## Sections

| | |
|---|---|
| 69A.1 | Why these questions decide the first ten minutes |
| 69A.2 | The vocabulary that trips people up — SQL against PostgreSQL, pandas against Python, what a notebook actually is |
| 69A.3 | Excel, or code? |
| 69A.4 | Which database, and why |
| 69A.5 | Which language, and when |
| 69A.6 | When not to use the clever thing |
| 69A.7 | Defending a choice you did not make |

## The measurements, which are the point

Most books answer "why not Excel?" with an opinion. This chapter measures it, on Riverstone's own
full dataset, and **the measurement contradicts the usual answer**:

| | |
|---|---|
| `order_items` | **209,006 rows — fits in Excel comfortably** |
| Excel's limit | 1,048,576 rows |
| Join + revenue + group by customer, pandas | **62 ms** |
| Writing 200,000 rows: csv / xlsx / parquet | **0.4 s / 14.1 s / 0.3 s** |
| Same, file size | 9.7 MB / 7.8 MB / 2.8 MB |

So Q69A-015 opens by **killing the standard answer**: "Excel does not scale" is wrong at the size
most analysts work, and a candidate who says it is repeating a line. The real reasons are
repeatability and auditability, and the question says so with the numbers. It also names the case
where Excel is the correct choice, which is the part that earns the extra point.

## The character of the chapter

Three things make it different from the tool banks:

1. **It refuses to declare winners.** Q69A-023 on PostgreSQL against MySQL says plainly that for
   most work there is no difference that matters, then names what would actually decide it.
2. **Section 69A.6 is about restraint** — when *not* to use machine learning, an LLM, an
   orchestrator, microservices, the cloud, a rewrite. Nine of its questions have "no" as the strong
   answer, which is where senior candidates separate themselves.
3. **Section 69A.7 is about defending a choice you did not make**, which is most of the choices you
   will be asked about, and where "it was already there" is honest and weak.

## Running total

Part VIII: **767 questions to 827.** The expansion target is about 1,160, so roughly 330 remain —
situational and tricky, Python and pandas, the DA/DS role bank, HR and behavioural, and data
wrangling.
