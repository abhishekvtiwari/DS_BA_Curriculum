select
    customer_id,
    customer_name,
    city,
    segment,
    signup_date
from {{ source('erp', 'customers') }}
