-- One row per month, with revenue split by product category.
{% set categories = ['Storage', 'Kitchen', 'Industrial', 'Furniture'] %}

select
    d.month_start,
    {% for category in categories %}
    sum(case when p.category = '{{ category }}' then f.net_revenue else 0 end)
        as revenue_{{ category | lower }}{{ "," if not loop.last }}
    {% endfor %}
from {{ ref('fct_sales_line') }} as f
join {{ ref('dim_product') }} as p on p.product_key = f.product_key
join {{ ref('dim_date') }} as d on d.date_key = f.date_key
group by d.month_start
