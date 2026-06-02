WITH first_reports_of_values AS (
    SELECT
        m.compound_id,
        m.property_type_id,
        m.value,
        m.temperature,
        ROUND(COALESCE(m.temperature, -9999), 0) AS rounded_temp,
        l.date AS publication_year,
        l.doi,
        l.keyid,
        ROW_NUMBER() OVER (
            PARTITION BY
                m.compound_id,
                m.property_type_id,
                m.value,
                ROUND(COALESCE(m.temperature, -9999), 0)
            ORDER BY l.date ASC, m.created_at ASC, m.measurement_id ASC
        ) AS rn
    FROM measurements m
    JOIN citations c ON m.citation_id = c.citation_id
    JOIN literature l ON c.source_id = l.literature_id
),
independent_measurements_only AS (
    SELECT
        compound_id,
        property_type_id,
        value,
        temperature,
        rounded_temp,
        publication_year,
        doi,
        keyid,
        COUNT(*) OVER (
            PARTITION BY
                compound_id,
                property_type_id,
                rounded_temp
        ) AS total_independent_values
    FROM first_reports_of_values
    WHERE rn = 1
)
SELECT
    comp.SMILES,
    p.name AS property_name,
    im.temperature AS exact_temperature,
    im.value,
    im.publication_year,
    im.keyid
FROM independent_measurements_only im
JOIN property_types p ON im.property_type_id = p.property_type_id
JOIN compounds comp ON im.compound_id = comp.compound_id
WHERE im.total_independent_values > 1
ORDER BY
    im.compound_id ASC,
    p.name ASC,
    im.rounded_temp ASC,
    im.publication_year ASC;
