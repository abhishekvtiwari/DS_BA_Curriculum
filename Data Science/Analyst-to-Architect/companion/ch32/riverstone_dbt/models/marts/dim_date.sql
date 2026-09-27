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
