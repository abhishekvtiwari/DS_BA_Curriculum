# riverstone-report

Riverstone's monthly sales report: reads one month from the `riverstone_2025` database, checks it,
summarizes it, and writes an Excel workbook. Built in Chapter 29 of *Analyst to Architect*.

## Install

    uv sync --locked            # add --no-dev on a server

## Run

    export RIVERSTONE_DATABASE_URL="postgresql+psycopg://postgres:YOUR_PASSWORD@localhost/riverstone_2025"
    uv run riverstone-report --month 2025-12

Or keep the settings in a `.env` file (never committed; copy `.env.example`) and run
`uv run --env-file .env riverstone-report --month 2025-12`.

| Variable | Needed | Meaning |
|---|---|---|
| `RIVERSTONE_DATABASE_URL` | yes | SQLAlchemy URL of the database |
| `RIVERSTONE_OUTPUT_DIR` | no (default `reports`) | folder for the workbooks |

Exit code 0 means the workbook was written; 1 means the run failed, with the reason in the log.

## Test

    uv run pytest               # the database test is skipped unless RIVERSTONE_DATABASE_URL is set
    uv run mypy
