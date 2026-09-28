# Chapter 32. Analytics Engineering with dbt

*Part 3 — Advanced Analytics & Analytics Engineering*

> **Chapter at a glance**
>
> **You will learn to:** explain what analytics engineering is and where dbt fits · set up a dbt project against a real database, with credentials kept out of the code · turn SQL you already write into models, sources, and `ref` calls that dbt orders for you · lay a project out in staging, intermediate, and marts layers · choose materializations, and know what each one costs · write tests that fail loudly when a business rule breaks, including a reconciliation test · generate documentation and lineage nobody has to maintain by hand · keep type 2 history with snapshots · make a large model incremental and measure what it saves · write a macro so a business rule exists once · lint SQL and run the whole project on every pull request.
>
> **Before you start:** Chapters 12 and 13 (SQL, the `sales_lines` view and its net-revenue rule), Chapter 28 (star schemas, grain, slowly changing dimensions, and its additions to `riverstone_2025`), Chapter 17 (virtual environments), Chapter 29 (`uv` in section 29.4, settings in environment variables, exit codes), Chapter 26 (Git, pull requests, the automated check and its YAML file), Chapter 34 (the command line, environment variables, running scripts, ports), and Chapter 16 (connecting Power BI to PostgreSQL, used in the project).
>
> **Time needed:** 18–22 hours, spread over three weeks, in four sittings: sections 32.1–32.5 (setup, sources, staging, marts, the first build: 5–6 hours); sections 32.6–32.9 (materializations, tests, docs, snapshots: 4–5 hours); sections 32.10–32.13 (incremental models, macros, linting, CI: 4–5 hours); and the project (5–6 hours).
>
> **Tools:** dbt Core 1.12 with the Postgres adapter, PostgreSQL 16, Git, and SQLFluff. Everything runs locally; no dbt Cloud account is needed. This chapter uses PostgreSQL only: dbt reaches MySQL only through a community adapter (`dbt-mysql`, at version 1.7.0 on PyPI in September 2026, well behind dbt Core), so the examples don't use it.
>
> **Practice data:** the `riverstone_2025` database from Chapter 13, with Chapter 28's additions, plus `riverstone_perf` from Chapter 28 for the incremental example. The finished project is in the companion folder as `ch32/riverstone_dbt`, and the chapter builds it from nothing.

---

## Why this matters

Chapter 28 built Riverstone a star schema. It works, and it has four problems that every hand-built warehouse has:

- **Nobody knows the order.** The build script has to run the dimensions before the fact table. That order lives in a file somebody wrote once and in the head of whoever wrote it.
- **Nothing checks it.** If tomorrow's load drops half the customers, the fact table shrinks and the dashboard is quietly wrong.
- **Nobody knows what depends on what.** Change `sales_lines` and you find out what breaks when someone complains.
- **There's no history of changes.** Who changed the revenue rule in March, and why?

Chapter 29 solved exactly these problems for Python: structure, tests, review, version control. **Analytics engineering** is the same answer for SQL, and **dbt** is the tool most teams use to do it. You write `SELECT` statements; dbt works out the dependency order, builds the tables and views, runs the tests, writes the documentation, and does it all from version control with a command that a schedule can run at 3 a.m.

It is also, right now, the job title that sits between analyst and data engineer, and the skill that most often turns "senior analyst" into "analytics engineer" with the salary that comes with it (Chapter 8). Interviewers ask about it directly: *"what does `ref` do?"*, *"what's the difference between a table and an incremental model?"*, *"how would you test that a load is complete?"*

---

## In plain English

**dbt is a kitchen rota for your SQL.**

You have thirty dishes to prepare, and some need others finished first: the sauce before the pasta, the stock before the sauce. Writing the order down by hand works until a new dish arrives, and then somebody serves pasta with no sauce.

dbt asks you to write each dish's recipe on its own card, and to say which other cards it uses, by name. From those names it works out the order itself. Add a dish and the rota updates. Change the stock and dbt knows every dish that needs remaking.

Three more things come with the cards:

- **Tasting notes**: rules each dish must satisfy before it leaves the kitchen (no duplicate order ids, no missing revenue, the total matches the source). If a rule fails, the pass stops and somebody is told.
- **A menu**: documentation and a diagram of what feeds what, generated from the same cards, so it can't drift from reality.
- **A logbook**: the cards live in Git, so every change was reviewed, dated, and attributed.

What dbt does *not* do is move data into the warehouse, or run itself on a schedule. It only transforms what's already there (Chapter 46 handles the moving and the scheduling).

---

## 32.1 What analytics engineering is

| | Data engineer | **Analytics engineer** | Data analyst |
|---|---|---|---|
| Works on | pipelines, infrastructure, ingestion | transforming raw tables into trusted models | questions, analysis, dashboards |
| Main tools | Python, orchestration, cloud | **SQL, dbt, Git, the warehouse** | SQL, BI tools, spreadsheets |
| Deliverable | data arrives, reliably | a modelled, tested, documented layer | an answer somebody acts on |
| Chapter | 46, 49 | this one | 13, 16 |

The role exists because of one change in how warehouses work. When storage and compute were expensive, you transformed data *before* loading it, because you couldn't afford to keep the raw version: **ETL**, extract-transform-load. Cloud warehouses made storage cheap and compute elastic, so the sensible order became **ELT**: load the raw data first, then transform it inside the warehouse with SQL.

That one change puts transformation where analysts already live, and it's why a tool whose entire job is "run my SQL in the right order, and test it" became a standard.

| | ETL | ELT |
|---|---|---|
| Transformation happens | in a separate tool, before loading | inside the warehouse, after loading |
| Raw data kept? | often not | usually, and it's the point (retention and privacy rules may still delete or mask some of it) |
| Written by | data engineers, often in a GUI or Python | analysts and analytics engineers, in SQL |
| Fixing a mistake means | reloading from the source | rebuilding models from raw data you still have |
| dbt's place | not used | the **T** |

---

## 32.2 Your first project

### Installing dbt

dbt is a Python program, so it goes into a virtual environment (Chapter 17), managed with `uv` as in section 29.4. It needs a folder to live in first. Make one, then turn it into a `uv` project:

<!-- run: none -->
```
# terminal, in the folder where you keep your projects
$ mkdir analytics
$ cd analytics
$ uv init --bare
Initialized project `analytics`
```

`uv init --bare` creates only a `pyproject.toml`, the list of what this folder needs. Section 29.4 used `uv init --package`, which also creates a `src/` folder for your own Python code; here the only code will be SQL, so the bare version is enough. Now add dbt and the **adapter** for your database, the piece that lets dbt talk to PostgreSQL:

<!-- run: none -->
```
# terminal, in analytics
$ uv add dbt-core dbt-postgres
Using CPython 3.14.7
Creating virtual environment at: .venv
Resolved 61 packages in 46ms
Installed 59 packages in 49ms
 + agate==1.9.1
 …
```

*(Trimmed: the full output lists all 59 packages, including dbt-core 1.12.5 and dbt-postgres 1.11.0. The first time, `uv` also downloads them, which takes a minute.)*

`uv add` did three things you know from section 29.4: it created the virtual environment in `.venv`, installed the two packages and everything they need, and recorded the exact versions in `uv.lock`. The `dbt` command lives inside `.venv`, so switch the environment on (Chapter 17), and check:

<!-- run: none -->
```
# terminal, in analytics
$ source .venv/bin/activate
$ dbt --version
Core:
  - installed: 1.12.5
  - latest:    1.12.5 - Up to date!

Plugins:
  - postgres: 1.11.0 - Up to date!
```

On Windows, in Git Bash the first line is `source .venv/Scripts/activate`, and in PowerShell it's `.venv\Scripts\Activate.ps1`. The environment stays on for this terminal window, including when you `cd` into subfolders; in a new window, activate it again. (The alternative is to put `uv run` in front of every command, `uv run dbt --version`, as Chapter 29 did.)

Adapters exist for Snowflake, BigQuery, Databricks, Redshift, DuckDB, SQL Server, and others; the project you write barely changes between them.

### Creating the project

<!-- run: none -->
```
# terminal, in analytics
$ dbt init riverstone_dbt --skip-profile-setup
19:04:31  Running with dbt=1.12.5
19:04:31  Your new dbt project "riverstone_dbt" was created!
$ cd riverstone_dbt
$ rm -r models/example
```

*(Trimmed: dbt also prints the new folder's full path and links to its documentation, and on its very first run it creates a `.dbt` folder in your home folder.)*

Every line dbt prints starts with the time, so yours will show different times. `dbt init` creates the project folder and its subfolders; `--skip-profile-setup` stops it asking connection questions, because you'll write that file yourself in a moment. `rm -r models/example` deletes the two sample models dbt includes (Chapter 34's `rm -r`: a folder and everything inside it, with no undo).

The folders that matter:

| Folder or file | Holds |
|---|---|
| `dbt_project.yml` | the project's name and settings: where things build, and how |
| `profiles.yml` | how to connect to the database (which is why it must not contain a password); you create it below |
| `models/` | your `SELECT` statements, one file per model |
| `snapshots/` | definitions for keeping type 2 history (section 32.5) |
| `tests/` | custom tests written as SQL (section 32.7) |
| `macros/` | reusable SQL snippets (section 32.11) |
| `seeds/` | small CSV files you want in the warehouse (a mapping table, say) |
| `target/` | everything dbt generates: compiled SQL, run results, docs. Never in Git |

`dbt init` also writes a `.gitignore` that already lists `target/`, `logs/`, `dbt_packages/`, and `.env`.

> **Jinja in two minutes.** dbt's files are **templates**. Before dbt uses a SQL or YAML file, it runs it through **Jinja**, a templating language from the Python world, and replaces three kinds of marker:
>
> | Syntax | Does | Example |
> |---|---|---|
> | `{{ ... }}` | works something out and puts the result in its place | `{{ ref('stg_orders') }}` |
> | `{% ... %}` | an instruction: `if`, `for`, `set`, `macro` | `{% if is_incremental() %}` |
> | `{# ... #}` | a comment that dbt removes, so it never reaches the database | `{# grain: one order line #}` |
>
> The first one you'll meet is `env_var`, which reads an environment variable (Chapter 29). In `profiles.yml` below, `{{ env_var('RIVERSTONE_HOST', 'localhost') }}` becomes `localhost`, unless you have set `RIVERSTONE_HOST`, in which case it becomes your value. Its two arguments are the variable's name and a default to use when the variable isn't set. `{{ env_var('RIVERSTONE_PASSWORD') }}` has no default on purpose: if you forget to set the password, dbt stops with an error instead of trying an empty one. Everything else in this chapter uses the same three markers.

### Connecting, without putting a password in a file

`profiles.yml` tells dbt how to reach the database. dbt looks for it first in the folder you run dbt from, then in a `.dbt` folder in your home folder (dbt's documentation, "About profiles.yml", checked 28 September 2026). This project keeps it in the project folder, beside the code, and reads secrets from environment variables, exactly as Chapter 29's package did. Create a file named `profiles.yml` in the `riverstone_dbt` folder (`code profiles.yml` opens it in VS Code) and type:

```yaml
# profiles.yml - how dbt connects. Keep the password out of this file and out of Git.
riverstone_dbt:
  target: dev
  outputs:
    dev:                     # the one-year database, for everyday work
      type: postgres
      host: "{{ env_var('RIVERSTONE_HOST', 'localhost') }}"
      port: 5432
      user: "{{ env_var('RIVERSTONE_USER', 'postgres') }}"
      password: "{{ env_var('RIVERSTONE_PASSWORD') }}"
      dbname: riverstone_2025
      schema: dbt_dev
      threads: 4
    large:                   # the three-year database, for the incremental example
      type: postgres
      host: "{{ env_var('RIVERSTONE_HOST', 'localhost') }}"
      port: 5432
      user: "{{ env_var('RIVERSTONE_USER', 'postgres') }}"
      password: "{{ env_var('RIVERSTONE_PASSWORD') }}"
      dbname: riverstone_perf
      schema: dbt_large
      threads: 4
    ci:                      # the throwaway database a CI run creates (section 32.12)
      type: postgres
      host: "{{ env_var('RIVERSTONE_HOST', 'localhost') }}"
      port: 5432
      user: "{{ env_var('RIVERSTONE_USER', 'postgres') }}"
      password: "{{ env_var('RIVERSTONE_PASSWORD') }}"
      dbname: riverstone_2025
      schema: dbt_ci
      threads: 4
```

In YAML the indentation is the structure (Chapter 26): each level is two spaces further in, and a line belongs to the nearest line above it that is indented less. Line by line:

- **`riverstone_dbt:`** names this **profile**. It must match the `profile:` line in `dbt_project.yml` (below); that's how the project finds its connection.
- **`target: dev`** is the connection used when you don't ask for another.
- **`outputs:`** lists the connections, called **targets**. There are three: `dev`, `large`, and `ci`.
- **`type: postgres`** says which adapter to use.
- **`host`**, **`port`**, **`user`**, **`password`**: where the server is and who logs in. `5432` is PostgreSQL's usual port (Chapter 34's ports).
- **`dbname`**: which database. `dev` and `ci` use `riverstone_2025`; `large` uses Chapter 28's three-year `riverstone_perf`, which section 32.10 uses to time an incremental build on 1.9 million rows.
- **`schema: dbt_dev`**: the schema dbt builds into, and the start of every schema name it creates (explained under the project file).
- **`threads: 4`**: build up to four models at the same time, when the dependency graph allows it (Figure 32.1).

