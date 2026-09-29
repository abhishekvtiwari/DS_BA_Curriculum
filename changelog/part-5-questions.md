# Part 5: questions for Abhishek

The chapter agents' questions, in reading order, each trimmed to the decision it needs. None of them blocks the
Part 5 PDF: every chapter builds, and where a question offers options, the text as it stands follows the one
described as current.

## Story and facts (these wait on the fact sheet, PR #3)

1. **The Part 5 story calendar and cast (RJ-S2-18, Open).** Several stories are affected:
   - Ch 45: "went live in February" has no year.
   - Ch 46: "two months after", "the data engineer" is unnamed.
   - Ch 47: the story sits in the same week as the 5 January exercise, and "the analytics engineer" is unnamed.
   - Ch 48: "about 200 machines" in the story, against 25 in the dataset.
   - Ch 49 and 50: undated stories.

   Each is a small edit once the calendar and the cast are approved.
2. **Exchange rate.** Ch 49 keeps "about ₹530 at ₹83 to the dollar", and Ch 51's cost is shown at both ₹83 and ₹88.
   Ch 65 implies ₹87. Which book rate should be used (fact sheet C8)?
3. **Ch 45: Green Leaf Hotels** (a key account from Ch 12–13) replaces "Hotel Sai Palace", which appears nowhere
   else. OK?
4. **Ch 51: customer 24 (Prime Wholesale) starts with no CRM account**, so §51.4 can create it and teach upserts. OK?

## Tools and versions

5. **psycopg2 or psycopg 3?** Ch 18 installs psycopg 3. Ch 45–47 and 51 use psycopg2 as finding 45.2 asked, so the
   reader installs a second driver; the text says why in one line. Keep psycopg2, or move Part 5 to psycopg 3? That
   change is small but touches four companion folders.
6. **One Python version for Part 5?** Ch 46 ran on Python 3.14.7, the book's version. Ch 45's tool note says 3.11.15.
   The outputs don't depend on the version.
7. **Ch 46: Airflow.** The DAG is marked "not executed in the book", but it was run with Airflow 3.3.2 while the
   chapter was being fixed, and the text says so. Keep that sentence?
8. **Ch 48: timings** come from the book's shared 4-core build machine, with each engine given 2 cores. Keep them,
   or re-time on a named laptop before print?
   - The reader's code uses Spark `local[2]` rather than `local[*]`.
   - One `explain()` cell shortens file paths so the plan prints the same on every machine; Windows readers see a
     slightly different path, and the text says so.
9. **Ch 50: a real Kafka 4.3.1 broker** is now an optional part of §50.3, and its producer and consumer are run for
   real. The main thread still uses `mini_log.py`. Keep it optional?
10. **Ch 52: host networking.** Ch 46 hard-codes the practice API at `127.0.0.1:8045`, so the container needs
    `--network host`. Should Ch 46 read the address from an environment variable (`CRM_API_BASE`)?

## Content choices

11. **Ch 47: dbt model contracts** are taught in §47.7, with a real failing `dbt run`, because Part 3 was already
    closed. Should Ch 32 §32.7 also get a short paragraph? The text is drafted in `questions-ch47` and can be pasted
    in.
12. **Ch 49: the five-format timing table.** Ch 2's 500,000-line test can't be reproduced, because the book has no
    such dataset. It was re-run on Ch 49's own sensor day (216,000 readings), which prints new numbers with the same
    pattern. OK, or generate a 500,000-line orders file?
13. **Ch 50, Figure 50.1:** the figure uses machines M-04/M-08 and M-07/M-21, because the real hash puts the
    finding's suggested M-03 and M-12 in the same partition. **RJ-S2-19:** run 3 really reads 1,506 rows, not the
    finding's 1,550. Both follow the real code.
14. **Ch 51: follow-up-due flag (option A).** The book has no payment data, so the chapter syncs an honest recency
    flag rather than an "overdue payment" flag. Or add a small payments table (option B)?
15. **Ch 51: Stripe facts** (keys may be removed after 24 hours; V4 UUIDs suggested) were checked through a web
    search, because docs.stripe.com is blocked here. Please confirm them, or the Stripe name can be dropped.
16. **Ch 52: split the chapter?** It is now 51 pages and 20–26 h. It was kept as one chapter, which the finding
    allows as a fallback.
17. **Ch 52:** is `flash-page`, a hypothetical internal web page, a good enough example for Deployment + Service? And
    does an EventBridge schedule pick up a new task-definition revision by itself? docs.aws.amazon.com is blocked
    here, so the text asks the reader to check.

## Screenshots (V12)

18. **Ch 46:** one screenshot of the Dagster asset graph (finding 46.3). There is no browser here. The steps are in
    `questions-ch46`: run `dagster dev -f riverstone_pipeline.py`, then open Assets → graph.

## Not done here, for later passes or other files

- **`review/sequence-map.md`** is read-only for me. Rows 45.31 and 48.5 ask for these additions:
  - Ch 45 → Ch 77/78;
  - Ch 48 keeps its own sensor dataset, separate from Ch 40's.
- **Ch 45 and Ch 46 name a `raw.dispatch` column differently:** Ch 45 uses `source_file`, Ch 46's module uses
  `file_day`. Ch 47 follows Ch 46. Both work, but the names could be unified.
- **Ch 51:** one edit to `reset_ch51.py` was refused by the permission check. The script is unchanged; never run it
  against a shared database server.
- **Glossary (Appendix A):** new key terms from Ch 52 and others are listed in the chapters' changelogs.
- **Hours (T12, final pass):** Part 5 is now 122–156 hours (was 100–132).
- **Verification environments** can be dropped after merge: private PostgreSQL clusters `16/ch45`, `ch46`, `ch47`
  and `ch51`; the Ch 47 tool venvs under `/var/lib/postgresql/`; Docker images from Ch 52.
