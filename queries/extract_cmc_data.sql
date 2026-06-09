-- Select the earliest (first-reported) measurement for each unique (compound,
-- property, value, temperature) combination by ranking all entries
-- chronologically by publication year and insertion order, then return only
-- the first occurrence (rn = 1) for CMC measurements measured between 20–25°C,
-- including property name, units, and DOI.
WITH ranked_measurements AS (
    SELECT
        m.compound_id,
        m.property_type_id,
        m.value,
        m.temperature,
        m.unit_id,
        m.citation_id,
        c.source_id AS literature_id,
        l.date AS publication_year,
        l.doi,
        -- Rank each unique group chronologically
        ROW_NUMBER() OVER (
            PARTITION BY
                m.compound_id,
                m.property_type_id,
                m.value,
                COALESCE(m.temperature, -9999)
            ORDER BY
                l.date ASC,
                m.created_at ASC,
                m.measurement_id ASC
        ) AS rn
    FROM measurements m
    JOIN citations c ON m.citation_id = c.citation_id
    JOIN literature l ON c.source_id = l.literature_id
)
SELECT
    r.compound_id,
    p.name AS property_name,
    r.value,
    r.temperature,
    u.name AS unit_name,
    r.publication_year,
    r.doi
FROM ranked_measurements r
LEFT JOIN property_types p ON r.property_type_id = p.property_type_id
LEFT JOIN units u ON r.unit_id = u.unit_id
WHERE r.rn = 1
  AND r.temperature BETWEEN 20 AND 25
  AND p.name = 'CMC'; -- works for different properties
