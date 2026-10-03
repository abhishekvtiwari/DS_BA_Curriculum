-- Chapter 47. Data Quality, Observability & Contracts
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch47-data-quality-observability-and-contracts.md


-- The hash comparison found the one changed order and set its status back to the ERP's value.

-- ---

-- =============================================================================================
-- Common mistakes
-- =============================================================================================

-- | Mistake | Symptom | Fix | |---|---|---| | Testing only that the pipeline ran | Green runs,
-- wrong numbers | Test the data, not only the job (47.2) | | Publishing first and checking after |
-- Wrong rows visible while you investigate | Write–audit–publish (47.4) | | Every test an error |
-- Pipelines blocked by trivia; people disable tests | Severity per test; warnings for edges (47.2)
-- | | Tests that have never failed | False confidence | Break things on purpose and watch them
-- fail (47.3) | | No freshness monitoring | Dashboards quietly show last week | Monitor age of
-- newest data per table (47.5) | | Baselines learned from broken days | "Normal" drifts toward
-- broken | Exclude failed days; use medians over longer windows | | Treating unusual as wrong |
-- Blocked pipelines on genuine big sales days | Anomalies warn; only hard rules block (47.5) | | A
-- missing day that looks like a zero day | Charts show a dip that never happened | Publish load
-- status alongside data (47.4) | | No lineage | "Is anything else affected?" takes hours | Declare
-- dependencies; use the orchestrator graph (47.6) | | Contracts as documents nobody checks | Same
-- breakage every quarter | Check the contract in the pipeline (47.7) | | Blaming the source's
-- owner | Cooperation stops; surprises continue | Make the safe path the obvious one; explain
-- impact in their terms | | Fixing without telling users | People act on numbers they didn't know
-- were wrong | Communicate at containment, before the fix (47.8) | | Skipping the review | The
-- same incident twice | Ten-minute blameless write-up, kept with the runbook | | One alert per
-- failed signal | Five messages for one problem; fatigue | Group by incident; route by owner
-- (47.9) | | Alerting on everything | The channel becomes noise | Alert only what someone will act
-- on; review monthly |

-- ---

-- =============================================================================================
-- In the real world: the dashboard that was right but late
-- =============================================================================================

-- Riverstone's sales dashboard had been correct for months, so when Vikram opened it on a Thursday
-- to prepare for a customer call, he didn't check the date on it. He told the customer their last
-- order had been in November.

-- It had been in January. The dashboard was showing data that stopped on 4 January, four days
-- earlier.

-- Meera traced it in twenty minutes. On the Monday, a change in the warehouse had renamed a column
-- in the staging model. The nightly pipeline's transformation step had failed at 2:10 a.m. That
-- failure had sent an alert, exactly as designed, into the data team's channel, where it sat among
-- the eleven other messages the pipeline sent every night: three warnings about dispatch rows with
-- unknown orders, a note about API retries, a long "run finished" message, and a nightly summary
-- nobody read. The failure was message seven.

-- Meanwhile, every test that ran was green, because the tests all ran against tables that had
-- stopped being updated. Their data was perfectly consistent, and three days old.

-- The fixes were small, and they're the ones in this chapter.

-- - Freshness checks on the tables people read, not only tests on their contents. The dashboard's
-- own table now fails a check if its newest day is older than the previous working day. - Fewer
-- alerts, better routed. Successes stopped being announced. Warnings moved to a weekly digest.
-- Failures went to the on-call person with a subject line naming the table and the impact. - A
-- status banner on the dashboard, driven by the load status table: "Data current to 7 January,
-- 6:35 a.m." Vikram's habit of glancing at the top-right corner now catches in one second what
-- took three days. - A contract conversation with the analytics engineer who had renamed the
-- column, agreeing that renames in shared models need a note and a deprecation window, exactly as
-- for external sources.

