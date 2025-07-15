{{ config(materialized='table', schema='marts') }}

SELECT
    d.message_id,
    c.channel_id,
    d.detected_object_class,
    d.confidence_score
FROM raw.image_detections d
JOIN {{ ref('dim_channels') }} c ON d.channel = c.channel_name