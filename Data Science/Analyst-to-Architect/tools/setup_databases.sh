#!/usr/bin/env bash
# setup_databases.sh - (re)load every Riverstone practice database used by the verification tools.
# Usage:  bash setup_databases.sh /path/to/companion
# Creates in PostgreSQL AND MySQL: riverstone (mini, Q1 2026) and riverstone_2025 (one year of 2025),
# plus the sales_lines view from Chapter 13, section 13.2, in both databases.
# Expects: PostgreSQL 16+ with a 'postgres' superuser; MySQL 8.0+ with root access from this shell.
set -euo pipefail
C="${1:-../companion}"
if [ "$(id -u)" = "0" ]; then PG() { su postgres -c "psql -X -q -v ON_ERROR_STOP=1 $*"; }; else PG() { psql -X -q -v ON_ERROR_STOP=1 -U postgres "$@"; }; fi

VIEW="CREATE VIEW sales_lines AS
SELECT o.order_id, o.order_date, o.customer_id, o.sales_rep_id, o.status,
       oi.product_id, p.category, oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * p.unit_cost AS product_cost
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled';"

for DB in riverstone riverstone_2025; do
  PG -d postgres -c "\"DROP DATABASE IF EXISTS $DB\"" >/dev/null 2>&1 || true
  PG -d postgres -c "\"CREATE DATABASE $DB\""
done
cp "$C/riverstone_setup_mini.sql" /tmp/rs_mini.sql 2>/dev/null || cp "$C/riverstone_setup.sql" /tmp/rs_mini.sql
cp "$C/riverstone_2025_setup.sql" /tmp/rs_2025.sql
chmod 644 /tmp/rs_mini.sql /tmp/rs_2025.sql
PG -d riverstone -f /tmp/rs_mini.sql
PG -d riverstone_2025 -f /tmp/rs_2025.sql
printf '%s\n' "$VIEW" > /tmp/rs_view.sql; chmod 644 /tmp/rs_view.sql
PG -d riverstone -f /tmp/rs_view.sql
PG -d riverstone_2025 -f /tmp/rs_view.sql

mysql -uroot < "$C/mysql/riverstone_setup_mysql.sql"
mysql -uroot < "$C/mysql/riverstone_2025_setup_mysql.sql"
mysql -uroot riverstone < /tmp/rs_view.sql
mysql -uroot riverstone_2025 < /tmp/rs_view.sql
# Chapter 13's calendar tables (calendar_months, calendar_days) in the one-year database.
cp "$C/ch13/calendar_tables_postgresql.sql" "$C/ch13/calendar_tables_mysql.sql" /tmp/ && chmod 644 /tmp/calendar_tables_*.sql
PG -d riverstone_2025 -f /tmp/calendar_tables_postgresql.sql
mysql -uroot riverstone_2025 < /tmp/calendar_tables_mysql.sql
# Chapter 28 add-ons: the HRMS staff table, the bill of materials, the ERP audit log and the dw star schema.
# Skipped without complaint if the Part III companion files aren't present.
if [ -f "$C/ch28/ch28_2025_addons.sql" ]; then
  cp "$C/ch28/ch28_2025_addons.sql" "$C/ch28/ch28_star_schema.sql" /tmp/ && chmod 644 /tmp/ch28_*.sql
  PG -d riverstone_2025 -f /tmp/ch28_2025_addons.sql
  PG -d riverstone_2025 -f /tmp/ch28_star_schema.sql
  echo "Chapter 28 add-ons and star schema loaded into riverstone_2025."
fi

# riverstone_perf (Chapter 28's volume dataset, about 200 MB) is NOT loaded here: generate it with
#   cd companion/ch28 && python3 generate_riverstone_perf.py
#   createdb riverstone_perf && psql -d riverstone_perf -f perf_data/load_postgresql.sql
# riverstone_full (Chapters 14 onward) is loaded from companion/full/riverstone_full_setup_postgresql.sql.

echo "PostgreSQL and MySQL practice databases loaded."
