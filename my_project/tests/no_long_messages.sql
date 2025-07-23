select *
from {{ ref('fct_messages') }}
where message_length > 4096