# Chapter 82 summary: Take-Home Assignments & Mock Interviews

**Rows:** 28 content (82.1–82.28) and 3 visual (V82.1, V82.2, V82.9) approved for this chapter: all fixed and checked in the rebuilt PDF or by a verifier. Visual rows V82.3–V82.8, V82.10, V82.11 were done by the style pass; V82.3 and V82.7 re-checked (V82.7's wrapped header renamed). Multi-chapter rows: 81.14 was done in Ch 81 (Ch 82 now cites Q81-002); RJ-S3-57 needs nothing more in Ch 82. Nothing left Open.

## What changed

- **Opening:** the drafting scope note ("blueprint", "this chat") is gone. A Part 8-style "Chapter at a glance" box now says what the chapter covers, who can adapt which take-home, what to read first, and the time needed.
- **New §82.0, "Is this a fair take-home?"**: the fair signs, the warning signs, and what to do about them. This keeps Chapter 8's promise.
- **§82.1, the DA take-home:** now four real queries on `riverstone_2025`, all rounded and reconciled: revenue, orders and customers; spend per order at the right grain; growth by quarter (H2 against H1); and profit, margin and discount. The recommendation changes. Kitchen and Industrial drive growth, but at a 13.6% margin Industrial earns about the same profit per order as Kitchen. So the crate discounts should be reviewed before any Industrial push.
- **§82.2, the DS take-home:** rebuilt from six real notebook cells on the lead data (`companion/ch82/lead_data.py`). Logistic regression ties with tuned boosting on validation and beats it on test (0.838 against 0.830), so the simpler model ships. The cost threshold is 0.077 (₹24.5 lakh against ₹10.8 lakh). The capacity limit is 504 leads, which gives ₹23.3 lakh. The confusion matrix is shown at the threshold actually used. The churn/lead number mix-up is gone.
- **§82.3, the DE take-home:** a stateful lab in `riverstone_lab` on the mini database:
  - an `IF NOT EXISTS` table with `NOT NULL` and `CHECK` rules;
  - a delete-and-insert window inside one transaction;
  - two real failure tests: a cancellation removes a stale day, and a 150% discount fails loudly and rolls back;
  - a per-day reconciliation data test that returns 0 rows.

  The design note separates atomicity from re-run safety, and explains why an upsert leaves stale days.
- **Mocks §82.4–82.6:** each is labelled with its level and uses Ch 69's exact dimension names and tags. The long answers are written out. Each mock has two "weaker answer, same turn" lines with their scores.
  - The DA candidate writes `NOT EXISTS` and explains the `NOT IN` trap.
  - The DS leakage mechanism is corrected.
  - The DE mock is now a borderline pass (3, 3, 2, 3, 3), with the interviewer's hire reasoning.
- **Pointers:** every "Learn it in" names teaching chapters and sections. The drill banks move to "Practise it with", and every Q-ID was checked against the current bank files.
- **Review stage:** a Final-week revision list was added (V82.9).

## Option picks

- 82.3: Option B, rerun the lead-data comparison.
- 82.13, 82.16, 82.20, 82.26 and V82.9: option (a).
- 82.17: the checks can fail through constraints and a data test. A `DO $$ … RAISE` block isn't taught anywhere in the book, so it isn't used.
- 82.28: lakh throughout.

## Time needed (new)

2–3 hours to read the chapter and run everything. About 10–12 hours with all three timed take-homes (2 + 3 + 2 h), review against the scoring tables, and one recorded mock. The old chapter stated no time.

## Code verification

- `verify_sql.py`: 24 statements run, 12 outputs checked, 0 mismatches. That covers 4 on `riverstone_2025` and 8 in the lab, including the expected CHECK error.
- `verify_python.py --cwd companion/ch82`: 6 blocks, 6 outputs, 0 mismatches.
- `checks/ch82_check.py`: 39 prose numbers recomputed from the databases, all passing. This includes the upsert stale-row claim, run in a scratch database.
- `check_code_teaching.py`: 2 residual flags. One is the hidden verifier `\i` block, which isn't printed. The other is the reconciliation query's column names, which are explained in the bullets.

## Skipped

Nothing.
