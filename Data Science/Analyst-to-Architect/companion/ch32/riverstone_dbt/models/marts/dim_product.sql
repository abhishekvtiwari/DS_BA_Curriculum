select
    product_id as product_key,
    product_id,
    product_name,
    category,
    list_price,
    unit_cost
from {{ ref('stg_products') }}
