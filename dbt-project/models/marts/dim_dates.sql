{{ config(materialized='table', schema='marts') }}

WITH date_range AS (
    SELECT generate_series(
        (SELECT MIN(CAST(message_date AS DATE)) FROM {{ ref('stg_telegram_messages') }}),
        (SELECT MAX(CAST(message_date AS DATE)) FROM {{ ref('stg_telegram_messages') }}),
        INTERVAL '1 day'
    ) AS date
)
SELECT
    ROW_NUMBER() OVER () AS date_id,
    date,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(DOW FROM date) AS day_of_week
FROM date_range