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
