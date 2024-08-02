-- models/example.sql
with source as (
    select *
    from {{ ref('raw_data') }}
)

select *
from source
