-- One row per product. The ERP's unit_price is the list price, so staging gives it that name.
select
    product_id,
    product_name,
    category,
    unit_price as list_price,
    unit_cost
from {{ source('erp', 'products') }}
