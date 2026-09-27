select
    employee_id as sales_rep_key,
    employee_id,
    employee_name as rep_name,
    job_title
from {{ source('erp', 'employees') }}
union all
select -1, null, 'No rep recorded', 'Unknown'