The same models run against any of the three targets. The `ci` target is for section 32.12, where an automated check builds the project in a fresh database.

Now give dbt the password. Chapter 34 warned that typing a password into an `export` command leaves it in your shell history, so keep it in a `.env` file that only you can read. Create `.env` in the `riverstone_dbt` folder containing one line, `export RIVERSTONE_PASSWORD='your-password'` (your PostgreSQL password from Chapter 12), then:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ chmod 600 .env
$ source .env
$ dbt debug
19:05:04  Running with dbt=1.12.5
19:05:04  dbt version: 1.12.5
19:05:04  python version: 3.14.7
19:05:04  adapter type: postgres
19:05:04  adapter version: 1.11.0
19:05:04  Configuration:
19:05:04    profiles.yml file [OK found and valid]
19:05:04    dbt_project.yml file [OK found and valid]
19:05:04  Required dependencies:
19:05:04   - git [OK found]
19:05:04  Registered adapter: postgres=1.11.0
19:05:04    Connection test: [OK connection ok]

19:05:04  All checks passed!
```

*(Trimmed: the full output also lists file paths and every connection setting.)*

`chmod 600` makes the file readable only by you (Chapter 34), `source .env` runs its `export` line in this shell, and `dbt debug` checks everything dbt needs: the two files, Git, and a real connection. `.env` is already in `.gitignore`, so the password never reaches Git. `profiles.yml` itself can go into Git, because it holds nothing secret; many teams keep it in `~/.dbt/` instead, so that credentials never sit next to code at all. Either way, **if a `profiles.yml` ever contains a password, it goes in `.gitignore`.** Run `source .env` again in each new terminal window.

### The project file

`dbt init` wrote a `dbt_project.yml` full of comments. Replace its contents with this:

```yaml
name: 'riverstone_dbt'
version: '1.0.0'
profile: 'riverstone_dbt'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

models:
  riverstone_dbt:
    staging:
      +materialized: view
      +schema: staging
    marts:
      +materialized: table
      +schema: marts

snapshots:
  riverstone_dbt:
    +schema: snapshots
```

Line by line:

- **`name`** is the project's name; **`version`** is your own version number for it, in quotes so YAML keeps `1.0.0` as text rather than trying to read a number; **`profile`** names the connection in `profiles.yml`.
- The five **`*-paths`** lines say which folder holds each kind of file. They're the defaults, written out so you can see them.
- Under **`models:`**, `riverstone_dbt:` means "this project's models", and `staging:` and `marts:` are **folder names** inside `models/`: they must match real folders. A word **with** a `+` in front, like `+materialized`, is a **setting**; a word without one is a folder.
- **`+materialized`** says what dbt builds from each model: a view in `staging`, a table in `marts` (section 32.6 explains why).
- **`+schema`** puts the folder's models in their own schema. dbt names it `<target schema>_<custom schema>` (dbt's documentation, "Custom schemas", checked 28 September 2026): with the `dev` target, staging builds into `dbt_dev_staging`, marts into `dbt_dev_marts`, and snapshots into `dbt_dev_snapshots`. Another target has another prefix (`dbt_ci_marts`), so environments never overwrite each other.

Settings apply to a folder and everything under it, and a single model can override them (section 32.5 shows how).

---

## 32.3 Models, sources, and `ref`

A **model** is a file containing one `SELECT` statement. dbt wraps it in `CREATE TABLE AS` or `CREATE VIEW AS`, using the file name as the object name. That's the whole idea: you write the query, dbt handles the object.

### The CRM extract

Riverstone's customer details come from its CRM, whose nightly extract holds only today's values. Your database doesn't have that extract yet, so the companion file `ch32/setup_raw_crm.sql` makes a stand-in for it: a `raw_crm` schema holding a copy of the customers table, the way a loading tool would deliver it.

<!-- run: none -->
```sql
-- setup_raw_crm.sql - stands in for the CRM's nightly customer extract (Chapter 32).
-- It copies today's customer details into their own schema, the way a loading tool would.
CREATE SCHEMA raw_crm;

CREATE TABLE raw_crm.customers AS
SELECT customer_id, customer_name, city, segment
FROM public.customers;
```

`CREATE TABLE … AS SELECT` makes a new table from a query's result. Copy the file into your `analytics` folder and run it once. In DBeaver, open it on a `riverstone_2025` connection and execute it as a script, as in Chapter 12. In the terminal, use PostgreSQL's command-line client, `psql`:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ export PGPASSWORD="$RIVERSTONE_PASSWORD"
$ psql -h localhost -U postgres -d riverstone_2025 -f ../setup_raw_crm.sql
CREATE SCHEMA
SELECT 24
```

- **`PGPASSWORD`** is the variable `psql` reads its password from. It knows nothing about `RIVERSTONE_PASSWORD`, so the first line copies one into the other; without it, `psql` stops and asks.
- **`-h localhost`** is the server (this machine), **`-U postgres`** the user, **`-d riverstone_2025`** the database, and **`-f`** the file of SQL to run. (`-c "…"` instead runs one statement typed in quotes; section 32.9 uses it.)
- `SELECT 24` is PostgreSQL saying it copied 24 customers.

On Windows, `psql` lives in `C:\Program Files\PostgreSQL\16\bin`; if Git Bash says `psql: command not found`, add that folder to `PATH` (Chapter 34) or use DBeaver.

### Declaring where raw data comes from

Before building anything, tell dbt what the raw tables are. Create `models/staging` and `models/marts` (`mkdir models/staging models/marts`), then write `models/staging/sources.yml`:

```yaml
version: 2

sources:
  - name: erp
    description: Riverstone's ERP tables, loaded into the reporting database every night.
    schema: public
    tables:
      - name: orders
        description: One row per order.
        columns:
          - name: order_id
            data_tests: [unique, not_null]
      - name: order_items
        description: One row per product line within an order.
        columns:
          - name: order_item_id
            data_tests: [unique, not_null]
      - name: products
      - name: employees

  - name: crm
    description: The CRM's nightly customer extract, which holds only current values.
    schema: raw_crm
    tables:
      - name: customers
```

> **YAML, part 2.** Chapter 26 used YAML's basics: `key: value`, indentation, and lists written with `- `. dbt's files add three more patterns:
>
> - **A list whose items are maps.** `- name: orders` starts one item of the `tables:` list, and every line indented under it (`description:`, `columns:`) belongs to that item. The next `- name:` at the same indentation starts the next item.
> - **One-line forms.** `[unique, not_null]` is a two-item list written on one line, the same as two lines starting `- `. `{count: 24, period: hour}` is a map written on one line.
> - **Quotes keep text as text.** `'1.0.0'` and `"3.12"` stay text; unquoted, YAML might read them as numbers.
>
> If the indentation is wrong, dbt stops and names the file and line. VS Code's YAML extension underlines the mistake as you type.

Line by line:

- **`version: 2`** is the version of dbt's file format, not of your project; every properties file starts with it.
- **`sources:`** is a list of source systems. Each has a **`name`** (`erp`, `crm`), a **`description`**, the **`schema`** its tables are in, and a list of **`tables`**.
- Under a table, **`columns:`** lists columns you want to say something about, and **`data_tests:`** lists checks to run on them (section 32.7): here, that `order_id` is `unique` and `not_null` in the raw data itself.

Declaring sources buys three things: `{{ source('erp', 'orders') }}` instead of a hard-coded name, tests that run against the raw tables, and sources that appear in the lineage graph so everyone can see where the data entered.

Note what isn't there: a `database:` line. Leaving it out lets the same project run against `riverstone_2025` or `riverstone_perf` by switching target. Hard-coding the database is a mistake worth avoiding early, because it fails only when someone tries a second environment.

### A first model

`models/staging/stg_orders.sql`:

<!-- run: none -->
```sql
-- One row per order, with cancelled orders flagged.
select
    order_id,
    customer_id,
    sales_rep_id,
    order_date,
    status,
    status <> 'Cancelled' as is_counted
from {{ source('erp', 'orders') }}
```

- **`{{ source('erp', 'orders') }}`** is replaced by the real table name (`"riverstone_2025"."public"."orders"`): the source named `erp` in `sources.yml`, table `orders`.
- **`status <> 'Cancelled' as is_counted`** makes a true/false column: the comparison is worked out for each row and stored as a **boolean**. If `status` were ever NULL, the comparison would give NULL, and the fact table's `where o.is_counted` would drop that order silently; the `not_null` test on `status` in section 32.7 guards against that.

Net revenue needs a rule, and the rule should exist in exactly one place. Create `macros/net_revenue.sql` with these four lines now; section 32.11 explains how a macro works:

<!-- run: none -->
```sql
{# The one definition of net revenue in the whole project (Chapter 13's rule). #}
{% macro net_revenue(quantity, unit_price, discount_pct) -%}
    round({{ quantity }} * {{ unit_price }} * (1 - {{ discount_pct }} / 100.0), 2)
{%- endmacro %}
```

For now, read it as "wherever a model writes `{{ net_revenue(...) }}`, put this arithmetic". Then `models/staging/stg_order_items.sql`, which uses it:

<!-- run: none -->
```sql
-- One row per order line, with net revenue and cost computed once, here, for everyone.
select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct,
    {{ net_revenue('oi.quantity', 'oi.unit_price', 'oi.discount_pct') }} as net_revenue,
    oi.quantity * p.unit_cost as product_cost
from {{ source('erp', 'order_items') }} as oi
join {{ source('erp', 'products') }} as p on p.product_id = oi.product_id
```

The join to `products` fetches `unit_cost`, one row per product, so it can't change the number of rows (section 32.4). And `models/staging/stg_products.sql`:

<!-- run: none -->
```sql
-- One row per product. The ERP's unit_price is the list price, so staging gives it that name.
select
    product_id,
    product_name,
    category,
    unit_price as list_price,
    unit_cost
from {{ source('erp', 'products') }}
```

Renaming is one of staging's jobs: `unit_price as list_price` gives the column a clearer business name, and if the ERP ever renames it, this is the one place to change.

### `ref`: the function that makes dbt work

Models refer to each other with `{{ ref('model_name') }}`, never by table name. Riverstone's fact model, in section 32.5, starts:

<!-- run: none -->
```sql
from {{ ref('stg_order_items') }} as oi
join {{ ref('stg_orders') }} as o on o.order_id = oi.order_id
```

`ref` does two jobs at once:

1. **It resolves to the right name at run time.** In your development target it becomes `"riverstone_2025"."dbt_dev_staging"."stg_orders"`; in the `ci` target, `dbt_ci_staging`. You never write a schema name in a model.
2. **It builds the dependency graph.** Because `fct_sales_line` refs `stg_orders`, dbt knows `stg_orders` must be built first. Nobody maintains a build order.

See it for yourself. `dbt compile` renders the Jinja without running anything; `--select` picks which model:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt compile --select stg_order_items
19:05:33  Running with dbt=1.12.5
19:05:33  Registered adapter: postgres=1.11.0
19:05:33  Unable to do partial parsing because saved manifest not found. Starting full parse.
19:05:34  [WARNING]: Configuration paths exist in your dbt_project.yml file which do not apply to any resources.
There are 2 unused configuration paths:
- models.riverstone_dbt.marts
- snapshots.riverstone_dbt
19:05:34  Found 3 models, 4 data tests, 5 sources, 478 macros
19:05:34  
19:05:34  Concurrency: 4 threads (target='dev')
19:05:34  
Compiled node 'stg_order_items' is:
-- One row per order line, with net revenue and cost computed once, here, for everyone.
select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct,
    round(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100.0), 2) as net_revenue,
    oi.quantity * p.unit_cost as product_cost
