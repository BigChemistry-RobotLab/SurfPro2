SELECT
    COUNT(*)
FROM measurements
WHERE ABS(temperature - 25.0) <= 1.0;
