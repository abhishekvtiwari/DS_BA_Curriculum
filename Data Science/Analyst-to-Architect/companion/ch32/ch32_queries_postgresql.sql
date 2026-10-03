-- Chapter 32. Analytics Engineering with dbt
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch32-analytics-engineering-with-dbt.md


-- (The times, and the timings in brackets, will differ on your machine; so may the order of lines
-- that run at the same time.)

-- How to read it:

-- - "Found 8 models, 4 data tests, 1 snapshot, 5 sources": three staging models and five marts,
-- the four tests in sources.yml, and the snapshot. The 13 nodes (models, tests, snapshots) are
-- numbered "1 of 13" to "13 of 13". - START and OK lines come in pairs. With four threads, up to
-- four nodes run at once, which is why the numbers arrive out of order. fct_sales_line starts
-- last, because everything it refs had to finish first. Nobody told dbt that; it read the ref
-- calls. - The bracket says what the database reported: SELECT 326 means 326 rows went into the
-- table, and CREATE VIEW means a view was made (views hold no rows). - PASS=13: every node
-- succeeded. ERROR and SKIP count failures and the nodes skipped because of them.

-- dbt build is the command to learn. It runs models, tests, snapshots, and seeds together, in
-- dependency order, and stops a branch of the graph when something upstream fails, so a failed
-- test doesn't let bad data through to the models below it. dbt run builds without testing, and
-- dbt test tests without building; build is what you want on a schedule.

-- The result is a schema of tables you can query like any other, in DBeaver or psql:

-- <!-- db: riverstone_2025 -->

SELECT COUNT(*) AS fact_rows,
       ROUND(SUM(net_revenue)) AS net_revenue,
       COUNT(DISTINCT customer_key) AS customer_versions
FROM dbt_dev_marts.fct_sales_line;

/* The chapter shows:
    fact_rows | net_revenue | customer_versions
   -----------+-------------+-------------------
          326 |     4335471 |                23
   (1 row)
*/


-- 326 lines and ₹43,35,471: the same numbers Chapter 28's hand-built star schema produced, which
-- is the point. What changed is that the build order, the tests, and the documentation now come
-- from the code itself. The 23 customer versions are 23 customers with one version each (the 24th,
-- Home Plus, placed no orders in 2025), where Chapter 28's dimension has 27 rows for the same 24
-- customers.

SELECT d.quarter_label,
       c.segment,
       ROUND(SUM(f.net_revenue)) AS net_revenue
FROM dbt_dev_marts.fct_sales_line AS f
JOIN dbt_dev_marts.dim_date AS d ON d.date_key = f.date_key
JOIN dbt_dev_marts.dim_customer AS c ON c.customer_key = f.customer_key
GROUP BY d.quarter_label, c.segment
ORDER BY d.quarter_label, c.segment;

/* The chapter shows:
    quarter_label |   segment   | net_revenue
   ---------------+-------------+-------------
    2025-Q1       | Hospitality |      149040
    2025-Q1       | Retail      |      394328
    2025-Q1       | Wholesale   |      190944
    2025-Q2       | Hospitality |      252170
    2025-Q2       | Retail      |      198474
    2025-Q2       | Wholesale   |      275925
    2025-Q3       | Hospitality |      307278
    2025-Q3       | Retail      |      333973
    2025-Q3       | Wholesale   |      479039
    2025-Q4       | Hospitality |      435551
    2025-Q4       | Retail      |      562000
    2025-Q4       | Wholesale   |      756751
   (12 rows)
*/


-- The twelve cells add up to ₹43,35,473, two rupees more than the total, because each cell was
-- rounded on its own.

-- =============================================================================================
-- The totals match Chapter 28; the history doesn't
-- =============================================================================================

-- Chapter 28 rebuilt three customers' 2025 history from the ERP's audit log: Metro Mart moved from
-- Thane to Mumbai on 1 July, for instance, so its January to June orders belong to Thane. The
-- snapshot has no such log. It starts from today's values, and the dimension stretches each
-- customer's first version back to 1900, so every Metro Mart order shows as Mumbai. This query
-- puts the two builds side by side.