from "riverstone_2025"."public"."order_items" as oi
join "riverstone_2025"."public"."products" as p on p.product_id = oi.product_id
```

Read the lines before the SQL too. "Starting full parse" means dbt read every file in the project for the first time. The warning is harmless: `dbt_project.yml` has settings for `marts` and snapshots, and neither has any files yet. "Found 3 models, 4 data tests, 5 sources" counts what you've written: three staging models, the four tests in `sources.yml`, and five source tables. Then the compiled model: the macro has become arithmetic and the sources have become table names. **Everything dbt runs is SQL you can read**, and it's all written to `target/compiled/` when anything surprises you.

---

## 32.4 Layers: staging, intermediate, marts

dbt projects converge on the same three layers, because each answers a different question.

| Layer | One model per | Job | Materialized as |
|---|---|---|---|
| **staging** | source table | rename, cast, clean, compute row-level values. No joins that change the grain | view |
| **intermediate** | a step in a calculation | the awkward middle of a complicated transformation, split so each piece is readable and testable | view or ephemeral |
| **marts** | business concept | the tables people query: facts and dimensions, at a declared grain | table |

Riverstone's project once sections 32.5 to 32.10 are done:

```
models/
├── staging/
│   ├── sources.yml          where raw data comes from, and its tests
│   ├── schema.yml           tests and descriptions for the staging models
│   ├── stg_order_items.sql
│   ├── stg_orders.sql
│   └── stg_products.sql
└── marts/
    ├── schema.yml           tests and descriptions for the marts
    ├── dim_customer.sql
    ├── dim_date.sql
    ├── dim_product.sql
    ├── dim_sales_rep.sql
    ├── fct_daily_sales.sql
    └── fct_sales_line.sql
