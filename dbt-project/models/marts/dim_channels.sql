{{ config(materialized='table', schema='marts') }}

SELECT DISTINCT
    channel AS channel_name,
    ROW_NUMBER() OVER () AS channel_id
FROM {{ ref('stg_telegram_messages') }}