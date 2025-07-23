with raw as (
    select
        id,
        channel,
        message_json
    from {{ source('telegram', 'raw_telegram_messages') }}
)

select
    id,
    channel,
    (message_json->>'id')::bigint as message_id,
    (message_json->>'date')::timestamp as message_date,
    (message_json->>'message') as message_text,
    (message_json->>'from_id') as from_id,
    (message_json->>'reply_to_msg_id')::bigint as reply_to_msg_id,
    (message_json->>'views')::int as views,
    (message_json->>'forwards')::int as forwards,
    (message_json->>'edit_date')::timestamp as edit_date,
    (message_json->>'post_author') as post_author,
    message_json
from raw