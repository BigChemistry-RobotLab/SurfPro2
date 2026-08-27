-- Retrieve data erporting on the temperature dependence of all properties in the database
-- where possible (measurements at > 2 temperatures)
WITH temperature_series AS (
    SELECT
        m.compound_id,
        m.property_type_id
    FROM measurements m
    LEFT JOIN citations cit USING(citation_id)
    LEFT JOIN measurement_flags mf USING(measurement_id)
    WHERE
        cit.cited_id IS NULL
        AND mf.data_flag_id IS NULL
        AND m.temperature IS NOT NULL
    GROUP BY
        m.compound_id,
        m.property_type_id
    HAVING
        COUNT(DISTINCT m.temperature) >= 2
)

SELECT
    c.compound_id,
    c.SMILES,
    c.Surfactant_Type,
    pt.name AS property,
    m.temperature,
    m.value,
    u.name AS unit,
    u.latex_math_text AS latex_unit,
    pt.latex_math_text,
    meth.name AS method
FROM measurements m
JOIN temperature_series ts
    ON ts.compound_id = m.compound_id
    AND ts.property_type_id = m.property_type_id
JOIN compounds c
    ON c.compound_id = m.compound_id
JOIN property_types pt
    ON pt.property_type_id = m.property_type_id
LEFT JOIN methods meth
    ON meth.method_id = m.method_id
LEFT JOIN citations cit
    USING(citation_id)
LEFT JOIN measurement_flags mf
    USING(measurement_id)
LEFT JOIN units u
    USING(unit_id)
WHERE
    cit.cited_id IS NULL
    AND mf.data_flag_id IS NULL
    AND m.temperature IS NOT NULL
ORDER BY
    pt.name,
    c.compound_id,
    m.temperature;
