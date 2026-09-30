# Chapter 71 — one-page summary

**What changed.** The drafting notes are gone, and the chapter now reads in the order the review asked for: core → tricky basics → aggregation → subqueries and CTEs → window functions → classic problems → schema, constraints and transactions (old §71.4 and §71.8 merged) → dialects → optimization → live walk-throughs. The questions are renumbered Q71-001 to Q71-076 in page order, and each rapid-fire table is titled after its own section. Every question has a level (Warm-up, Core or Advanced) and a section-level "Learn it in" pointer, checked against the current Ch 12, 13, 14, 27, 28 and 49. Recursive CTEs point to Ch 28 §28.2, EXPLAIN and indexes to Ch 28 §28.4–28.6, and ACID to Ch 49 §49.4. Rows the book doesn't teach say *Beyond the book*. A short "concurrency in five minutes" box covers isolation levels, a dirty-read timeline and MVCC.

Wrong answers corrected:
- TRUNCATE and identity counters;
- PostgreSQL's default `NO ACTION` for foreign keys;
- MySQL's default isolation level (Repeatable Read);
- `CURRENT_DATE` in MySQL;
- the self-join error;
- the default window frame (`RANGE`);
- integer division;
- "longest streak", which now really keeps one streak per customer;
- the top-2-per-category output, which now matches its query;
- the pivot, which now has all four categories and reconciles.

Every result is a real psql/mysql grid naming its database. MySQL gets its own blocks wherever the syntax differs. The foreign-key demos use table-level `FOREIGN KEY` on ordinary lab tables, as Ch 12 recommends. Tags are Ch 69's twelve. The revision list has 20 IDs.

**Code verified.**
- `tools/verify_sql.py --db riverstone_2025`: 60 statements run, 48 outputs checked, **0 mismatches**. It passed on six servers: the shared PostgreSQL 16.13 and MySQL 8.0.46, plus scratch containers running PostgreSQL 16.15, 18.6 and MySQL 8.4.11, 9.7.2.
- `checks/ch71_check.py` (new) makes 41 more comparisons, all OK on every server set:
  - the view (Q71-049) and index (Q71-068) cells, run in PostgreSQL inside BEGIN … ROLLBACK so the shared database is unchanged;
  - the MySQL versions printed as "returns the same rows";
  - every number stated in prose, such as TRUNCATE/RESTART IDENTITY, NULLS NOT DISTINCT, 175/164, 5/8/10, the 23 and 23, ₹43,35,471, RANGE = ROWS, `cte_max_recursion_depth` 1,000, `group_concat_max_len` 1,024 and the MySQL 3593 error.
- Throwaway tables go in `riverstone_lab` (the verifier's lab) or `scratch_ch71`, which is dropped at the end.
- One real finding from the newer versions: MySQL 9.7 prints EXPLAIN as a tree by default. The chapter now asks for `FORMAT=TRADITIONAL` and prints it with `\G`, and it says why.

**Build.** 45 pages.
- layout_check: map 13/13, no stranded headings or lead-ins, no sparse pages, no small text, no draft labels, tofu 0.
- prescan: 0 draft labels; the 6 hyphen breaks are all real hyphens.
- fig_check: 0 figures (the chapter has none).
- restructure --check: already in order.
- Before/after crops for V71.1 and V71.2 are in `changelog/img/`.

**Option picks.** Option (a) throughout:
- 71.9 adds Q71-009 to the revision list.
- 71.17 explains in-chapter with a Beyond-the-book box, rather than asking for a Ch 49 box.
- 71.18 needed neither option: Ch 14 §14.4 already teaches `STRING_AGG` and `GROUP_CONCAT`, so the pointer goes there.

**Skipped or partial.**
- 71.23's optional role tags were not added (see questions).
- 71.7's cross-chapter citations in Ch 77 and Ch 79 are listed for the integrator (Ch 72's were already updated).
- No row is left Open.

**Time needed (new).** 3–4 hours for a first pass, plus 6–8 hours to run every core question yourself in both databases, plus 1 hour for the final-week list. The chapter had no estimate before. The estimate allows about 5 minutes per core question and 1 per rapid-fire row to read (31 core questions and walk-throughs, 45 rapid-fire rows), and 10–15 minutes per core question to type and run in two engines.