SELECT 'Chapter 28 star' AS built_by, c.city, ROUND(SUM(f.net_revenue)) AS net_revenue
FROM dw.fact_sales_line AS f
JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
WHERE c.customer_id = 5
GROUP BY c.city
UNION ALL
SELECT 'dbt project', c.city, ROUND(SUM(f.net_revenue))
FROM dbt_dev_marts.fct_sales_line AS f
JOIN dbt_dev_marts.dim_customer AS c ON c.customer_key = f.customer_key
WHERE c.customer_id = 5
GROUP BY c.city
ORDER BY built_by, city;

/* The chapter shows:
       built_by     |  city  | net_revenue
   -----------------+--------+-------------
    Chapter 28 star | Mumbai |      177258
    Chapter 28 star | Thane  |      152040
    dbt project     | Mumbai |      329298
   (3 rows)
*/


-- (Trimmed to the lines that matter; PGPASSWORD is still set from section 32.3, or psql would ask
-- for the password.)

-- INSERT 0 1: the snapshot closed Evergreen Mart's old version and added one new row. dim_customer
-- now has 25 rows, and the fact table still has 326 lines, because every 2025 order falls in the
-- first version. Evergreen Mart's versions:

-- <!-- db: riverstone_2025 -->

SELECT customer_id, customer_name, segment,
       valid_from::date AS valid_from, valid_to::date AS valid_to, is_current
FROM dbt_dev_marts.dim_customer
WHERE customer_id = 18
ORDER BY valid_from;

/* The chapter shows:
    customer_id | customer_name  |  segment  | valid_from |  valid_to  | is_current
   -------------+----------------+-----------+------------+------------+------------
             18 | Evergreen Mart | Retail    | 1900-01-01 | 2026-09-28 | f
             18 | Evergreen Mart | Wholesale | 2026-09-28 | 9999-12-31 | t
   (2 rows)
*/


-- (Trimmed: the full output has a START and a result line for each of the 37 nodes.)

-- The count checks out: 10 models (3 staging, 7 marts), 1 snapshot, and 26 tests (4 on sources, 8
-- on staging, 13 on marts, 1 singular) make 37 nodes.

-- =============================================================================================
-- Where dbt runs in production
-- =============================================================================================

-- dbt Core is a command-line tool: something has to run it on a schedule. The options, in rough
-- order of how much they cost you:

-- | Option | What it is | |---|---| | cron on a small server (Chapter 34) | the simplest thing
-- that works | | An orchestrator: Airflow, Dagster, Prefect (Chapter 46) | dbt as one task among
-- ingestion and downstream jobs | | A container on a cloud scheduler | no server to maintain | |
-- dbt Cloud | dbt Labs' hosted product: scheduling, a browser IDE, CI, hosted docs, on a paid plan
-- with a limited free tier |

-- The models, tests, and docs are identical either way. Check current dbt Cloud plans and prices
-- on dbt Labs' site; they change, and this chapter was written against dbt Core 1.12.

-- ---

-- =============================================================================================
-- 32.13 What dbt is not, and the semantic layer
-- =============================================================================================

-- dbt only transforms data that's already in the warehouse. It does not extract or load (that's
-- Fivetran, Airbyte, or your own Python, Chapter 46), does not schedule itself, is not a BI tool,
-- and is not a database. A dbt project on a warehouse that nothing loads is a rota for an empty
-- kitchen.

-- The one boundary that keeps moving is the semantic layer: the idea that metric definitions
-- (revenue, active customer, churn) should live in one place that every tool asks, rather than
-- being re-implemented in each dashboard. dbt has a semantic layer built on MetricFlow, where you
-- define metrics in YAML alongside models and BI tools query them through an API. Competing
-- approaches exist (Cube, Looker's LookML, and BI tools' own modeling layers), and this area
-- changes fast enough that any specific instruction here would be stale by the time you read it.

-- The idea, though, is stable, and you already have it: Riverstone's net_revenue macro is a one-
-- metric semantic layer. If a metric's definition lives in one file, is tested, and everything
-- downstream refs it, you have most of the benefit. If it lives in six dashboards, no product will
-- save you. Check dbt's documentation for the current state of the semantic layer before adopting
-- it, and Chapter 16 for how BI tools consume a mart.

