with dates as (
    select
        generate_series(
            (select min(message_date) from {{ ref('stg_telegram_messages') }}),
            (select max(message_date) from {{ ref('stg_telegram_messages') }}),
            interval '1 day'
        )::date as date_day
)
select
    date_day as date_id,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day,
    extract(dow from date_day) as day_of_week,
    to_char(date_day, 'Day') as day_name
from dates