-- finds the earliest publication of a value in the database
WITH RECURSIVE chain AS (
    SELECT
        m.measurement_id,
        m.compound_id,
        c.source_id,
        c.cited_id,
        0 AS depth
    FROM measurements m
    JOIN citations c ON m.citation_id = c.citation_id
    WHERE m.compound_id = 696

    UNION ALL

    SELECT
        ch.measurement_id,
        ch.compound_id,
        c2.source_id,
        c2.cited_id,
        ch.depth + 1
    FROM chain ch
    JOIN citations c2 ON ch.cited_id = c2.source_id
)
, last_step AS (
    SELECT
        measurement_id,
        source_id,
        cited_id,
        depth,
        ROW_NUMBER() OVER (
            PARTITION BY measurement_id
            ORDER BY depth DESC
        ) AS rn
    FROM chain
)
SELECT
    a.measurement_id,
    l.keyid AS recorded_source,
    l2.keyid AS cited_source,
    m.value, m.temperature, m.property_type_id
FROM last_step a
LEFT JOIN literature l ON l.literature_id = a.source_id
LEFT JOIN literature l2 ON l2.literature_id = a.cited_id
LEFT JOIN measurements m ON m.measurement_id = a.measurement_id
WHERE rn < 2 AND m.property_type_id = 1 AND ABS(m.temperature - 25.0) < 0.1
ORDER BY cited_source;
