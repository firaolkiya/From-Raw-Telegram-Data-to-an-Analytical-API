select
    m.id as message_pk,
    m.channel as channel_id,
    m.message_date::date as date_id,
    m.message_id,
    m.message_text,
    length(m.message_text) as message_length,
    m.views,
    m.forwards,
    m.reply_to_msg_id,
    m.from_id,
    m.post_author,
    -- Key metric: does this message have an image?
    case
        when m.message_json->'media' is not null then true
        else false
    end as has_image
from {{ ref('stg_telegram_messages') }} m