-- --- ## Common mistakes

-- | Mistake | Symptom | Fix | |---|---|---| | Hard-coded table names instead of ref | Models build
-- in the wrong order; the lineage graph is wrong | {{ ref(...) }} and {{ source(...) }}, always |
-- | database: pinned in sources.yml | Works in dev, fails in every other environment | Let the
-- target decide the database | | Credentials in profiles.yml in Git | A warehouse password in the
-- repository forever | Environment variables or a secrets manager | | Models that duplicate a
-- business rule | Two dashboards, two revenue numbers | One macro, refed everywhere | | Joins in
-- staging that change the grain | Row counts inflate downstream and nobody knows where | Keep
-- staging one-row-per-source-row; join in marts | | No tests on the grain | Duplicate keys reach
-- the fact table | unique and not_null on every model's key | | Tests only on shapes, never on
-- numbers | Everything passes while the total is wrong | A reconciliation test against the source
-- | | dbt run on a schedule instead of dbt build | Bad data ships because tests ran after, or not
-- at all | dbt build, which stops the branch on failure | | Ignoring a failing test for a few days
-- | The test gets deleted, and the trust with it | Fix or explicitly change the rule, in a
-- reviewed pull request | | Everything materialized as a table | Slow builds, warehouse bills |
-- Views for staging, tables for marts, incremental for the big ones | | Incremental models never
-- fully refreshed | Old rows built by old logic | Scheduled --full-refresh, and after any logic
-- change | | An incremental filter with no lookback | Late-arriving rows never appear | A few days
-- of overlap plus delete+insert on a unique key | | Snapshot pointed at a changing source path |
-- History silently lost | Treat snapshot tables as irreplaceable | | Documentation written in a
-- wiki | Stale within a month | Descriptions in the YAML beside the model | | Jinja loops
-- generating clever SQL | Nobody can debug it, including you in March | Write the SQL out; save
-- Jinja for repetition that is truly mechanical | | No CI | Broken models found in production |
-- Build and test on every pull request | | One enormous mart model | Impossible to test or review
-- | Split into intermediate models; views are free |

-- ---

-- =============================================================================================
-- In the real world: the two dashboards that disagreed
-- =============================================================================================

-- Anita's dashboard says December revenue was ₹4,39,824. The finance pack says ₹4,47,000. The gap
-- is ₹7,176 and nobody can explain it, so both numbers stop being used and the argument is settled
-- by whoever speaks last in the meeting.

-- Meera spends a morning on it. The dashboard reads Chapter 13's sales_lines view, which excludes
-- cancelled orders. The finance pack reads a spreadsheet built from a different export, which
-- includes them. Neither is wrong: they are answers to different questions, and nobody wrote
-- either question down.

-- The fix isn't a better argument, it's a place for the answer to live. Over two weeks she builds
-- the dbt project in this chapter:

-- - net_revenue becomes a macro. One definition, used by staging and by the reconciliation test. -
-- fct_sales_line states its grain in its description: one non-cancelled order line. Cancelled
-- orders keep their own model, so the finance question has an answer too, and the two differ by a
-- number anyone can query. - The reconciliation test compares the fact total to the source on
-- every build, so drift is caught the morning it appears, not in a meeting. - The lineage graph
-- shows the dashboard reading fct_sales_line, and fct_sales_line reading stg_order_items, and that
-- reading the ERP's order_items. The chain is on a page. - Everything runs in CI on every pull
-- request, so changing the revenue rule is a reviewed decision with a name and a date attached.

-- Three months later the ERP team renames a column in order_items. The nightly build fails at
-- 03:14 with a clear message, one staging model is changed and reviewed the next morning, and
-- nothing downstream needed touching. Before dbt, that rename would have surfaced as a blank
-- dashboard tile at 9 a.m., traced by hand over a day.

-- What Meera tells Anita: "The two numbers were answering different questions, and now both
-- questions have a model with its definition written down. The dashboard will keep matching
-- finance, because a test checks it every night and the build fails if it stops."

