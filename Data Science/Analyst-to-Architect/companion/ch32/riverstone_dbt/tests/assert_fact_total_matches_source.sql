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
