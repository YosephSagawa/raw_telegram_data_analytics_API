{{ config(materialized='view', schema='staging') }}

SELECT
    id,
    channel,
    CAST(date AS TIMESTAMP) AS message_date,
    text,
    has_media
FROM raw.telegram_messages
WHERE text IS NOT NULL