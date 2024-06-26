SELECT
    vehicle,
    COUNT(*) AS trips
FROM
    {{ source('public', 'vehicle_updates') }}
GROUP BY
    vehicle
ORDER BY
    trips DESC