-- Notice that dbt didn't settle the argument. Writing the definition down did. dbt made writing it
-- down the cheapest option, and kept it honest afterwards.

-- ---

-- =============================================================================================
-- Project: a tested mart that feeds a dashboard
-- =============================================================================================

-- Goal: a dbt project someone else could clone, build, and trust, ending in a mart a BI tool
-- reads.

-- =============================================================================================
-- Tools you'll need
-- =============================================================================================

-- Versions used for this chapter, checked in September 2026:

-- - dbt Core 1.12.5 with dbt-postgres 1.11.0, installed with uv add dbt-core dbt-postgres. dbt
-- releases often: check dbt --version against the documentation, and re-read the release notes
-- before upgrading a project. - PostgreSQL 16, holding riverstone_2025 and riverstone_perf. -
-- SQLFluff 4.3.0 with sqlfluff-templater-dbt (the templater is a separate package, and forgetting
-- it produces a confusing error). - Git (Chapter 26) and a CI service; the example is GitHub
-- Actions. - Adapters for other warehouses: dbt-snowflake, dbt-bigquery, dbt-databricks, dbt-
-- redshift, dbt-duckdb, dbt-sqlserver. The project changes very little between them; the SQL
-- dialect does. - Packages worth knowing: dbt_utils (macros and extra tests), dbt_expectations (a
-- larger test catalog), codegen (generates boilerplate YAML from your warehouse), elementary
-- (observability, Chapter 47). - Python 3.14, which uv picked for the analytics environment
-- (Chapter 17's recommendation). - Companion files in ch32/: the complete riverstone_dbt project,
-- including its CI workflow and .sqlfluff; setup_raw_crm.sql (section 32.3); and pyproject.toml
-- with requirements-pinned.txt, the exact versions every output in this chapter came from.

-- Option A: your own warehouse. Pick one report that matters and rebuild its inputs as a dbt
-- project. Work against a development schema, never production, and keep credentials in
-- environment variables.

-- Option B: Riverstone. Build the project in this chapter from an empty folder, without copying
-- the companion files, then compare.

-- Steps:

-- 1. Set it up: dbt init, a profiles.yml reading secrets from the environment, dbt debug passing,
-- and the whole thing in Git with target/ and .env ignored. 2. Declare your sources, with unique
-- and not_null on their keys, and dbt source freshness configured for at least one. 3. Build
-- staging models, one per source table, materialized as views. 4. Build the marts: at least one
-- fact table with a grain stated in its description, and two dimensions. 5. Test it: grain tests
-- on every model, relationships on every key in the fact table, accepted_values on one category,
-- and one reconciliation test against the source. 6. Break something on purpose and confirm the
-- build fails and the message tells you where. 7. Add a macro for one business rule, and use it in
-- at least two places. 8. Add a snapshot for a dimension that changes, and prove it captures a
-- change. 9. Make one model incremental and time a full refresh against an incremental run. 10.
-- Document it: descriptions for every model and for columns whose meaning isn't obvious. Generate
-- the docs and read your own lineage graph. 11. Add CI that lints and builds on every pull
-- request, and open one pull request that fails on purpose. 12. Point a BI tool at the mart
-- (Chapter 16) and confirm the numbers match your reconciliation.

-- Deliverables: the repository, the docs site (a screenshot of the lineage graph is fine), the
-- output of a passing dbt build and of a failing one, and a half-page note on which tests you
-- chose and why.

-- Stretch goals:

-- - Add dbt_utils and replace one hand-written test with expression_is_true or equal_rowcount. -
-- Add a second target and prove the same models build against both. - Convert the fact table to
-- incremental with a three-day lookback, and write a test that compares it with a full
-- recomputation. - Add dbt build --select state:modified+ to CI so only changed models rebuild.

-- ---

-- =============================================================================================
-- Recap
-- =============================================================================================

-- - Analytics engineering brings software habits (version control, tests, review, documentation)
-- to SQL transformation. ELT put that transformation inside the warehouse, and dbt is the tool
-- most teams use for it. - A model is one SELECT in a file. source declares raw tables; ref
-- connects models, resolves names per environment, and builds the dependency graph dbt runs in
-- order. - Projects layer into staging (one model per source table, views, grain preserved),
-- optional intermediate, and marts (facts and dimensions, tables). - Materializations: view,
-- table, incremental, ephemeral. Views for staging, tables for marts, incremental when a rebuild
-- hurts. - Tests return no rows when they pass. unique, not_null, relationships, and
-- accepted_values cover shapes; a singular test reconciling to the source covers the numbers. dbt
-- build runs models and tests together and stops the branch when one fails. - Documentation and
-- the lineage graph are generated from the YAML and the ref calls, so they can't drift. -
-- Snapshots keep type 2 history from a source that overwrites, but only from the day they start
-- running. - Incremental models process new rows only: 2.19 seconds against 0.55 on 1.9 million
-- lines here. Use a lookback window, a unique key, and a scheduled full refresh. - Jinja turns
-- dbt's files into templates: {{ }} for values, {% %} for instructions, {# #} for comments. Macros
-- define a business rule once. Packages such as dbt_utils bring proven macros and tests. -
-- SQLFluff lints; CI builds and tests every pull request; something else (cron, an orchestrator,
-- or dbt Cloud) runs dbt on a schedule. - dbt transforms; it does not extract, load, schedule, or
-- visualize.

-- ---

-- =============================================================================================
-- Key terms
-- =============================================================================================

-- analytics engineering · ETL · ELT · dbt Core · dbt Cloud · adapter · profile · target ·
-- dbt_project.yml · profiles.yml · env_var · model · source · ref · source() · config() · Jinja ·
-- compiled SQL · DAG (dependency graph) · staging layer · intermediate layer · mart ·
-- materialization · view · table · incremental model · ephemeral model · is_incremental() · {{
-- this }} · incremental strategy · lookback window · full refresh · generic test · singular test ·
-- unique · not_null · relationships · accepted_values · source freshness · dbt build · dbt run ·
-- dbt test · node selection (+, state:modified) · snapshot · dbt_valid_from · dbt_valid_to ·
-- dbt_scd_id · check strategy · timestamp strategy · macro · package · dbt_utils · docs site ·
-- lineage graph · SQLFluff · templater · linting · continuous integration · service container ·
-- repository secret · semantic layer · MetricFlow

-- (All terms are defined in the Glossary, Appendix A.)

-- ---

-- =============================================================================================
-- Check yourself
-- =============================================================================================

-- - [ ] I can explain ELT, and why transformation moved into the warehouse. - [ ] I can set up a
-- dbt project whose credentials never appear in the code. - [ ] Every model of mine uses ref and
-- source, and I can explain both jobs ref does. - [ ] I lay projects out in staging and marts, and
-- I keep the grain in staging. - [ ] I choose materializations deliberately and can say what each
-- costs. - [ ] My models carry grain tests, relationship tests, and at least one reconciliation. -
-- [ ] I run dbt build, not dbt run, on a schedule, and I know why. - [ ] I can read a failing
-- test's output and get to the offending rows. - [ ] I write descriptions beside the models and
-- can navigate my own lineage graph. - [ ] I can keep type 2 history with a snapshot, and I know
-- what a snapshot can't recover. - [ ] I can make a model incremental, with a lookback, and
-- measure what it saves. - [ ] I write a business rule once, as a macro, and lint and build on
-- every pull request.

-- ---

-- =============================================================================================
-- Exercises
-- =============================================================================================

-- Work in the riverstone_dbt project, against the dev target. Predict each answer before you run
-- it.

-- =============================================================================================
-- Warm-up
-- =============================================================================================

-- 1. Run dbt ls and dbt ls --select staging. What do the outputs tell you about how models are
-- addressed? 2. Compile fct_sales_line and read target/compiled/.../fct_sales_line.sql. Which
-- parts were written by you, and which by dbt? 3. Run dbt build --select stg_orders+ and explain,
-- from the output, what the + did. 4. Query dbt_dev_marts.fct_daily_sales. How many rows does it
-- have, and why that number?

-- =============================================================================================
-- Core
-- =============================================================================================

-- 5. Add a stg_employees staging model, with unique and not_null tests on employee_id, and change
-- dim_sales_rep to ref it instead of the source. Does the lineage graph change? 6. Add an
-- accepted_values test on stg_orders.status, run it, then add a new status to the source data and
-- watch it fail. 7. Write a singular test asserting that no order line has a negative net_revenue,
-- and one asserting that every non-cancelled order in stg_orders has at least one line in
-- fct_sales_line. 8. Change the net_revenue macro to round to zero decimal places. Which models
-- change, and which test catches the consequence? 9. Materialize dim_date as a view instead of a
-- table, rebuild, and compare the run output. When would that be the right choice? 10. Add
-- descriptions for every column of fct_sales_line, regenerate the docs, and check the column-level
-- lineage.

-- =============================================================================================
-- Stretch
-- =============================================================================================

-- 11. Write a model int_orders_with_totals as an ephemeral materialization, use it in
-- fct_daily_sales, and look at the compiled SQL. Where did the model go? 12. Convert
-- fct_sales_line to incremental, keyed on order_item_id, with a three-day lookback on order_date.
-- Then write a test that compares its total against a full recomputation. 13. Add dbt_utils to the
-- project and replace the reconciliation test with dbt_utils.equal_rowcount plus an expression
-- test. Which version would you rather maintain? 14. Section 32.11's mart_sales_monthly pivots
-- revenue by category with a Jinja loop. Write the same model without Jinja, as
-- mart_sales_monthly_plain, and compare the two compiled files. Which would you put in the
-- repository? 15. Configure dbt source freshness on erp.orders with a warn-after of 24 hours and
-- an error-after of 48, and make it fail.

-- =============================================================================================
-- Think about it (no code needed)
-- =============================================================================================

-- 16. A colleague wants the dashboard to read stg_order_items directly, "because it has everything
-- and it's fresher". Give two reasons to say no, and one case where they'd be right. 17. Your
-- project has 300 models and dbt build takes 40 minutes. List four things you'd look at, in order.
-- 18. When would you not use dbt for a transformation?

-- ---

-- =============================================================================================
-- Answers
-- =============================================================================================

-- 1. dbt ls lists every node in the project: sources, models, snapshots, and tests, one per line:
-- models as project.folder.name (riverstone_dbt.staging.stg_orders), sources as
-- source:riverstone_dbt.erp.orders. dbt ls --select staging lists only what's under
-- models/staging. That naming is how node selection works everywhere: --select stg_orders (one
-- model), stg_orders+ (it and everything downstream), +fct_sales_line (it and everything
-- upstream), tag:nightly, source:erp+, state:modified+. Selection is the skill that makes a
-- 300-model project workable.

-- 2. Everything between select and the final from is yours. dbt replaced {{ source('erp',
-- 'order_items') }} with the fully qualified table name, and expanded the net_revenue macro into
-- arithmetic. Nothing else was added. The compiled file is your query exactly as the database will
-- run it; when the model is built, dbt wraps it in create table ... as and saves that version in
-- target/run/, which is why reading it settles most "why is this model doing that?" questions.

-- 3. The + selects the model and everything downstream of it: stg_orders, then the marts that ref
-- it, then the tests on all of them. The output shows the fact models and their tests running
-- after the staging view. Use it before opening a pull request: it proves that a change to one
-- model doesn't break anything below it. +stg_orders (the plus in front) would select its upstream
-- instead, which is what you want when a source is misbehaving.

-- 4.

-- <!-- db: riverstone_2025 -->

SELECT COUNT(*) AS days,
       MIN(order_date) AS first_day,
       MAX(order_date) AS last_day,
       ROUND(SUM(net_revenue)) AS net_revenue
FROM dbt_dev_marts.fct_daily_sales;

/* The chapter shows:
    days | first_day  |  last_day  | net_revenue
   ------+------------+------------+-------------
     132 | 2025-01-02 | 2025-12-23 |     4335471
   (1 row)
*/

