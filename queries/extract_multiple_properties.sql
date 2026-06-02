-- with assistance from Google Gemini
WITH ranked_measurements AS (
    SELECT
        m.compound_id,
        m.property_type_id,
        m.value,
        m.temperature,
        -- Rounding here ensures we rank chronologically WITHIN the temperature bracket
        ROUND(COALESCE(m.temperature, -9999), 0) AS rounded_temp,
        m.citation_id,
        l.date AS publication_year,
        l.doi,
        -- Find the "first citation" for EVERY property per rounded temperature bracket
        ROW_NUMBER() OVER (
            PARTITION BY
                m.compound_id,
                m.property_type_id,
                ROUND(COALESCE(m.temperature, -9999), 0)
            ORDER BY l.date ASC, m.created_at ASC, m.measurement_id ASC
        ) AS rn
    FROM measurements m
    JOIN citations c ON m.citation_id = c.citation_id
    JOIN literature l ON c.source_id = l.literature_id
)
SELECT
    comp.SMILES,
    r.rounded_temp AS temperature_bracket, -- Shows the grouped temperature (e.g. 25)

    MAX(CASE WHEN p.name = 'CMC' THEN r.value END) AS cmc_value,
    MAX(CASE WHEN p.name = 'CMC' THEN r.doi END) AS cmc_first_doi,

    MAX(CASE WHEN p.name = 'air_water_surface_tension_CMC' THEN r.value END) AS aw_st_cmc_value,
    MAX(CASE WHEN p.name = 'air_water_surface_tension_CMC' THEN r.doi END) AS aw_st_cmc_first_doi,

    MAX(CASE WHEN p.name = 'Gamma_max' THEN r.value END) AS gamma_max_value,
    MAX(CASE WHEN p.name = 'Gamma_max' THEN r.doi END) AS gamma_max_doi

FROM ranked_measurements r
JOIN property_types p ON r.property_type_id = p.property_type_id
JOIN compounds comp ON r.compound_id = comp.compound_id
WHERE r.rn = 1
  AND r.temperature BETWEEN 20 AND 25
GROUP BY r.compound_id, comp.SMILES, r.rounded_temp
HAVING cmc_value IS NOT NULL;