-- At the next sales review, Anita asked whether the data was reliable now. "It fails more often
-- than it used to," Meera said. "That's the point. When it's wrong, it stops and tells us, instead
-- of looking right."

-- What made this work.

-- - They monitored freshness, not only correctness. The data was correct; that was never the
-- problem. - They treated alert noise as a real defect, because it's what hid the failure. - They
-- put the status where the users look, so trust didn't depend on the data team noticing first. -
-- They applied contracts internally, where most surprise changes actually come from.

-- ---

-- =============================================================================================
-- Project: quality, monitoring, and a contract for the Riverstone pipeline
-- =============================================================================================

-- Goal: make the Chapter 46 pipeline trustworthy: nothing wrong gets published, staleness is
-- noticed, one incident produces one useful alert, and the dispatch file has a contract that's
-- checked automatically.

-- =============================================================================================
-- Tools you'll need
-- =============================================================================================

-- - Python 3.14 in the virtual environment from Chapter 17, with duckdb and psycopg2 (Chapter 45,
-- section 45.2); PostgreSQL 16; Jupyter; the Chapter 47 companion folder (companion/ch47/), which
-- is Chapter 46's environment without Dagster, plus reset_ch47.py and the two Soda files. Open
-- your notebook in that folder. - No data quality product needed: every test in the main thread is
-- SQL run from Python. - Optional: great_expectations and soda-duckdb (section 47.10), and your
-- Chapter 32 dbt project for the dbt tests and the model contract. - Versions used for the outputs
-- shown: Python 3.11.15, DuckDB 1.5.6, psycopg2 2.9.13, PostgreSQL 16.13, Great Expectations
-- 1.23.2, Soda Core 4.25.0, dbt Core 1.12.5 with dbt-postgres 1.11.0 and dbt_utils 1.4.1, on 29
-- September 2026. Your Python 3.14 environment gives the same outputs.

-- Option A: Riverstone. Extend your Chapter 46 pipeline.

-- Option B: your own pipeline. Apply the same layers to a report you produce, using data you're
-- allowed to use.

-- Steps

-- 1. Write the specification for two tables: what "good" means, in sentences, for at least four
-- dimensions from section 47.1. 2. Build a test suite of at least ten tests across raw, staging,
-- and mart, each with a severity and a one-line description. 3. Break each rule on purpose and
-- confirm every test fails when it should. Note any test that didn't catch what you expected. 4.
-- Convert the pipeline to write–audit–publish for the Flash, and prove a failing day leaves the
-- published table untouched. 5. Add freshness checks for every table people read, with limits
-- based on the promise to users, and a load_status table the dashboard can show. 6. Add two volume
-- checks: zero rows on a working day (error), and a wide band around the median of recent days
-- (warning). 7. Add lineage: list, for each source, which outputs it affects, and use it in your
-- alert text. 8. Write a data contract for the dispatch file with the warehouse team's view in
-- mind, and check it in the pipeline. 9. Run an incident: break the pipeline, produce one grouped
-- alert, write the user-facing message, fix, re-run, and write the review (half a page). 10. Count
-- your alerts. Over a week of runs, how many messages would a person receive? If it's more than a
-- handful, cut them.

-- Stretch goals

-- - Store every test result in a test_results table with the run and day, and chart pass rates
-- over time. - Add a check that compares this week's revenue by segment with last week's and warns
-- on large shifts. - Write the same tests as dbt tests and run both, comparing effort and output.

-- ---

-- =============================================================================================
-- Recap
-- =============================================================================================

