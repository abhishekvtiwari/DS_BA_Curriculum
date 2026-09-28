# riverstone_dbt: Chapter 32's finished project

The dbt project that Chapter 32 builds from nothing, as it stands at the end of the chapter.
Tested with dbt Core 1.12.5, dbt-postgres 1.11.0, SQLFluff 4.3.0 and Python 3.14 on PostgreSQL 16
(exact versions of everything: `../requirements-pinned.txt`).

To run it (section 32.2 explains each step):

1. In the folder above this one: `uv sync` (or `uv add dbt-core dbt-postgres` in your own folder), then
   `source .venv/bin/activate`.
2. Once per database: run `../setup_raw_crm.sql` against `riverstone_2025` (section 32.3). It creates the
   `raw_crm.customers` table that stands in for the CRM's nightly extract.
3. In this folder: create `.env` with `export RIVERSTONE_PASSWORD='your-password'`, `chmod 600 .env`,
   `source .env`, then `dbt debug` and `dbt build`.

`profiles.yml` is kept here and holds no secrets; dbt finds it because you run dbt from this folder.
`models/marts/fct_sales_line.sql` is kept exactly as section 32.5 prints it, so `sqlfluff lint` reports
the ten violations section 32.12 shows.
