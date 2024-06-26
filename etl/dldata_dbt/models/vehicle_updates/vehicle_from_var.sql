SELECT
    vehicle,
    trip_id,
    departure_delay,
    departure_stop_id,
    "timestamp"
FROM
    {{ source('public', 'vehicle_updates') }}
WHERE
    vehicle::integer = {{ var('vehicle_id') }}
ORDER BY
    "timestamp" DESC