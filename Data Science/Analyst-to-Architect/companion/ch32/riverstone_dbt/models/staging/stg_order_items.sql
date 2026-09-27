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
