select
    -- Join to fct_messages using channel and (optionally) image filename conventions
    m.message_pk as message_id,
    d.detected_object_class,
    d.confidence_score,
    d.image_path
from {{ ref('raw_image_detections') }} d
left join {{ ref('fct_messages') }} m
    on d.channel = m.channel_id
    -- Optionally, match on image filename if you store image filename in fct_messages