snapshots/
└── customers_snapshot.yml   history of the CRM's customers
tests/
└── assert_fact_total_matches_source.sql
macros/
└── net_revenue.sql
```

Naming conventions matter more than they look: `stg_` for staging, `dim_` and `fct_` for marts, `int_` for intermediate. A reader can tell what a model is from its name, and so can a reviewer looking at a pull request.

**Rules of thumb that keep projects readable:**

- **One source table, one staging model**, and everything downstream refs the staging model, never the source. If the ERP renames a column, exactly one file changes.
- **Don't join in staging** unless the join can't change the grain. `stg_order_items` joins products only to fetch `unit_cost`, one row per product, which can't fan out (Chapter 28's grain discipline, now enforced by habit).
- **Marts are wide and friendly.** Dimensions carry every attribute a report might slice by, spelled out in business language.
- **If a mart model is getting hard to read, split it** into intermediate models. Views cost nothing to keep.

![A dependency graph with arrows: ERP source tables feed three staging views, the CRM's customers feed a snapshot, and these feed four dimensions, a daily summary and a tall fact table, which Power BI reads](figures/fig32-1-project-layers.svg)

*Figure 32.1 — Sources on the left, marts on the right; each arrow points from a model to the model that uses it. dbt derives this graph from the `ref`, `source`, and snapshot calls in the files. The customer dimension is built from the snapshot of the CRM extract (section 32.5), and the ERP's employees table feeds `dim_sales_rep` directly for now (exercise 5 adds its staging model).*

---

## 32.5 Building the star schema as models

Chapter 28's dimensions become four short models, and the fact table a fifth. The date dimension is pure SQL with no source at all. `models/marts/dim_date.sql`:

<!-- run: none -->
```sql
{{ config(materialized='table') }}
-- One row per calendar day of 2025 (Chapter 28's date dimension).
with days as (
    select generate_series(date '2025-01-01', date '2025-12-31', interval '1 day')::date as full_date
)
select
    to_char(full_date, 'YYYYMMDD')::int as date_key,
    full_date,
    trim(to_char(full_date, 'Day')) as day_name,
    date_trunc('month', full_date)::date as month_start,
    to_char(full_date, 'YYYY-"Q"Q') as quarter_label,
    extract(isodow from full_date) in (6, 7) as is_weekend
from days
```

- **`{{ config(materialized='table') }}`** sets options for this model alone, overriding `dbt_project.yml`. `dim_date` is in `marts`, so it's already a table; the line is here to show the syntax, and exercise 9 changes it to a view.
- **`generate_series(…)`** makes one row per day from 1 January to 31 December (Chapter 13's date spine); `::date` turns each timestamp into a date.
- **`to_char(full_date, 'YYYYMMDD')::int`** turns 2025-03-14 into the number 20250314, Chapter 28's date key.
- **`to_char(full_date, 'YYYY-"Q"Q')`** prints `2025-Q1`: text in double quotes is copied as it is, and the second `Q` is the quarter number.
- **`extract(isodow from full_date)`** numbers the days Monday 1 to Sunday 7, so 6 and 7 are the weekend.

The product dimension is a rename of a staging model, `models/marts/dim_product.sql`:

<!-- run: none -->
```sql
select
    product_id as product_key,
    product_id,
    product_name,
    category,
    list_price,
    unit_cost
from {{ ref('stg_products') }}
```

It reads `stg_products` through `ref`, so dbt builds the staging view first. `product_id` appears twice: once as `product_key`, the dimension's key in Chapter 28's style, and once as itself, for joining back to the source. `list_price` is the name staging gave `unit_price`.

The sales rep dimension, `models/marts/dim_sales_rep.sql`, adds the "no rep recorded" row that Chapter 28 argued for, so no order is dropped by an inner join:

<!-- run: none -->
```sql
select
    employee_id as sales_rep_key,
    employee_id,
    employee_name as rep_name,
    job_title
from {{ source('erp', 'employees') }}
union all
select -1, null, 'No rep recorded', 'Unknown'
```

The first `select` gives one row per employee, with `employee_id` as the key; `union all` adds a sixth row, key `-1`, for orders with no rep. This breaks section 32.4's rule on purpose: there is no `stg_employees` yet, so the dimension reads the source directly. Exercise 5 adds the staging model and shows the lineage graph change.

### The customer dimension needs history: a snapshot

Chapter 28 built a type 2 customer dimension by reconstructing history from an audit log. Most source systems don't keep one: the CRM holds today's values and overwrites yesterday's. A dbt **snapshot** solves that by recording what a table looked like each time it runs. `snapshots/customers_snapshot.yml`:

```yaml
snapshots:
  - name: customers_snapshot
    relation: source('crm', 'customers')
    config:
      unique_key: customer_id
      strategy: check
      check_cols: [city, segment]
```

- **`relation:`** is the table to watch: the CRM extract.
- **`config:`** says how to watch it. **`unique_key`** identifies the business entity, as in Chapter 28. **`strategy: check`** compares the columns in **`check_cols`** with the stored version and writes a new row when any of them differ. The alternative, `strategy: timestamp`, uses an `updated_at` column and is cheaper when the source maintains one reliably.
- dbt adds `dbt_valid_from`, `dbt_valid_to`, and `dbt_scd_id` to every row. `dbt_scd_id` is a key for one version of one customer: a long hashed text value rather than Chapter 28's 1, 2, 3, but it does the same job.

(Snapshots have been configured in YAML like this since dbt 1.9; older projects define them in SQL files with a `{% snapshot %}` block. dbt's documentation, "Add snapshots to your DAG", checked 28 September 2026.)

The dimension model then reads the snapshot, `models/marts/dim_customer.sql`:

<!-- run: none -->
```sql
-- A type 2 customer dimension, built from the snapshot dbt maintains (Chapter 28, section 28.10).
-- dbt records history from the first snapshot onwards, so the first version of each customer is
-- opened far enough in the past to cover the orders we already hold.
with versions as (
    select
        dbt_scd_id as customer_key,
        customer_id,
        customer_name,
        city,
        segment,
        dbt_valid_from,
        dbt_valid_to,
        row_number() over (partition by customer_id order by dbt_valid_from) as version_number
    from {{ ref('customers_snapshot') }}
)
select
    customer_key,
    customer_id,
    customer_name,
    city,
    segment,
    case when version_number = 1 then timestamp '1900-01-01' else dbt_valid_from end as valid_from,
    coalesce(dbt_valid_to, timestamp '9999-12-31') as valid_to,
    dbt_valid_to is null as is_current
from versions
```

**How it works:**

- **`ref('customers_snapshot')`** reads the snapshot's table, and puts the snapshot before this model in the graph.
- **`row_number()`** numbers each customer's versions in date order (Chapter 13's window functions).
- The first version's start is moved back to **1900-01-01**. The snapshot's own start date is the day you first run it, long after every 2025 order; without this, no order would find a customer. Section 32.9 comes back to what that costs.
- A current version has no `dbt_valid_to`, so **`coalesce`** gives it Chapter 28's far-future end date, and **`is_current`** is true exactly when `dbt_valid_to` is NULL.

### The fact table

The fact table, `models/marts/fct_sales_line.sql`, joins the staging models to the dimensions, with the point-in-time join to the customer dimension that Chapter 28 introduced:

<!-- run: none -->
```sql
-- Grain: one non-cancelled order line.
select
    oi.order_item_id,
    oi.order_id,
    o.order_date,
    to_char(o.order_date, 'YYYYMMDD')::int as date_key,
    c.customer_key,
    p.product_key,
    coalesce(r.sales_rep_key, -1) as sales_rep_key,
    oi.quantity,
    oi.net_revenue,
    oi.product_cost
from {{ ref('stg_order_items') }} as oi
join {{ ref('stg_orders') }} as o on o.order_id = oi.order_id
join {{ ref('dim_customer') }} as c
      on c.customer_id = o.customer_id
     and o.order_date >= c.valid_from::date
     and o.order_date <  c.valid_to::date
join {{ ref('dim_product') }} as p on p.product_id = oi.product_id
left join {{ ref('dim_sales_rep') }} as r on r.employee_id = o.sales_rep_id
where o.is_counted
```

**How it works:**

- The grain is one row per `order_item_id`, from `stg_order_items`; every other join adds columns, never rows.
- **`to_char(o.order_date, 'YYYYMMDD')::int`** makes the `date_key` that matches `dim_date`.
- The join to **`dim_customer`** picks the customer version in effect on the order date, exactly as in Chapter 28, and stores its `customer_key`.
- **`where o.is_counted`** keeps only non-cancelled orders, using the flag from `stg_orders`.

It follows Chapter 28's fact table line for line, with two differences. It keeps `order_date` beside `date_key`, which exercise 12 needs. And instead of `IS NOT DISTINCT FROM`, it `left join`s the reps and uses `coalesce(…, -1)` to send an order with no rep to the "No rep recorded" row. This model has no `config` line: the project's default for `marts`, a table, is what it needs.

### Running it

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt build
19:05:53  Running with dbt=1.12.5
19:05:53  Registered adapter: postgres=1.11.0
19:05:54  Found 8 models, 4 data tests, 1 snapshot, 5 sources, 478 macros
19:05:54  
19:05:54  Concurrency: 4 threads (target='dev')
19:05:54  
19:05:54  2 of 13 START sql table model dbt_dev_marts.dim_sales_rep ...................... [RUN]
19:05:54  4 of 13 START snapshot dbt_dev_snapshots.customers_snapshot .................... [RUN]
19:05:54  1 of 13 START sql table model dbt_dev_marts.dim_date ........................... [RUN]
19:05:55  3 of 13 START sql view model dbt_dev_staging.stg_products ...................... [RUN]
19:05:55  3 of 13 OK created sql view model dbt_dev_staging.stg_products ................. [CREATE VIEW in 0.25s]
19:05:55  2 of 13 OK created sql table model dbt_dev_marts.dim_sales_rep ................. [SELECT 6 in 0.28s]
19:05:55  1 of 13 OK created sql table model dbt_dev_marts.dim_date ...................... [SELECT 365 in 0.28s]
19:05:55  5 of 13 START test source_not_null_erp_order_items_order_item_id ............... [RUN]
19:05:55  6 of 13 START test source_not_null_erp_orders_order_id ......................... [RUN]
19:05:55  4 of 13 OK snapshotted dbt_dev_snapshots.customers_snapshot .................... [SELECT 24 in 0.28s]
19:05:55  7 of 13 START test source_unique_erp_order_items_order_item_id ................. [RUN]
19:05:55  8 of 13 START test source_unique_erp_orders_order_id ........................... [RUN]
19:05:55  6 of 13 PASS source_not_null_erp_orders_order_id ............................... [PASS in 0.10s]
19:05:55  9 of 13 START sql table model dbt_dev_marts.dim_product ........................ [RUN]
19:05:55  7 of 13 PASS source_unique_erp_order_items_order_item_id ....................... [PASS in 0.10s]
19:05:55  5 of 13 PASS source_not_null_erp_order_items_order_item_id ..................... [PASS in 0.13s]
19:05:55  10 of 13 START sql table model dbt_dev_marts.dim_customer ...................... [RUN]
19:05:55  11 of 13 START sql view model dbt_dev_staging.stg_order_items .................. [RUN]
19:05:55  8 of 13 PASS source_unique_erp_orders_order_id ................................. [PASS in 0.07s]
19:05:55  12 of 13 START sql view model dbt_dev_staging.stg_orders ....................... [RUN]
19:05:55  9 of 13 OK created sql table model dbt_dev_marts.dim_product ................... [SELECT 8 in 0.08s]
19:05:55  10 of 13 OK created sql table model dbt_dev_marts.dim_customer ................. [SELECT 24 in 0.08s]
19:05:55  11 of 13 OK created sql view model dbt_dev_staging.stg_order_items ............. [CREATE VIEW in 0.08s]
19:05:55  12 of 13 OK created sql view model dbt_dev_staging.stg_orders .................. [CREATE VIEW in 0.07s]
19:05:55  13 of 13 START sql table model dbt_dev_marts.fct_sales_line .................... [RUN]
19:05:55  13 of 13 OK created sql table model dbt_dev_marts.fct_sales_line ............... [SELECT 326 in 0.04s]
19:05:55  
19:05:55  Finished running 1 snapshot, 5 table models, 4 data tests, 3 view models in 0 hours 0 minutes and 0.76 seconds (0.76s).
19:05:55  
19:05:55  Completed successfully
19:05:55  
19:05:55  Done. PASS=13 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=13
```

*(The times, and the timings in brackets, will differ on your machine; so may the order of lines that run at the same time.)*

How to read it:

- **"Found 8 models, 4 data tests, 1 snapshot, 5 sources"**: three staging models and five marts, the four tests in `sources.yml`, and the snapshot. The 13 **nodes** (models, tests, snapshots) are numbered "1 of 13" to "13 of 13".
- **START** and **OK** lines come in pairs. With four threads, up to four nodes run at once, which is why the numbers arrive out of order. `fct_sales_line` starts last, because everything it refs had to finish first. Nobody told dbt that; it read the `ref` calls.
- The bracket says what the database reported: **`SELECT 326`** means 326 rows went into the table, and **`CREATE VIEW`** means a view was made (views hold no rows).
- **`PASS=13`**: every node succeeded. `ERROR` and `SKIP` count failures and the nodes skipped because of them.

**`dbt build` is the command to learn.** It runs models, tests, snapshots, and seeds together, in dependency order, and **stops a branch of the graph when something upstream fails**, so a failed test doesn't let bad data through to the models below it. `dbt run` builds without testing, and `dbt test` tests without building; `build` is what you want on a schedule.

The result is a schema of tables you can query like any other, in DBeaver or `psql`:

<!-- db: riverstone_2025 -->

<!-- run: pg -->
```sql
SELECT COUNT(*) AS fact_rows,
       ROUND(SUM(net_revenue)) AS net_revenue,
       COUNT(DISTINCT customer_key) AS customer_versions
FROM dbt_dev_marts.fct_sales_line;
```

```
 fact_rows | net_revenue | customer_versions
-----------+-------------+-------------------
       326 |     4335471 |                23
(1 row)
```

326 lines and ₹43,35,471: the same numbers Chapter 28's hand-built star schema produced, which is the point. What changed is that the build order, the tests, and the documentation now come from the code itself. The 23 customer versions are 23 customers with one version each (the 24th, Home Plus, placed no orders in 2025), where Chapter 28's dimension has 27 rows for the same 24 customers.

```sql
SELECT d.quarter_label,
       c.segment,
       ROUND(SUM(f.net_revenue)) AS net_revenue
FROM dbt_dev_marts.fct_sales_line AS f
JOIN dbt_dev_marts.dim_date AS d ON d.date_key = f.date_key
JOIN dbt_dev_marts.dim_customer AS c ON c.customer_key = f.customer_key
GROUP BY d.quarter_label, c.segment
ORDER BY d.quarter_label, c.segment;
```

```
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
```

The twelve cells add up to ₹43,35,473, two rupees more than the total, because each cell was rounded on its own.

### The totals match Chapter 28; the history doesn't

Chapter 28 rebuilt three customers' 2025 history from the ERP's audit log: Metro Mart moved from Thane to Mumbai on 1 July, for instance, so its January to June orders belong to Thane. The snapshot has no such log. It starts from today's values, and the dimension stretches each customer's first version back to 1900, so every Metro Mart order shows as Mumbai. This query puts the two builds side by side.

<!-- run: pg -->
```sql
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
```

```
    built_by     |  city  | net_revenue
-----------------+--------+-------------
 Chapter 28 star | Mumbai |      177258
 Chapter 28 star | Thane  |      152040
 dbt project     | Mumbai |      329298
(3 rows)
```

The first half reads Chapter 28's `dw` tables and the second the dbt marts, both for customer 5; `UNION ALL` stacks the two results, and the `built_by` column labels which is which.

> **Watch out: totals match; breakdowns don't.** For Patel Kitchenware, Metro Mart, and Harbour Traders, results by city or segment differ from Chapter 28's. Section 32.9 explains why, and what to do about it.

---

## 32.6 Materializations: view, table, incremental, ephemeral

A **materialization** is how dbt turns a model's `SELECT` into something in the database. Four cover almost everything.

| Materialization | dbt creates | Build cost | Query cost | Use for |
|---|---|---|---|---|
| **view** | a view | almost none | the full query, every time | staging models, small transformations |
| **table** | a table, rebuilt each run | full rebuild | fast | marts, anything queried often |
| **incremental** | a table, updated with new rows | only the new rows | fast | large fact tables (section 32.10) |
| **ephemeral** | nothing: the SQL is pasted into the models that ref it | nothing stored | its SQL runs inside every model that uses it | small intermediate steps you don't want cluttering the warehouse |

![Four rows: view, table, incremental and ephemeral, each with what dbt creates, what it suits, and what it costs to build and to query](figures/fig32-2-materializations.svg)

*Figure 32.2 — The choice is a trade between build cost and query cost.*

The defaults in `dbt_project.yml` (views for staging, tables for marts) are the usual starting point, and the reasoning is worth keeping:

- **Staging as views** means no storage and no staleness: a view always reflects the raw table underneath. Since marts are built on top and materialized as tables, the view is read once per run, not once per dashboard.
- **Marts as tables** means the expensive joins happen once per run, not once per person who opens a report.

Switch one and see what happens if you change it. Before you run it, predict what the bracket at the end of the line will say. Add `{{ config(materialized='view') }}` as the first line of `dim_product.sql`, then build just that model: `dbt run` builds without testing, and `--select dim_product` picks the one model.

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt run --select dim_product
19:06:20  1 of 1 START sql view model dbt_dev_marts.dim_product .......................... [RUN]
19:06:20  1 of 1 OK created sql view model dbt_dev_marts.dim_product ..................... [CREATE VIEW in 0.08s]
```

Now delete the `config` line and run the same command again:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt run --select dim_product
19:06:23  1 of 1 START sql table model dbt_dev_marts.dim_product ......................... [RUN]
19:06:23  1 of 1 OK created sql table model dbt_dev_marts.dim_product .................... [SELECT 8 in 0.13s]
```

*(Both trimmed to the lines about the model; the rest is the same header and summary as before.)*

The first run replaced the table with a view: `CREATE VIEW`, and no row count, because a view stores none. The second put the table back: `SELECT 8` is PostgreSQL telling you eight rows were written.

> **Watch out: a table is a snapshot of the moment it was built.** Everything in a mart is as fresh as the last `dbt build`, which is why teams put "data as of" on dashboards (Chapter 28's staleness warning) and why the schedule matters as much as the models. If a number must be live to the second, it doesn't belong in a mart.

---

## 32.7 Tests: the part that earns the trust

A dbt **test** is a query that should return **no rows**. If it returns rows, something is wrong, and dbt tells you how many.

### Built-in tests

Four generic tests cover most of what goes wrong, and they're declared in YAML beside the models. `models/staging/schema.yml` tests the staging models:

```yaml
version: 2

models:
  - name: stg_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: status
        data_tests: [not_null]
  - name: stg_order_items
    columns:
      - name: order_item_id
        data_tests: [unique, not_null]
      - name: net_revenue
        data_tests: [not_null]
  - name: stg_products
    columns:
      - name: product_id
        data_tests: [unique, not_null]
```

It has the same shape as `sources.yml`, with `models:` in place of `sources:`: a list of models, each with the columns to test. `models/marts/schema.yml` tests the marts, and uses the two tests that take settings:

```yaml
version: 2

models:
  - name: fct_sales_line
    description: "Grain: one non-cancelled order line. The single source for sales reporting."
    columns:
      - name: order_item_id
        data_tests: [unique, not_null]
      - name: customer_key
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_customer')
                field: customer_key
      - name: date_key
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_date')
                field: date_key
      - name: net_revenue
        data_tests: [not_null]
  - name: dim_customer
    description: "Type 2 customer dimension: one row per customer per period their details stayed the same."
    columns:
      - name: customer_key
        data_tests: [unique, not_null]
      - name: segment
        data_tests:
          - accepted_values:
              arguments:
                values: ['Retail', 'Hospitality', 'Wholesale']
  - name: dim_date
    columns:
      - name: date_key
        data_tests: [unique, not_null]
```

- **`unique`** and **`not_null`** are grain and completeness checks: exactly Chapter 28's habit of testing what one row represents.
- **`relationships`** is a foreign key that the warehouse doesn't enforce: every `customer_key` in the fact table must exist in the dimension. This is the test that catches a dimension load that silently dropped rows. It needs settings, so it's written as a list item that is itself a map: **`arguments:`** holds them, **`to:`** names the other model and **`field:`** its column. (Before dbt 1.10.5, the settings sat directly under the test name without `arguments:`; you'll see both in older projects. dbt's documentation, "data_tests", checked 28 September 2026.)
- **`accepted_values`** catches new categories appearing without warning, which is how "Retail" quietly becomes "retail " and a dashboard loses a segment. Its one setting, **`values`**, is the list of allowed values.
- **`description`** is documentation, used in section 32.8.

More live in packages: `dbt_utils` adds tests for expressions, row counts between two models, recency, and mutually exclusive ranges; `dbt_expectations` ports the Great Expectations catalog (Chapter 47).

### A custom test: the reconciliation

Generic tests check shapes. The test that protects the business most directly is the one that checks a number against something outside the model. Chapter 28 reconciled the star schema to the source by hand; here it runs on every build. The test is a file in the `tests/` folder.

<!-- run: none -->
```sql
-- tests/assert_fact_total_matches_source.sql
-- The reconciliation from Chapter 28: the fact table must total what the source says, to the paisa.
-- A dbt test passes when it returns no rows.
with fact as (select sum(net_revenue) as total from {{ ref('fct_sales_line') }}),
source_total as (
    select sum({{ net_revenue('oi.quantity', 'oi.unit_price', 'oi.discount_pct') }}) as total
    from {{ source('erp', 'order_items') }} as oi
    join {{ source('erp', 'orders') }} as o on o.order_id = oi.order_id
    where o.status <> 'Cancelled'
)
select fact.total as fact_total, source_total.total as source_total
from fact, source_total
where abs(fact.total - source_total.total) > 0.01
```

Any `.sql` file in `tests/` is a **singular test**: it passes when the query returns nothing. This one returns a row only when the fact table and the source disagree by more than a paisa. Its source side reuses the `net_revenue` macro, so it checks the joins and filters (a dropped line, a cancelled order let through), not the revenue formula itself; answer 8 shows how to close that gap with a total from outside the project.

Run `dbt build` again, and the 20 new tests run too: "Found 8 models, 24 data tests" and `PASS=33`.

### What a failure looks like

Suppose someone "tidies up" `fct_sales_line` and turns the last line, `where o.is_counted`, into a comment, so cancelled orders creep in. The `+` after the model's name selects it *and everything downstream of it*:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt build --select fct_sales_line+
19:06:44  1 of 8 START sql table model dbt_dev_marts.fct_sales_line ...................... [RUN]
19:06:44  1 of 8 OK created sql table model dbt_dev_marts.fct_sales_line ................. [SELECT 330 in 0.09s]
19:06:44  2 of 8 START test assert_fact_total_matches_source ............................. [RUN]
19:06:44  2 of 8 FAIL 1 assert_fact_total_matches_source ................................. [FAIL 1 in 0.10s]
19:06:45  Completed with 1 error, 0 partial successes, and 0 warnings:
19:06:45  
19:06:45  [ERROR]: in test assert_fact_total_matches_source (tests/assert_fact_total_matches_source.sql)
19:06:45    Got 1 result, configured to fail if != 0
19:06:45  
19:06:45    compiled code at target/compiled/riverstone_dbt/tests/assert_fact_total_matches_source.sql
19:06:45  
19:06:45  Done. PASS=7 WARN=0 ERROR=1 SKIP=0 NO-OP=0 REUSED=0 TOTAL=8
$ echo "exit code $?"
exit code 1
```

*(Trimmed: the header, and the lines for the six tests that passed.)*

Three things to notice. `SELECT 330`: the four lines of the two cancelled orders got in, and only the reconciliation noticed; every shape test passed. The build **failed** with exit code 1, so a scheduler sees it and raises an alarm (Chapter 29's exit codes, Chapter 34's `$?`). And the message names the **path to the compiled SQL**, so you can run the failing query yourself and look at the row. Put the line back and the same command ends `PASS=8`.

![Two columns: run-then-test lets a bad fact table reach dashboards before the tests fail; dbt build tests each model as it goes, fails on the grain test, and skips everything downstream](figures/fig32-3-build-stops-the-branch.svg)

*Figure 32.3 — `dbt build` stops a branch of the graph the moment a test fails, so bad data doesn't reach the models below it.*

### How much to test

| Test | Where | Why |
|---|---|---|
| `unique` + `not_null` on the grain | every model | the single most common failure |
| `relationships` on every key in a fact table | marts | catches incomplete dimension loads |
| `accepted_values` on categories reports group by | marts | catches new or misspelled values |
| a reconciliation to the source | one per mart | catches everything else |
| freshness on sources (`dbt source freshness`) | sources | catches a load that didn't run |

A useful discipline: **when a number is wrong in production, add the test that would have caught it** before you fix the model. The project's test suite then grows out of real failures rather than good intentions.

---

## 32.8 Documentation and lineage

Descriptions live in the same YAML as the tests, next to the thing they describe. That's the only way documentation stays true: if it isn't beside the code, it drifts.

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt docs generate
19:07:08  Found 8 models, 24 data tests, 1 snapshot, 5 sources, 478 macros
19:07:08  Building catalog
$ dbt docs serve
Serving docs at 8080
To access from your browser, navigate to: http://localhost:8080

Press Ctrl+C to exit.
```

*(Trimmed: the usual header lines, and a last line giving the full path of the `catalog.json` file it wrote into `target/`.)*

`dbt docs generate` reads the project and the database's own list of tables and columns, and writes a small website into `target/`. `dbt docs serve` starts a web server on your own machine and opens the site in your browser: `localhost` is this computer and 8080 is the port the server listens on (Chapter 34). The terminal stays busy while it serves; press Ctrl+C to stop it.

The generated site gives you, for every model: its description, every column with its description and tests, the compiled SQL, and an interactive **lineage graph** showing what it depends on and what depends on it. The graph isn't drawn by anyone; it's the `ref` calls.

**What it's actually for**, day to day:

- *"Where does this number come from?"* Click the column, read the description, open the SQL.
- *"If I change this source, what breaks?"* Look downstream in the graph.
- *"Is this metric the same as that one?"* Two models both calling `{{ net_revenue(...) }}` are the same by construction; two different formulas are visible as two different formulas.

Two habits make it worth the small effort: describe a model in **one sentence that states its grain** (Chapter 28), and describe any column whose meaning someone could get wrong. Don't describe `order_id` as "the order id".

---

## 32.9 Snapshots: history dbt keeps for you

Section 32.5 set the snapshot up, and its first run stored one version of each of the 24 customers. Its value shows the next time the source changes. `dbt snapshot` runs only the snapshots in the project.

Watch it work. Suppose the CRM reclassifies Evergreen Mart, a Retail customer in Indore, as Wholesale. Make that change in the stand-in extract (in DBeaver, or with `psql`, whose `-c` runs the one statement in quotes), then take a new snapshot:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ psql -h localhost -U postgres -d riverstone_2025 -c "UPDATE raw_crm.customers SET segment = 'Wholesale' WHERE customer_id = 18"
UPDATE 1
$ dbt snapshot
19:07:29  Found 8 models, 24 data tests, 1 snapshot, 5 sources, 478 macros
19:07:29  1 of 1 START snapshot dbt_dev_snapshots.customers_snapshot ..................... [RUN]
19:07:29  1 of 1 OK snapshotted dbt_dev_snapshots.customers_snapshot ..................... [INSERT 0 1 in 0.24s]
19:07:29  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=1
$ dbt build --select dim_customer+
19:07:32  1 of 12 OK created sql table model dbt_dev_marts.dim_customer .................. [SELECT 25 in 0.09s]
19:07:32  5 of 12 OK created sql table model dbt_dev_marts.fct_sales_line ................ [SELECT 326 in 0.04s]
19:07:32  Done. PASS=12 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=12
```

*(Trimmed to the lines that matter; `PGPASSWORD` is still set from section 32.3, or `psql` would ask for the password.)*

`INSERT 0 1`: the snapshot closed Evergreen Mart's old version and added one new row. `dim_customer` now has 25 rows, and the fact table still has 326 lines, because every 2025 order falls in the first version. Evergreen Mart's versions:

<!-- db: riverstone_2025 -->

<!-- run: pg -->
```sql
SELECT customer_id, customer_name, segment,
       valid_from::date AS valid_from, valid_to::date AS valid_to, is_current
FROM dbt_dev_marts.dim_customer
WHERE customer_id = 18
ORDER BY valid_from;
```

```
 customer_id | customer_name  |  segment  | valid_from |  valid_to  | is_current
-------------+----------------+-----------+------------+------------+------------
          18 | Evergreen Mart | Retail    | 1900-01-01 | 2026-09-28 | f
          18 | Evergreen Mart | Wholesale | 2026-09-28 | 9999-12-31 | t
(2 rows)
```

Two versions, one closed and one current, built by a tool instead of by the careful `UPDATE`-then-`INSERT` transaction of Chapter 28. The change date is the day the snapshot ran, so yours will be the day you run it. That is the snapshot's whole nature: it records *when it noticed* a change, not when the change happened.

> **Watch out: a snapshot only knows what it has seen.** dbt records history from the first time the snapshot runs, not before. Riverstone's first versions therefore start on the day snapshotting began, which would leave every 2025 order without a matching customer version, so `dim_customer` opens each customer's first version in 1900. That is why section 32.5's Metro Mart orders all show as Mumbai: the move from Thane happened in July 2025, long before the first snapshot, and nothing recorded it. Two lessons: **start snapshotting the day you think you might ever want history**, and when a source system does keep an audit log (Chapter 28's `customer_changes`), reconstructing from it gives you history you never captured.

> **Watch out: snapshots are precious.** The snapshot table is the only record of what the source used to say. Never point a snapshot at a different source, never run it against a temporary copy of the data, and back it up like any other irreplaceable table.

---

## 32.10 Incremental models

Rebuilding a mart every run is fine until the fact table has millions of rows. An **incremental** model builds fully the first time, and afterwards processes only what's new. Riverstone's daily summary is a good candidate.

<!-- run: none -->
```sql
-- models/marts/fct_daily_sales.sql
{{ config(materialized='incremental', unique_key='order_date', incremental_strategy='delete+insert') }}
-- One row per day: rebuilt only for days that changed since the last run.
select
    o.order_date,
    count(distinct o.order_id) as orders,
    sum(oi.net_revenue) as net_revenue
from {{ ref('stg_orders') }} as o
join {{ ref('stg_order_items') }} as oi on oi.order_id = o.order_id
where o.is_counted
{% if is_incremental() %}
  and o.order_date >= (select coalesce(max(order_date), date '1900-01-01') from {{ this }})
{% endif %}
group by o.order_date
```

**How it works:**

- **`materialized='incremental'`** tells dbt to create the table on the first run, and to insert into it afterwards.
- **`is_incremental()`** is true only when the table already exists and the run isn't a full refresh. The `and` line inside the `{% if %}` limits the work to recent days; on the first run, dbt leaves it out.
- **`{{ this }}`** is the model's own table, so the filter can ask "what's the latest day I already have?".
- **`incremental_strategy='delete+insert'`** with a **`unique_key`** replaces the days it rebuilds instead of duplicating them. That matters because the newest day is usually incomplete: it gets rebuilt tomorrow. Other strategies are `append` (fastest, no deduplication) and `merge` (an upsert, on warehouses that support it).

Add its grain test to `models/marts/schema.yml`, at the end of the `models:` list, and build it with `dbt build --select fct_daily_sales` (the model and its two tests, `PASS=3`):

```yaml
  - name: fct_daily_sales
    columns:
      - name: order_date
        data_tests: [unique, not_null]
```

On 175 orders the saving is invisible. On Chapter 28's three-year database (1,926,847 order lines, 1,096 days) it isn't. Measured on the machine used to test this chapter (four processor cores, 16 GB of memory):

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt run --target large --select +fct_daily_sales --full-refresh
19:07:51  1 of 3 OK created sql view model dbt_large_staging.stg_order_items ............. [CREATE VIEW in 0.14s]
19:07:51  2 of 3 OK created sql view model dbt_large_staging.stg_orders .................. [CREATE VIEW in 0.14s]
19:07:53  3 of 3 OK created sql incremental model dbt_large_marts.fct_daily_sales ........ [SELECT 1096 in 2.19s]
19:07:53  Finished running 1 incremental model, 2 view models in 0 hours 0 minutes and 2.50 seconds (2.50s).
$ dbt run --target large --select fct_daily_sales
19:07:57  1 of 1 OK created sql incremental model dbt_large_marts.fct_daily_sales ........ [INSERT 0 1 in 0.55s]
19:07:57  Finished running 1 incremental model in 0 hours 0 minutes and 0.68 seconds (0.68s).
```

*(Trimmed to the result lines. Timings vary from run to run and machine to machine; two more runs gave 2.16 and 2.25 seconds for the full build, and 0.50 and 0.51 for the incremental one.)*

- **`--target large`** uses the `large` connection in `profiles.yml`, so the same models build into `riverstone_perf`.
- **`+fct_daily_sales`**, with the plus in front, selects the model **and everything it depends on**, here its two staging views (a plus after the name, as in section 32.7, selects everything that depends on it).
- **`--full-refresh`** rebuilds an incremental table from scratch, as if it had never existed.

The full build wrote all 1,096 days (`SELECT 1096`). The second run found the table already there, rebuilt only the latest day, and inserted one row (`INSERT 0 1`). **2.19 seconds against 0.55**: about four times faster here, and the gap grows with the table, because the full build reads every line while the incremental one writes only the newest days. On a cloud warehouse billed by compute, that ratio is the bill.

**When to make a model incremental:** when a full rebuild is slow enough to hurt, and rows arrive rather than change. **When not to:** small models (the complexity isn't worth it), and models whose history changes (a customer dimension where old rows get corrected). The rule of thumb is to start with a table and convert when the run time bothers you.

> **Watch out: incremental models drift.** Late-arriving data, back-dated corrections, and changed business logic all leave an incremental table holding rows built by yesterday's rules. Defenses: a **lookback window** (`>= max(order_date) - interval '3 days'`) rather than a hard `>=`, a scheduled **`--full-refresh`** (weekly is common), and a test that compares the model's totals against a full recomputation. If you change the model's logic, refresh it fully; dbt will not do it for you.

---

## 32.11 Macros: write a rule once

A **macro** is a reusable piece of SQL written in Jinja. You created Riverstone's only one in section 32.3, `macros/net_revenue.sql`:

<!-- run: none -->
```sql
{# The one definition of net revenue in the whole project (Chapter 13's rule). #}
{% macro net_revenue(quantity, unit_price, discount_pct) -%}
    round({{ quantity }} * {{ unit_price }} * (1 - {{ discount_pct }} / 100.0), 2)
{%- endmacro %}
```

**How it works:**

- **`{% macro net_revenue(quantity, unit_price, discount_pct) %}`** … **`{% endmacro %}`** defines a macro with a name and three **arguments**, like a Python function (Chapter 17).
- Inside, **`{{ quantity }}`** is replaced by whatever was passed as `quantity`. A model calls `{{ net_revenue('oi.quantity', 'oi.unit_price', 'oi.discount_pct') }}`, with each argument **in quotes**, because the macro works on text: it pastes the text `oi.quantity` into the SQL, where the database then reads it as a column. Without the quotes, Jinja would look for a variable called `oi` and fail.
- The **`-`** inside `-%}` and `{%-` trims the blank lines and spaces next to the tag, so the compiled SQL shows the arithmetic on one line (section 32.3's compile output) rather than surrounded by empty lines.
- It is Chapter 13's rule, now **rounded to the paisa on each line** with `round(…, 2)`. Chapter 13's `sales_lines` view doesn't round, so a total built from this macro can differ from `sales_lines` by a few paise. The reconciliation test is safe because both of its sides use the macro; a test against `sales_lines` itself would need a tolerance of about a rupee.

The value isn't saving keystrokes; it's that Chapter 13's argument about whose revenue number is right can only have one answer, and changing the rule means changing one file, reviewed in one pull request.

The three markers are the ones from section 32.2's "Jinja in two minutes". A loop earns its keep when a model repeats itself. `models/marts/mart_sales_monthly.sql` pivots revenue by category, without typing each category:

<!-- run: none -->
```sql
-- One row per month, with revenue split by product category.
{% set categories = ['Storage', 'Kitchen', 'Industrial', 'Furniture'] %}

select
    d.month_start,
    {% for category in categories %}
    sum(case when p.category = '{{ category }}' then f.net_revenue else 0 end)
        as revenue_{{ category | lower }}{{ "," if not loop.last }}
    {% endfor %}
from {{ ref('fct_sales_line') }} as f
join {{ ref('dim_product') }} as p on p.product_key = f.product_key
join {{ ref('dim_date') }} as d on d.date_key = f.date_key
group by d.month_start
```

Before you compile it, write down what you expect the lines between `d.month_start,` and `from` to become. Then:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt compile --select mart_sales_monthly
Compiled node 'mart_sales_monthly' is:
-- One row per month, with revenue split by product category.


select
    d.month_start,
    
    sum(case when p.category = 'Storage' then f.net_revenue else 0 end)
        as revenue_storage,
    
    sum(case when p.category = 'Kitchen' then f.net_revenue else 0 end)
        as revenue_kitchen,
    
    sum(case when p.category = 'Industrial' then f.net_revenue else 0 end)
        as revenue_industrial,
    
    sum(case when p.category = 'Furniture' then f.net_revenue else 0 end)
        as revenue_furniture
    
from "riverstone_2025"."dbt_dev_marts"."fct_sales_line" as f
join "riverstone_2025"."dbt_dev_marts"."dim_product" as p on p.product_key = f.product_key
join "riverstone_2025"."dbt_dev_marts"."dim_date" as d on d.date_key = f.date_key
group by d.month_start
```

*(Trimmed: the header lines.)*

Each construct, in one line:

- **`{% set categories = [...] %}`** stores a list of four names in a Jinja variable.
- **`{% for category in categories %}`** … **`{% endfor %}`** repeats the lines between them once per name, with `category` holding the current one.
- **`'{{ category }}'`** puts the name inside SQL quotes: `'Storage'`.
- **`{{ category | lower }}`** passes the name through the **filter** `lower`, giving `storage`, so the column is `revenue_storage`.
- **`{{ "," if not loop.last }}`** writes a comma after every column except the last: `loop.last` is true on the final pass, and `"," if …` is Jinja's one-line if.
- The empty lines are where the `{% %}` tags stood. They're harmless; the `-` marks from the macro would remove them.

A better version reads the category list from the warehouse itself with `dbt_utils.get_column_values`, so a new category appears in the report the day it appears in the data.

**Packages** bring other people's macros. A `packages.yml` file in the project folder lists them, and `dbt deps` downloads them into `dbt_packages/`:

<!-- run: none -->
```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.3.0", "<2.0.0"]
```

`version: [">=1.3.0", "<2.0.0"]` means any 1.x release from 1.3.0 on: new fixes arrive, but not a 2.0 that might change how things work. Riverstone's project doesn't need a package yet; exercise 13 adds this one. `dbt_utils` is the one nearly every project uses: `date_spine` (Chapter 13's date spine, as a macro), `star`, `generate_surrogate_key` (called `surrogate_key` before dbt_utils 1.0), `pivot`, and a shelf of extra tests. Check the current version on the dbt package hub when you add it.

> **Watch out: Jinja is a power tool.** A model that generates SQL through three nested loops is unreadable, un-lintable, and impossible for the next analyst to debug. The test: could a colleague work out what this produces without running it? If not, write the SQL out.

---

## 32.12 Linting and continuous integration

### SQLFluff

Chapter 13 promised automatic formatting for teams. **SQLFluff** is the SQL linter and formatter most dbt projects use; it understands dbt's Jinja through a **templater**, a separate package that compiles each model with dbt first, so it lints the SQL rather than choking on `{{ ref(...) }}`. Add both to the environment from the `analytics` folder with `uv add sqlfluff sqlfluff-templater-dbt`, as you added dbt. The configuration goes in a file named `.sqlfluff` in the `riverstone_dbt` folder.

```
# .sqlfluff - settings for the SQL linter
[sqlfluff]
templater = dbt
dialect = postgres
max_line_length = 120

[sqlfluff:templater:dbt]
project_dir = ./
profiles_dir = ./

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = lower
```

- **`[sqlfluff]`** holds the main settings: use the **dbt** templater, read the SQL as PostgreSQL's **dialect**, and allow lines up to 120 characters.
- **`[sqlfluff:templater:dbt]`** tells the templater where the project and `profiles.yml` are: `./`, this folder.
- **`[sqlfluff:rules:capitalisation.keywords]`** sets one rule: keywords such as `select` and `join` in lower case, the style this chapter uses.

Before you run it on the fact model, guess how many complaints a linter could have about SQL that works:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ sqlfluff lint models/marts/fct_sales_line.sql
=== [dbt templater] Sorting Nodes...
=== [dbt templater] Compiling dbt project...
=== [dbt templater] Project Compiled.
== [models/marts/fct_sales_line.sql] FAIL
L:   2 | P:   1 | ST06 | Select wildcards then simple targets before calculations
                       | and aggregates. [structure.column_order]
L:  14 | P:   1 | AM05 | Join clauses should be fully qualified. [ambiguous.join]
L:  14 | P:  38 | ST09 | Joins should list the table referenced earlier first.
                       | [structure.join_condition_order]
L:  15 | P:   1 | AM05 | Join clauses should be fully qualified. [ambiguous.join]
L:  16 | P:   1 | LT02 | Expected indent of 4 spaces. [layout.indent]
L:  16 | P:   9 | LT02 | Expected line break and indent of 8 spaces before 'c'.
                       | [layout.indent]
L:  17 | P:   1 | LT02 | Expected indent of 8 spaces. [layout.indent]
L:  18 | P:   1 | LT02 | Expected indent of 8 spaces. [layout.indent]
L:  18 | P:  24 | LT01 | Expected only single space before naked identifier.
                       | Found '  '. [layout.spacing]
L:  19 | P:   1 | AM05 | Join clauses should be fully qualified. [ambiguous.join]
All Finished!
```

Ten. `L:` is the line and `P:` the position in it; then the rule's code and message. The five rules:

- **ST06**: put plain columns before calculated ones (the `select` on line 2 has `to_char(…)` and `coalesce(…)` among plain columns).
- **AM05**: write `inner join`, not a bare `join`, so the kind of join is never left to the reader's memory.
- **ST09**: in a join condition, write the table that appeared earlier first: `oi.order_id = o.order_id`.
- **LT02**: indent in steps of four spaces, with each condition of a multi-line `on` on its own line.
- **LT01**: one space between words; line 18 lined up `<` with two spaces.

`sqlfluff fix` makes the fixes it can make safely, and says so:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ sqlfluff fix models/marts/fct_sales_line.sql
==== finding fixable violations ====
== [models/marts/fct_sales_line.sql] FIXED
10 fixable linting violations found
$ sqlfluff lint models/marts/fct_sales_line.sql
All Finished!
```

*(Trimmed: `fix` lists the same ten violations before "FIXED", and both commands print the templater's three lines.)*

All ten were mechanical, and the fixed model runs the same query: the calculated columns moved to the end of the `select`, each `join` became `inner join`, and the join conditions were turned round and re-indented. (The companion project keeps the model as section 32.5 prints it, so you can run the lint yourself.) Two pieces of advice from teams who have adopted SQLFluff: **turn rules off rather than arguing about them** (the point is consistency, not any particular style), and **run `fix` across the project in one commit** when you adopt it, so the first pull request afterwards isn't an unreadable mess of whitespace changes.

### Running everything on every pull request

Chapter 26 introduced continuous integration: automated checks on every change. For a dbt project the checks are obvious, and this workflow runs them. It goes in `.github/workflows/dbt.yml`, as Chapter 26's did:

```yaml
# Runs on every pull request: install, lint, then build and test the whole project against a scratch database.
name: dbt
on: [pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: ${{ secrets.CI_DATABASE_PASSWORD }}
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    env:
      RIVERSTONE_HOST: localhost
      RIVERSTONE_USER: postgres
      RIVERSTONE_PASSWORD: ${{ secrets.CI_DATABASE_PASSWORD }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install dbt-core dbt-postgres sqlfluff sqlfluff-templater-dbt
      - run: psql -h localhost -U postgres -c "CREATE DATABASE riverstone_2025" && ./load_test_data.sh
      - run: sqlfluff lint models/
      - run: dbt deps
      - run: dbt build --target ci
```

The parts Chapter 26's workflow didn't have:

- **`services: postgres:`** asks GitHub to start a fresh PostgreSQL 16 for this run, next to the job, and throw it away afterwards. It runs in a **container**, a small self-contained machine (Chapter 52 explains them); you only need to know it's a real, empty PostgreSQL.
- **`ports: ["5432:5432"]`** makes it reachable at `localhost:5432`, the same address as on your machine.
- **`options: >-`** passes settings that make the job wait until the database is ready. In YAML, `>-` means "the indented lines below are one long value".
- **`${{ secrets.CI_DATABASE_PASSWORD }}`** is GitHub's own template syntax, unrelated to dbt's `{{ }}` despite the look. It inserts a **secret** stored in the repository's settings: on GitHub, open the repository, then *Settings → Secrets and variables → Actions → New repository secret*, name it `CI_DATABASE_PASSWORD`, and paste a password. For a throwaway test database, a password written in the file would do no harm; the book uses a secret anyway, because the habit is the point.
- The job's **`env:`** sets the variables `profiles.yml` reads, and **`--target ci`** builds with the `ci` connection from section 32.2, into `dbt_ci_…` schemas.
- **`pip install`** rather than `uv`: the runner starts empty each time, and `pip` is already on it. (`astral-sh/setup-uv` is an alternative that installs `uv` first.)

**What it buys.** A pull request that breaks a test cannot be merged unnoticed. A model that doesn't compile is caught before it reaches production. And the reviewer's job shrinks to the part a human is good at: *is this the right business rule?*

Two refinements real teams add:

- **Build only what changed**, with dbt's state comparison: `dbt build --select state:modified+ --state ./prod-artifacts`. On a project with hundreds of models, rebuilding everything on every pull request is too slow.
- **Build into a separate schema per pull request**, so reviewers can query the proposed models without touching production.

### The finished project

With every section's files in place, one command builds and tests the whole project, exactly as the workflow does:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt build
19:09:09  Running with dbt=1.12.5
19:09:09  Registered adapter: postgres=1.11.0
19:09:10  Found 10 models, 26 data tests, 1 snapshot, 5 sources, 478 macros
19:09:10  
19:09:10  Concurrency: 4 threads (target='dev')
19:09:10  
19:09:10  3 of 37 START sql view model dbt_dev_staging.stg_products ...................... [RUN]
…
19:09:11  37 of 37 OK created sql table model dbt_dev_marts.mart_sales_monthly ........... [SELECT 12 in 0.03s]
19:09:11  
19:09:11  Finished running 1 incremental model, 1 snapshot, 6 table models, 26 data tests, 3 view models in 0 hours 0 minutes and 1.22 seconds (1.22s).
19:09:11  
19:09:11  Completed successfully
19:09:11  
19:09:11  Done. PASS=37 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=37
```

*(Trimmed: the full output has a START and a result line for each of the 37 nodes.)*

The count checks out: 10 models (3 staging, 7 marts), 1 snapshot, and 26 tests (4 on sources, 8 on staging, 13 on marts, 1 singular) make 37 nodes.

### Where dbt runs in production

dbt Core is a command-line tool: something has to run it on a schedule. The options, in rough order of how much they cost you:

| Option | What it is |
|---|---|
| `cron` on a small server (Chapter 34) | the simplest thing that works |
| An orchestrator: Airflow, Dagster, Prefect (Chapter 46) | dbt as one task among ingestion and downstream jobs |
| A container on a cloud scheduler | no server to maintain |
| **dbt Cloud** | dbt Labs' hosted product: scheduling, a browser IDE, CI, hosted docs, on a paid plan with a limited free tier |

The models, tests, and docs are identical either way. Check current dbt Cloud plans and prices on dbt Labs' site; they change, and this chapter was written against dbt Core 1.12.

---

## 32.13 What dbt is not, and the semantic layer

dbt only transforms data that's already in the warehouse. It does **not** extract or load (that's Fivetran, Airbyte, or your own Python, Chapter 46), does **not** schedule itself, is **not** a BI tool, and is **not** a database. A dbt project on a warehouse that nothing loads is a rota for an empty kitchen.

The one boundary that keeps moving is the **semantic layer**: the idea that metric definitions (revenue, active customer, churn) should live in one place that *every* tool asks, rather than being re-implemented in each dashboard. dbt has a semantic layer built on MetricFlow, where you define metrics in YAML alongside models and BI tools query them through an API. Competing approaches exist (Cube, Looker's LookML, and BI tools' own modeling layers), and this area changes fast enough that any specific instruction here would be stale by the time you read it.

**The idea, though, is stable, and you already have it**: Riverstone's `net_revenue` macro is a one-metric semantic layer. If a metric's definition lives in one file, is tested, and everything downstream refs it, you have most of the benefit. If it lives in six dashboards, no product will save you. Check dbt's documentation for the current state of the semantic layer before adopting it, and Chapter 16 for how BI tools consume a mart.

---
## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Hard-coded table names instead of `ref` | Models build in the wrong order; the lineage graph is wrong | `{{ ref(...) }}` and `{{ source(...) }}`, always |
| `database:` pinned in `sources.yml` | Works in dev, fails in every other environment | Let the target decide the database |
| Credentials in `profiles.yml` in Git | A warehouse password in the repository forever | Environment variables or a secrets manager |
| Models that duplicate a business rule | Two dashboards, two revenue numbers | One macro, refed everywhere |
| Joins in staging that change the grain | Row counts inflate downstream and nobody knows where | Keep staging one-row-per-source-row; join in marts |
| No tests on the grain | Duplicate keys reach the fact table | `unique` and `not_null` on every model's key |
| Tests only on shapes, never on numbers | Everything passes while the total is wrong | A reconciliation test against the source |
| `dbt run` on a schedule instead of `dbt build` | Bad data ships because tests ran after, or not at all | `dbt build`, which stops the branch on failure |
| Ignoring a failing test for a few days | The test gets deleted, and the trust with it | Fix or explicitly change the rule, in a reviewed pull request |
| Everything materialized as a table | Slow builds, warehouse bills | Views for staging, tables for marts, incremental for the big ones |
| Incremental models never fully refreshed | Old rows built by old logic | Scheduled `--full-refresh`, and after any logic change |
| An incremental filter with no lookback | Late-arriving rows never appear | A few days of overlap plus `delete+insert` on a unique key |
| Snapshot pointed at a changing source path | History silently lost | Treat snapshot tables as irreplaceable |
| Documentation written in a wiki | Stale within a month | Descriptions in the YAML beside the model |
| Jinja loops generating clever SQL | Nobody can debug it, including you in March | Write the SQL out; save Jinja for repetition that is truly mechanical |
| No CI | Broken models found in production | Build and test on every pull request |
| One enormous mart model | Impossible to test or review | Split into intermediate models; views are free |

---

## In the real world: the two dashboards that disagreed

Anita's dashboard says December revenue was ₹4,39,824. The finance pack says ₹4,47,000. The gap is ₹7,176 and nobody can explain it, so both numbers stop being used and the argument is settled by whoever speaks last in the meeting.

Meera spends a morning on it. The dashboard reads Chapter 13's `sales_lines` view, which excludes cancelled orders. The finance pack reads a spreadsheet built from a different export, which includes them. Neither is wrong: they are answers to different questions, and nobody wrote either question down.

The fix isn't a better argument, it's a place for the answer to live. Over two weeks she builds the dbt project in this chapter:

- **`net_revenue` becomes a macro.** One definition, used by staging and by the reconciliation test.
- **`fct_sales_line` states its grain** in its description: one non-cancelled order line. Cancelled orders keep their own model, so the finance question has an answer too, and the two differ by a number anyone can query.
- **The reconciliation test** compares the fact total to the source on every build, so drift is caught the morning it appears, not in a meeting.
- **The lineage graph** shows the dashboard reading `fct_sales_line`, and `fct_sales_line` reading `stg_order_items`, and that reading the ERP's `order_items`. The chain is on a page.
- **Everything runs in CI** on every pull request, so changing the revenue rule is a reviewed decision with a name and a date attached.

Three months later the ERP team renames a column in `order_items`. The nightly build fails at 03:14 with a clear message, one staging model is changed and reviewed the next morning, and nothing downstream needed touching. Before dbt, that rename would have surfaced as a blank dashboard tile at 9 a.m., traced by hand over a day.

**What Meera tells Anita:** *"The two numbers were answering different questions, and now both questions have a model with its definition written down. The dashboard will keep matching finance, because a test checks it every night and the build fails if it stops."*

Notice that dbt didn't settle the argument. Writing the definition down did. dbt made writing it down the cheapest option, and kept it honest afterwards.

---

## Project: a tested mart that feeds a dashboard

**Goal:** a dbt project someone else could clone, build, and trust, ending in a mart a BI tool reads.

### Tools you'll need

Versions used for this chapter, checked in September 2026:

- **dbt Core 1.12.5** with **dbt-postgres 1.11.0**, installed with `uv add dbt-core dbt-postgres`. dbt releases often: check `dbt --version` against the documentation, and re-read the release notes before upgrading a project.
- **PostgreSQL 16**, holding `riverstone_2025` and `riverstone_perf`.
- **SQLFluff 4.3.0** with **sqlfluff-templater-dbt** (the templater is a separate package, and forgetting it produces a confusing error).
- **Git** (Chapter 26) and a CI service; the example is GitHub Actions.
- **Adapters** for other warehouses: `dbt-snowflake`, `dbt-bigquery`, `dbt-databricks`, `dbt-redshift`, `dbt-duckdb`, `dbt-sqlserver`. The project changes very little between them; the SQL dialect does.
- **Packages** worth knowing: `dbt_utils` (macros and extra tests), `dbt_expectations` (a larger test catalog), `codegen` (generates boilerplate YAML from your warehouse), `elementary` (observability, Chapter 47).
- **Python 3.14**, which `uv` picked for the `analytics` environment (Chapter 17's recommendation).
- **Companion files** in `ch32/`: the complete `riverstone_dbt` project, including its CI workflow and `.sqlfluff`; `setup_raw_crm.sql` (section 32.3); and `pyproject.toml` with `requirements-pinned.txt`, the exact versions every output in this chapter came from.

**Option A: your own warehouse.** Pick one report that matters and rebuild its inputs as a dbt project. Work against a development schema, never production, and keep credentials in environment variables.

**Option B: Riverstone.** Build the project in this chapter from an empty folder, without copying the companion files, then compare.

**Steps:**

1. **Set it up**: `dbt init`, a `profiles.yml` reading secrets from the environment, `dbt debug` passing, and the whole thing in Git with `target/` and `.env` ignored.
2. **Declare your sources**, with `unique` and `not_null` on their keys, and `dbt source freshness` configured for at least one.
3. **Build staging models**, one per source table, materialized as views.
4. **Build the marts**: at least one fact table with a grain stated in its description, and two dimensions.
5. **Test it**: grain tests on every model, `relationships` on every key in the fact table, `accepted_values` on one category, and one **reconciliation test** against the source.
6. **Break something on purpose** and confirm the build fails and the message tells you where.
7. **Add a macro** for one business rule, and use it in at least two places.
8. **Add a snapshot** for a dimension that changes, and prove it captures a change.
9. **Make one model incremental** and time a full refresh against an incremental run.
10. **Document it**: descriptions for every model and for columns whose meaning isn't obvious. Generate the docs and read your own lineage graph.
11. **Add CI** that lints and builds on every pull request, and open one pull request that fails on purpose.
12. **Point a BI tool at the mart** (Chapter 16) and confirm the numbers match your reconciliation.

**Deliverables:** the repository, the docs site (a screenshot of the lineage graph is fine), the output of a passing `dbt build` and of a failing one, and a half-page note on which tests you chose and why.

**Stretch goals:**

- Add `dbt_utils` and replace one hand-written test with `expression_is_true` or `equal_rowcount`.
- Add a second target and prove the same models build against both.
- Convert the fact table to incremental with a three-day lookback, and write a test that compares it with a full recomputation.
- Add `dbt build --select state:modified+` to CI so only changed models rebuild.

---

## Recap

- **Analytics engineering** brings software habits (version control, tests, review, documentation) to SQL transformation. **ELT** put that transformation inside the warehouse, and **dbt** is the tool most teams use for it.
- A **model** is one `SELECT` in a file. **`source`** declares raw tables; **`ref`** connects models, resolves names per environment, and **builds the dependency graph** dbt runs in order.
- Projects layer into **staging** (one model per source table, views, grain preserved), optional **intermediate**, and **marts** (facts and dimensions, tables).
- **Materializations**: view, table, incremental, ephemeral. Views for staging, tables for marts, incremental when a rebuild hurts.
- **Tests** return no rows when they pass. `unique`, `not_null`, `relationships`, and `accepted_values` cover shapes; a **singular test** reconciling to the source covers the numbers. **`dbt build`** runs models and tests together and stops the branch when one fails.
- **Documentation** and the **lineage graph** are generated from the YAML and the `ref` calls, so they can't drift.
- **Snapshots** keep type 2 history from a source that overwrites, but only from the day they start running.
- **Incremental models** process new rows only: 2.19 seconds against 0.55 on 1.9 million lines here. Use a **lookback window**, a **unique key**, and a scheduled **full refresh**.
- **Jinja** turns dbt's files into templates: `{{ }}` for values, `{% %}` for instructions, `{# #}` for comments. **Macros** define a business rule once. **Packages** such as `dbt_utils` bring proven macros and tests.
- **SQLFluff** lints; **CI** builds and tests every pull request; something else (cron, an orchestrator, or dbt Cloud) runs dbt on a schedule.
- dbt transforms; it does not extract, load, schedule, or visualize.

---

## Key terms

analytics engineering · ETL · ELT · dbt Core · dbt Cloud · adapter · profile · target · `dbt_project.yml` · `profiles.yml` · `env_var` · model · source · `ref` · `source()` · `config()` · Jinja · compiled SQL · DAG (dependency graph) · staging layer · intermediate layer · mart · materialization · view · table · incremental model · ephemeral model · `is_incremental()` · `{{ this }}` · incremental strategy · lookback window · full refresh · generic test · singular test · `unique` · `not_null` · `relationships` · `accepted_values` · source freshness · `dbt build` · `dbt run` · `dbt test` · node selection (`+`, `state:modified`) · snapshot · `dbt_valid_from` · `dbt_valid_to` · `dbt_scd_id` · check strategy · timestamp strategy · macro · package · `dbt_utils` · docs site · lineage graph · SQLFluff · templater · linting · continuous integration · service container · repository secret · semantic layer · MetricFlow

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can explain ELT, and why transformation moved into the warehouse.
- [ ] I can set up a dbt project whose credentials never appear in the code.
- [ ] Every model of mine uses `ref` and `source`, and I can explain both jobs `ref` does.
- [ ] I lay projects out in staging and marts, and I keep the grain in staging.
- [ ] I choose materializations deliberately and can say what each costs.
- [ ] My models carry grain tests, relationship tests, and at least one reconciliation.
- [ ] I run `dbt build`, not `dbt run`, on a schedule, and I know why.
- [ ] I can read a failing test's output and get to the offending rows.
- [ ] I write descriptions beside the models and can navigate my own lineage graph.
- [ ] I can keep type 2 history with a snapshot, and I know what a snapshot can't recover.
- [ ] I can make a model incremental, with a lookback, and measure what it saves.
- [ ] I write a business rule once, as a macro, and lint and build on every pull request.

---

## Exercises

Work in the `riverstone_dbt` project, against the `dev` target. Predict each answer before you run it.

### Warm-up

1. Run `dbt ls` and `dbt ls --select staging`. What do the outputs tell you about how models are addressed?
2. Compile `fct_sales_line` and read `target/compiled/.../fct_sales_line.sql`. Which parts were written by you, and which by dbt?
3. Run `dbt build --select stg_orders+` and explain, from the output, what the `+` did.
4. Query `dbt_dev_marts.fct_daily_sales`. How many rows does it have, and why that number?

### Core

5. Add a `stg_employees` staging model, with `unique` and `not_null` tests on `employee_id`, and change `dim_sales_rep` to ref it instead of the source. Does the lineage graph change?
6. Add an `accepted_values` test on `stg_orders.status`, run it, then add a new status to the source data and watch it fail.
7. Write a singular test asserting that no order line has a negative `net_revenue`, and one asserting that every non-cancelled order in `stg_orders` has at least one line in `fct_sales_line`.
8. Change the `net_revenue` macro to round to zero decimal places. Which models change, and which test catches the consequence?
9. Materialize `dim_date` as a view instead of a table, rebuild, and compare the run output. When would that be the right choice?
10. Add descriptions for every column of `fct_sales_line`, regenerate the docs, and check the column-level lineage.

### Stretch

11. Write a model `int_orders_with_totals` as an **ephemeral** materialization, use it in `fct_daily_sales`, and look at the compiled SQL. Where did the model go?
12. Convert `fct_sales_line` to incremental, keyed on `order_item_id`, with a three-day lookback on `order_date`. Then write a test that compares its total against a full recomputation.
13. Add `dbt_utils` to the project and replace the reconciliation test with `dbt_utils.equal_rowcount` plus an expression test. Which version would you rather maintain?
14. Section 32.11's `mart_sales_monthly` pivots revenue by category with a Jinja loop. Write the same model without Jinja, as `mart_sales_monthly_plain`, and compare the two compiled files. Which would you put in the repository?
15. Configure `dbt source freshness` on `erp.orders` with a warn-after of 24 hours and an error-after of 48, and make it fail.

### Think about it (no code needed)

16. A colleague wants the dashboard to read `stg_order_items` directly, "because it has everything and it's fresher". Give two reasons to say no, and one case where they'd be right.
17. Your project has 300 models and `dbt build` takes 40 minutes. List four things you'd look at, in order.
18. When would you *not* use dbt for a transformation?

---

## Answers

**1.** `dbt ls` lists every node in the project: sources, models, snapshots, and tests, one per line: models as `project.folder.name` (`riverstone_dbt.staging.stg_orders`), sources as `source:riverstone_dbt.erp.orders`. `dbt ls --select staging` lists only what's under `models/staging`. That naming is how **node selection** works everywhere: `--select stg_orders` (one model), `stg_orders+` (it and everything downstream), `+fct_sales_line` (it and everything upstream), `tag:nightly`, `source:erp+`, `state:modified+`. Selection is the skill that makes a 300-model project workable.

**2.** Everything between `select` and the final `from` is yours. dbt replaced `{{ source('erp', 'order_items') }}` with the fully qualified table name, and expanded the `net_revenue` macro into arithmetic. Nothing else was added. The compiled file is your query exactly as the database will run it; when the model is built, dbt wraps it in `create table ... as` and saves that version in `target/run/`, which is why reading it settles most "why is this model doing that?" questions.

**3.** The `+` selects the model **and everything downstream of it**: `stg_orders`, then the marts that ref it, then the tests on all of them. The output shows the fact models and their tests running after the staging view. Use it before opening a pull request: it proves that a change to one model doesn't break anything below it. `+stg_orders` (the plus in front) would select its upstream instead, which is what you want when a source is misbehaving.

**4.**

<!-- db: riverstone_2025 -->

<!-- run: pg -->
```sql
SELECT COUNT(*) AS days,
       MIN(order_date) AS first_day,
       MAX(order_date) AS last_day,
       ROUND(SUM(net_revenue)) AS net_revenue
FROM dbt_dev_marts.fct_daily_sales;
```

```
 days | first_day  |  last_day  | net_revenue
------+------------+------------+-------------
  132 | 2025-01-02 | 2025-12-23 |     4335471
(1 row)
```

One row per day that had at least one non-cancelled order line, which is fewer than 365 because these key accounts don't order every day, and the last order in the source is dated 23 December (Chapter 13's date-spine problem). The total matches `fct_sales_line`, as it must: both come from the same staging models. If you need a row for every calendar day, join to `dim_date` rather than changing this model.

**5.** The model is short:

<!-- run: none -->
```sql
-- models/staging/stg_employees.sql
select
    employee_id,
    employee_name,
    job_title,
    manager_id
from {{ source('erp', 'employees') }}
```

with tests in `models/staging/schema.yml`, and `dim_sales_rep` changed to `from {{ ref('stg_employees') }}`. The lineage graph gains a node: `erp.employees → stg_employees → dim_sales_rep` instead of the source feeding the dimension directly. That's the point of the staging layer: one place where the ERP's column names are translated, so a rename upstream is a one-file change.

**6.**

<!-- run: none -->
```yaml
# in models/staging/schema.yml, under stg_orders
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['Delivered', 'Shipped', 'Pending', 'Cancelled']
```

It passes. Now insert an order with status `'Returned'` into the source and run `dbt test --select stg_orders`: the test fails with the count of offending rows and the path to the compiled query, which lists the unexpected value. This is the test that catches a source system quietly adding a category, which otherwise shows up as a dashboard whose segments no longer add to the total.

**7.**

<!-- run: none -->
```sql
-- tests/assert_no_negative_revenue.sql
select order_item_id, net_revenue
from {{ ref('fct_sales_line') }}
where net_revenue < 0
```

<!-- run: none -->
```sql
-- tests/assert_every_order_has_lines.sql
select o.order_id
from {{ ref('stg_orders') }} as o
left join {{ ref('fct_sales_line') }} as f on f.order_id = o.order_id
where o.is_counted and f.order_id is null
```

The second one is worth thinking about before you write it: it will fail for any non-cancelled order whose lines were dropped by a join in the fact model, which is exactly the bug you want to know about, and it's the kind of test that should have caught Chapter 28's point-in-time join problem.

**8.** Every model that uses the macro changes: `stg_order_items` (and therefore `fct_sales_line` and `fct_daily_sales`), plus the reconciliation test, which uses the same macro and so moves with it. That last part is a trap worth seeing: a test written with the same macro as the model **cannot catch a change to the macro**, because both sides move together. A reconciliation test is stronger when its other side comes from somewhere the macro doesn't touch, such as a figure finance publishes or a hard-coded expected total for a closed period.

**9.**

<!-- run: none -->
```
# terminal, in riverstone_dbt, after changing 'table' to 'view' in dim_date's config line
$ dbt run --select dim_date
19:19:05  1 of 1 START sql view model dbt_dev_marts.dim_date ............................. [RUN]
19:19:05  1 of 1 OK created sql view model dbt_dev_marts.dim_date ........................ [CREATE VIEW in 0.10s]
```

*(Trimmed: the header and summary lines.)*

The run is quicker because nothing is computed or stored, and every query against `dim_date` now runs `generate_series` again. For 365 rows that's free, so a view is a reasonable choice. Make it a table when the dimension is large, when it's joined in every report, or when the warehouse charges for compute rather than storage: then paying once per build beats paying once per query.

**10.** Descriptions go in `models/marts/schema.yml` under each column. After `dbt docs generate`, the site shows them beside the column, along with the tests attached to it, and the column-level lineage where the adapter supports it. The habit that pays: describe the column's **meaning and unit**, not its name. `net_revenue`: "line value after discount, before tax, in rupees; excludes cancelled orders" is worth writing. "The net revenue" is not.

**11.** With `{{ config(materialized='ephemeral') }}`, dbt creates nothing in the database. The model's SQL is inlined into every model that refs it, as a CTE at the top of the compiled file. Check `target/compiled/`: `fct_daily_sales.sql` now starts with `with __dbt__cte__int_orders_with_totals as (...)`, the model's SQL under a name dbt made up. Ephemeral models keep intermediate steps out of the warehouse, which is tidy, but they can't be queried, can't be tested on their own, and get recomputed in every model that uses them. Use them for small steps used once or twice.

**12.** The model gains a config line at the top and a filter at the bottom. The filter begins with `and`, because the model already has a `where`, and it reads `order_date`, which is why section 32.5 kept that column in the fact table:

<!-- run: none -->
```sql
{{ config(materialized='incremental', unique_key='order_item_id', incremental_strategy='delete+insert') }}
-- ... the select, joins and where o.is_counted, unchanged ...
{% if is_incremental() %}
  and o.order_date >= (select max(order_date) - interval '3 days' from {{ this }})
{% endif %}
```

The existing reconciliation test already compares grand totals, so the new test compares **each day**, which catches drift that a grand total can hide (one day too high, another too low):

<!-- run: none -->
```sql
-- tests/assert_incremental_matches_full.sql
-- Every day's total in the incremental fact must match a full recomputation from the source.
-- Returns one row per day that has drifted.
with incremental_days as (
    select order_date, sum(net_revenue) as total
    from {{ ref('fct_sales_line') }}
    group by order_date
),
full_days as (
    select o.order_date,
           sum({{ net_revenue('oi.quantity', 'oi.unit_price', 'oi.discount_pct') }}) as total
    from {{ source('erp', 'order_items') }} as oi
    join {{ source('erp', 'orders') }} as o on o.order_id = oi.order_id
    where o.status <> 'Cancelled'
    group by o.order_date
)
select f.order_date, i.total as incremental_total, f.total as full_total
from full_days as f
left join incremental_days as i on i.order_date = f.order_date
where i.total is null or abs(i.total - f.total) > 0.01
```

The `left join` and `i.total is null` also catch a day missing from the fact altogether. Run it after a few incremental runs, not just after a full refresh: drift is the failure mode you're testing for. (Tested: after a `--full-refresh`, each incremental run deleted and re-inserted the 4 lines of the last three days, and the test passed every time.)

**13.** `dbt_utils.equal_rowcount` compares two models' row counts, and `dbt_utils.expression_is_true` checks a condition per row. They're shorter to write and consistent across projects. The hand-written reconciliation is more specific: it compares a *total* against the source, to the paisa, which is the thing finance cares about. In practice, keep both: package tests for the mechanical checks, hand-written ones for the business rules that would actually cause an argument.

**14.** The Jinja version is shorter and adapts when a category is added (more so if the list comes from `dbt_utils.get_column_values`). The written-out version is readable by anyone, lints cleanly, and can be pasted into a query window to debug. For four categories that change once a decade, put the written-out version in the repository. For forty categories that change monthly, use Jinja, and leave a comment saying what it generates.

**15.** In `sources.yml`:

<!-- run: none -->
```yaml
      - name: orders
        loaded_at_field: order_date::timestamp
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 48, period: hour}
```

`dbt source freshness` compares the newest `loaded_at_field` value with now. Against `riverstone_2025`, whose latest order is dated 23 December 2025, it errors immediately (`ERROR STALE`), which is the point of the exercise: **freshness catches the load that didn't run**, which is the single most common cause of a wrong dashboard, and no model test will ever notice it. In production, point it at a genuine load timestamp rather than a business date.

**16.** Two reasons to say no: staging models aren't guaranteed stable (they're an implementation detail that gets renamed and restructured), and they don't have the marts' joins, tests, or the grain that reports depend on, so two dashboards reading staging will re-implement the same joins differently. The case where they'd be right: an analyst exploring, in a scratch query, to decide what a mart should contain. Exploration reads whatever it likes; production reports read marts.

**17.** In order: (1) **Which models are slow?** `target/run_results.json` has a duration per node, and a handful of models usually dominate. (2) **Should the slow ones be incremental?** A full rebuild of a large fact table is the usual culprit. (3) **Are there tables that should be views, or views that should be tables?** Both mistakes cost time. (4) **Is the graph too wide or too deep?** Threads help only if the DAG allows parallelism, and a chain of twelve dependent models can't be parallelized at all. After those, look at warehouse-side things: clustering, partitioning, and the warehouse size (Chapter 49).

**18.** When the transformation isn't SQL and doesn't want to be: machine-learning features that need Python, or parsing awkward files. When the data isn't in the warehouse yet: dbt can't fetch it. When you need row-by-row processing or true real-time results: dbt runs batches. When the project is one query that one person runs occasionally: a scheduled script is less machinery. And when the team has no version control or review habit, dbt on its own won't create one, though adopting it is a reasonable excuse to start.

---

## Where this leads

- **Chapter 16, Business Intelligence with Power BI,** reads the mart this chapter builds.
- **Chapter 28, Advanced SQL, Performance & Data Modeling,** is the modeling this chapter automates; its grain and SCD lessons are the reason the tests here look the way they do.
- **Chapter 46, Pipelines & Orchestration,** gets the data into the warehouse and runs dbt on a schedule alongside everything else.
- **Chapter 47, Data Quality, Observability & Contracts,** goes further than tests: freshness, anomaly detection, contracts, and who gets paged.
- **Chapter 49, Storage, Warehouses & Lakehouses,** is where these models run at scale, and where materialization choices become money.
- **Chapter 62, Data Architecture Patterns,** puts dbt in the wider picture, including when a team shouldn't use it.
- **Chapter 71, SQL Question Bank,** and **Chapter 77** include dbt and analytics-engineering questions.