-- - Data quality has dimensions: accuracy, completeness, validity, uniqueness, consistency, and
-- timeliness. Each becomes a test. - A data test is a query that returns the rows that break a
-- rule; zero rows means it passed. dbt's tests compile to exactly these queries; Great
-- Expectations and Soda report the same rule as a measurement, a count of the values that break
-- it. - Severity decides what stops a pipeline. Warnings are for edges; errors are for numbers
-- people act on. Tests nobody acts on should be fixed, downgraded, or deleted. - Tests belong at
-- every layer: structure in raw, validity and consistency in staging, business rules and
-- reconciliation in mart, and blocking checks before delivery. - Break your tests on purpose. A
-- suite that has never failed hasn't been tested. - Write–audit–publish keeps failed data out of
-- the tables people read; the same 5 January failure that left a wrong row in Chapter 46 now
-- leaves the published table untouched. - Observability answers three questions: did it run, is it
-- fresh, does its volume look normal. Stale data is one of the most common incidents, and the
-- least noticed. Freshness is judged against the promise to users, such as "yesterday's working
-- day is loaded by 6:30", not a fixed number of hours. - Unusual is not wrong. Anomalies warn;
-- only hard rules block. - Lineage tells you what a broken table affects, and where a wrong number
-- could come from. - Data contracts state fields, rules, delivery, change notice, and what happens
-- on a breach, and are checked in the pipeline: columns and values. They apply to internal
-- producers too, where dbt's model contracts enforce them. - Incidents follow detect, classify,
-- contain, fix and verify, review. Tell users at containment, before the fix. - Alert fatigue
-- hides real failures: one incident, one alert; route by owner; alert only what someone will act
-- on.

-- ---

-- =============================================================================================
-- Key terms
-- =============================================================================================

-- data quality dimensions (accuracy, completeness, validity, uniqueness, consistency, timeliness)
-- · data test · failing rows · severity (error, warning) · raw, staging, mart layers ·
-- reconciliation · anti-join · foreign key · self-healing load · dbt test · singular test ·
-- write–audit–publish (WAP) · audit schema · cross join · floating-point comparison · publish swap
-- · blue/green tables · load status · observability · freshness · previous working day · staleness
-- limit · volume check · baseline · median · anomaly · lineage · column-level lineage · impact
-- analysis · data contract · model contract · change notice · breach · data incident · severity
-- levels (S1, S2, S3) · containment · blameless review · alert fatigue · alert grouping · runbook
-- · expectation (Great Expectations) · check (Soda)

-- (All terms are defined in the Glossary, Appendix A.)

-- ---

-- =============================================================================================
-- Check yourself
-- =============================================================================================

-- - [ ] You can name the six data quality dimensions and write a test for each on Riverstone data.
-- - [ ] You can explain why a data test is "a query that returns the rows that break the rule". -
-- [ ] You can choose error or warning severity for a test, and defend the choice. - [ ] You can
-- say which checks belong in raw, staging, mart, and before delivery. - [ ] You can break a rule
-- on purpose and show the test catching it. - [ ] You can implement write–audit–publish and prove
-- readers never see failed data. - [ ] You can explain why a re-run repairs a table loaded by hash
-- comparison. - [ ] You can set freshness limits from a promise to users, and explain why stale
-- data is the hardest failure to notice. - [ ] You can build a volume baseline with a median, and
-- explain why unusual is not the same as wrong. - [ ] You can use lineage to say who is affected
-- by a broken table. - [ ] You can write a data contract and check it automatically. - [ ] You can
-- classify an incident's severity, write the user-facing message, and run the review. - [ ] You
-- can group one incident into one alert and explain three rules that prevent alert fatigue. - [ ]
-- You can write the same rule as a dbt test, a Great Expectations expectation, and a Soda check,
-- and say how their results differ. - [ ] You can recommend a starting set of tools for a small
-- data team.

-- ---

-- =============================================================================================
-- Exercises
-- =============================================================================================

-- Run reset() and re-run the setup and test blocks before each exercise that uses the companion
-- environment.

-- =============================================================================================
-- Warm-up
-- =============================================================================================

