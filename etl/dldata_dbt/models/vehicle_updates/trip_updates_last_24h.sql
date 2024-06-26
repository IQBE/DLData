WITH source_data AS (
    SELECT
        COUNT(*) AS amount_of_trip_updates
    FROM
        {{ source('public', 'vehicle_updates') }}
    WHERE
        "timestamp" > NOW() - INTERVAL '1 DAY'
)
SELECT
    amount_of_trip_updates
FROM
    source_data
