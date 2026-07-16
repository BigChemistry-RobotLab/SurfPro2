-- Get the number of values for each property with measurements at least two
-- different temperatures
SELECT
    pt.name AS property,
    COUNT(*) AS n_compounds
FROM (
    SELECT
        compound_id,
        property_type_id
    FROM measurements
    WHERE temperature IS NOT NULL
    GROUP BY
        compound_id,
        property_type_id
    HAVING COUNT(DISTINCT temperature) >= 2
) t
JOIN property_types pt
    USING(property_type_id)
GROUP BY
    pt.name
ORDER BY
    n_compounds DESC;
