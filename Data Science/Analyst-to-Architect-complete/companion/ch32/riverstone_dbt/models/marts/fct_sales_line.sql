-- Grain: one non-cancelled order line.
select
    oi.order_item_id,
    oi.order_id,
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
