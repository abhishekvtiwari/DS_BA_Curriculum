# 3 October 2026 · New chapter 72B: Data Cleaning & Wrangling Question Bank

100 questions, Q72B-001 to 100. Nothing renumbered anywhere; `72b` registered in
`PART_PACKAGES['8']` between `72a` and `73`. Book 4 rebuilt: **535 → 648 pages**, chapter at
pages 279–333, 50 bookmarks, 406 contents links resolved. `check_bank.py`: 150 code fences
balanced, no duplicate or missing codes, all 32 core questions carry all five required parts,
0 uneven table blocks.

Abhishek asked for data wrangling as part of the push to ~1,160 questions. Part VIII is now
**1,056**.

## What makes this chapter different from every competitor's cleaning material

It runs on two real messy files that already ship with the book — `companion/ch14/orders_q4_2025_export.csv`
(25,976 rows) and `customers_crm_export.csv` (5,027 records) — **and Chapter 14 also ships
`clean_truth_orders_q4_2025.csv`, the correct answer.** So every defect has a verified count and
every fix has a verifiable result. Nobody selling an interview book can offer that, because it
requires having built the dirty data and the ground truth together.

| | |
|---|---|
| 72B.2 Profiling | What to do before you change anything |
| 72B.3 The row count | Duplicates, repeated headers, footers |
| 72B.4 **Dates** | Four formats in one column; the strongest section in the chapter |
| 72B.5 Categories and text | 18 spellings of 4 statuses |
| 72B.6 Numbers, units and money | Currency text, percent-vs-fraction, cartons, typed zeros |
| 72B.7 **Keys, joins and match rates** | The silent 537-row loss |
| 72B.8 Missing values and validation | The four actions; rules that must return zero |
| 72B.9 Full rapid-fire | 28 rows |
| 72B.10 Reproduce every number | The setup, and where the measurements differ from the answer key |

## The three findings worth the chapter

**1. No single `pd.to_datetime` call parses the date column correctly.** `errors='coerce'` with
defaults destroys **17,089 of 25,969** dates (66%). Adding `dayfirst=True` drops that to 5,088 —
and silently corrupts the 3,227 ISO values instead, because pandas reverses `2025-10-01` into
10 January. **Both `format='mixed'` variants report exactly 49 NaT**, so no null check can detect
either bug. The naive parse spreads **₹12.78 crore of Q4 revenue across nine months the file does
not cover.** Only shape dispatch with explicit per-format parsing works: it covers all 25,969 rows
and leaves exactly the 9 genuinely impossible dates.

**2. The obvious price cleaner is wrong, and produces the more believable wrong answer.**
`str.replace(r'[^0-9.]', '')` turns `Rs. 1,400` into **0.14**, because it keeps the dot from "Rs.".
The 1,205 `Rs.`-prefixed rows are destroyed; the 1,111 rupee-sign rows survive, which is why it
passes a spot check. Three totals, all from code that looks reasonable: `to_numeric` alone
₹41.87 cr, character-class strip ₹43.89 cr, **correct ₹46.01 cr.**

**3. A total can be right for the wrong reasons.** Cleaning prices and discounts but nothing else
gives ₹44.38 cr against the truth file's ₹44.26 cr — within 0.28%, and meaningless: 137 duplicates
(+₹0.25 cr) and 6 extra-zero quantities (+₹0.11 cr) inflate it while 141 unconverted carton rows
(−₹0.22 cr) understate it. Q72B-069 decomposes it and shows the correct pipeline landing at
₹44.24 cr, −₹1.90 lakh (−0.043%) from truth, with the residual named.

## Errors caught by running the code, recorded rather than quietly fixed

Every one of these was in a draft of this chapter, and each was found by executing what had been
written instead of trusting it. They are listed because the chapter's whole argument is that this
is the only thing that works.

- **The price regex above.** Found because the Q72B-068 validation suite returned **1,197** on
  `price not a known price`. A null check could not have found it — `0.14` is a valid number.
  Only set membership caught it, and that is now said in the chapter.
- **"12 pieces per carton" was invented.** The truth file shows those 141 rows summing to 5,400
  against 540 raw, so Riverstone's factor is **10**. Q72B-047 now reports the wrong assumption as
  part of the answer, because the point of the question is that the factor comes from the product
  master and never from intuition.
- **The status mapping table was missing `cxl`**, leaving 32 rows unmapped and `Cancelled` at
  1,068 instead of 1,100. This is exactly the failure Q72B-035 teaches, so it is now stated there
  as having actually happened.
- **The "leading zeros are lost on a default read" lesson was false on pandas 3.0.** Every column
  reads as `str`, partly from the new string default and partly because the 6 repeated header rows
  put text in every column. Q72B-002 was rebuilt around the better finding: remove the junk rows
  first — the correct step — re-read, and `customer_code` *then* becomes `int64` and loses the
  zeros. The default read was only ever safe because the file was dirty.
- **Invented header-row positions.** Claimed every 4,001 rows; actually 4,028/8,047/12,061/16,090/
  20,109/24,130, with gaps of 4,019–4,029. Pagination is still the right diagnosis but the page
  size is now stated as an inference, not a measurement.
- **Crore arithmetic off by 10×** in two places (₹423 crore for ₹42.3 crore).
- **Three smaller corrections:** duplicate `order_item_id` is 137 not 138; `order_id` duplicates
  11,597 not 11,598; `entered_at_utc` needs `format='ISO8601'`, not a space-separated pattern.

## Where the measurements differ from `answer_key.json`, and why

Recorded in §72B.10 rather than reconciled away. Most figures in the chapter are quoted on the
**25,969-row body** (the file minus 6 header rows and 1 footer row, **still containing the 137
duplicates**); the answer key and truth file are quoted on the **25,832** de-duplicated lines.

| | Chapter (measured) | `answer_key.json` |
|---|---|---|
| Currency-text prices | 2,316 | 2,300 |
| Fractional discounts | 1,371 | 1,362 |
| UTC date ≠ IST date | 1,604 | 1,598 |
| Codes without leading zeros | **537** | 3,210 |

The first three differ by the duplicates. The last is a different case and worth a note for
whoever maintains Chapter 14: `codes_without_leading_zeros: 3210` equals the Kolkata branch line
count exactly, so it appears to record the number of rows the generator *targeted*. Only the
**537** whose code actually begins with a zero lose a character and fail the join — 40 two-character
and 497 three-character codes against a uniformly four-character master. `zfill(4)` takes the
failure count to 0. Not changed, since `answer_key.json` is Chapter 14's file, not this chapter's.

## Verified on

Python 3.12.0, pandas 3.0.2, numpy 2.4.3. Every output in the chapter was produced by running the
code against the shipped files. The one version-dependent behaviour (pandas 3.0 string inference,
Q72B-002) is called out in the chapter itself.

## Not done

- §70.9 is still the only unverified section in Part VIII (needs Excel).
- ~104 questions remain to reach ~1,160.
- Cover and back cover still to design.
