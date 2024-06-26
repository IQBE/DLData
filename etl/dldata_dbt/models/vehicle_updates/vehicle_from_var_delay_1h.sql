SELECT
    vehicle,
    trip_id,
    departure_delay,
    departure_stop_id,
    "timestamp"
FROM
    {{ ref('vehicle_from_var') }}
WHERE
    departure_delay >= 60