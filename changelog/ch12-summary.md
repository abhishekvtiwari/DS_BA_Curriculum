# Chapter 12 — Databases & SQL Foundations: summary (Parts 2 and 3 build)

**What changed**
- **Install just in time (§12.3).** PostgreSQL now gets the same care as MySQL: Windows/macOS/Linux steps, the words localhost/port/driver, how to edit a connection, a troubleshooting box, and both check queries with real output. New optional step loads the one-year database. New box "Running your first query in DBeaver". Terminal commands are glossed; the command-line load waits for Chapter 26.
- **Order of ideas.** ORDER BY/LIMIT/DISTINCT moved up to a new §12.5 (WHERE → §12.6, NULL → §12.7). Dates come before the overdue example. Joins are no longer used before §12.10 (the profit example moved there) and subqueries not before §12.12 (the money fix and the segment grid moved there). The MySQL monthly report now follows its PostgreSQL original.
- **One idea per cell.** Calculated columns, BETWEEN/IN, the margin query, the aggregates, line revenue and the per-order SUM are built up in small runs. New runs show the half-open range, NOT IN vs NOT EXISTS, UNION ALL, EXCEPT, text functions on real rows, 0.1 + 0.2, ROUND ties, COLLATE, and the four join-building row counts.
- **New worked material.** Rebuilding Figure 12.2's order slip; Question 5 "Why did March fall?" (Chapter 5's issue tree as five queries, every number matching Chapter 5); exercises 30–33 (Chapter 7's quiet customers on 2025 data, rounding predictions, Chapter 11's pivot in SQL, the IT request).
- **Reader aids.** "Plan your sittings" box and eight "Good place to stop" lines; a note on psql-style output vs the DBeaver grid; PostgreSQL/MySQL labels on every dialect pair in §12.13; DBeaver's import wizard as the taught CSV route.
- **Figures.** All five redrawn from a new `figures/make_figs12.py`, smallest text 7.0–8.1 pt (was 4.7–6.6 pt); Figure 12.2's bands now name their tables; the half-empty page is gone.
- **Consistency.** 31 March 2026 is a Tuesday; gross value instead of "list value"; four MySQL behaviours, not three; lakh grouping in prose; the Flash lands by 7:30; Chapter 45 for upserts and Chapter 64 for access.

**New Time needed:** 22–26 hours for the PostgreSQL core, plus 6–10 hours for the MySQL track and the project, over four to five weeks (was 19–23 hours).

**Checked**
- `verify_sql.py`: 263 statements run, 175 outputs checked, **0 mismatches** (was 1).
- `sql/ch12_companion.py`: 106 queries run in both databases, 0 unexplained differences; the companion query files and both lab files run end to end.
- `restructure.py --check`: already in order. `fig_check`: 0 figures under 7 pt.
- Rebuilt PDF (126 pages): no stranded headings or lead-ins, no sparse pages, no small text, no clipped lists, tofu 0; draft_labels only "draft basket" and "sales coordinator" (reader text). Pages with figures, the CSV section, MODIFY pairs and the cheat sheet were rendered and inspected.

**Skipped, and why**
- **RJ-S2-10, RJ-S3-10:** held Open by the reading-order decision.
- **12.41 (part):** the chapter says what was really tested (PostgreSQL 16, MySQL 8.0), not "16–18 and 8.4/9.7"; the Chapter 13 wording belongs to Chapter 13.
- **12.22 / 12.50 optional parts:** Steps 10–11 not boxed as "Reference"; §12.11 not moved.
- **12.1, 12.27 screenshots:** can't be made here; listed for Abhishek.
- **12.32 (Ch 13 part), RJ-S3-15 (Ch 13 part), RJ-S3-78:** belong to other chapters.

**Option picks:** 12.5 gloss (first option); 12.21 (b) with 12.32's recommended option (load riverstone_2025 in §12.3); 12.23 box; 12.46 add "ignore cancelled orders"; V12.6 two rows of four; V12.11 text labels; 12.38 modified to fit D8 (MySQL report moved after the original instead of moving "In the real world").
