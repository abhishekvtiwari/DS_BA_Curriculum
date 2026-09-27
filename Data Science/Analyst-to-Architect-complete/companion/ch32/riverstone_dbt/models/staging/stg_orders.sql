-- One row per order, with names cleaned up and cancelled orders flagged.
select
    order_id,
    customer_id,
    sales_rep_id,
    order_date,
    status,
    status <> 'Cancelled' as is_counted
from {{ source('erp', 'orders') }}
