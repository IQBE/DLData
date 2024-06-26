SELECT
    date_trunc ('day', "timestamp") AS DATE,
    AVG(departure_delay) AS avg_delay
FROM
    {{ source('public', 'vehicle_updates') }}
GROUP BY
    date_trunc ('day', "timestamp")