-- 1. Name the data quality dimension each rule belongs to: (a) every order line points at an order
-- that exists; (b) status is one of four values; (c) yesterday's orders are loaded by 6:30 a.m.;
-- (d) the warehouse's revenue for a day equals the ERP's; (e) one row per order. 2. Write the
-- failing-rows query for: (a) duplicate dispatch_id values in raw.dispatch; (b) orders with a
-- sales_rep_id that doesn't exist in a raw.employees table. 3. For each, choose error or warning
-- and give a reason: (a) revenue doesn't match the ERP; (b) a dispatch row points at an unknown
-- order; (c) a customer's email is missing; (d) mart.daily_flash has two rows for one day.

-- =============================================================================================
-- Core
-- =============================================================================================

-- 4. Add a test flash_revenue_matches_lines that fails when a published Flash row's revenue
-- doesn't equal the revenue recomputed from raw.orders and raw.order_items for that day. Would
-- this have caught the 5 January failure? Would it have caught a wrong discount in the source? 5.
-- In section 47.3 the ERP refused the orphan order line, and the warehouse accepted it. Explain
-- why, and say what you'd add to the warehouse to make it refuse too. What's the trade-off of
-- adding it? 6. After the resync block, all seven tests pass again. Explain, in terms of Chapter
-- 45's hash comparison, why re-running the load repaired the warehouse. Which of the three broken
-- things would a load with an ID watermark have repaired? 7. The freshness check flagged
-- mart.daily_flash as stale at 6:30 a.m. on 6 January. Write the user-facing message the sales
-- team should receive, in three sentences. 8. Set freshness limits for: (a) raw.orders; (b)
-- raw.dispatch; (c) raw.crm_leads, given the Flash is promised by 7:30 a.m. IST on working days,
-- the dispatch file is due at 20:00 IST daily, and lead figures are used in a Monday report. State
-- your assumption about weekends. 9. Using the 2025 numbers in section 47.5 (median ₹27,442.50,
-- 131 days with orders), design two volume rules: one error and one warning. Say what each would
-- have done on 16 November 2025 (₹175,895.00) and on a day the load brought in nothing.

-- =============================================================================================
-- Stretch
-- =============================================================================================

-- 10. Design the load_status table mentioned in section 47.4: columns, one row per what, and how a
-- dashboard would use it to show "data current to…". Include how it distinguishes "not published
-- yet", "published", and "failed". 11. Write the full dispatch data contract as a document the
-- warehouse supervisor would accept: fields, rules, delivery, change process, breach handling,
-- review. Then list the three checks you'd automate first, and why those three. 12. An analytics
-- engineer renames a column in a shared staging model, breaking two downstream reports. Design an
-- internal contract process for shared models: what's promised, how changes are announced, how
-- long the old name survives, and how the pipeline enforces it.

-- =============================================================================================
-- Think about it (no code needed)
-- =============================================================================================

-- 13. Riverstone's pipeline now fails more often than it used to, because it stops when data is
-- wrong. Write the paragraph you'd use to explain to Anita why that's an improvement, and what
-- you'd show her each month to prove it. 14. Which is worse: a wrong number delivered on time, or
-- no number at all? Argue both sides using examples from this chapter, then say what design choice
-- follows from your answer.

-- ---

-- =============================================================================================
-- Answers
-- =============================================================================================

-- 1. (a) Consistency (a relationship between tables). (b) Validity. (c) Timeliness. (d) Accuracy.
-- (e) Uniqueness. Completeness would cover "every order has a customer".

-- 2. Sample answers:

-- (a) duplicate dispatch_id
SELECT dispatch_id, COUNT(*) AS n
FROM raw.dispatch
GROUP BY dispatch_id
HAVING COUNT(*) > 1;

-- (b) orders whose sales rep is unknown
SELECT o.order_id, o.sales_rep_id
FROM raw.orders AS o
LEFT JOIN raw.employees AS e ON e.employee_id = o.sales_rep_id
WHERE o.sales_rep_id IS NOT NULL AND e.employee_id IS NULL;

