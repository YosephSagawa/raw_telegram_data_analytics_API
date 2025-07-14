{{ config(materialized='table', schema='marts') }}

SELECT
    m.id AS message_id,
    c.channel_id,
    d.date_id,
    m.text,
    m.has_media,
    LENGTH(m.text) AS message_length
FROM {{ ref('stg_telegram_messages') }} m
JOIN {{ ref('dim_channels') }} c ON m.channel = c.channel_name
JOIN {{ ref('dim_dates') }} d ON CAST(m.message_date AS DATE) = d.date