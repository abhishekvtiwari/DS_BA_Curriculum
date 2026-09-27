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
