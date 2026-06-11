WITH filtered AS (
    SELECT *
    FROM measurements
    WHERE temperature BETWEEN 20 AND 30
),
ranked AS (
    SELECT
        m.*,
        ROW_NUMBER() OVER (
            PARTITION BY m.compound_id, m.property_type_id
            ORDER BY ABS(m.temperature - 25)
        ) AS rn
    FROM filtered m
)
SELECT
    c.compound_id,
    c.SMILES,

    MAX(CASE WHEN r.property_type_id = 1 THEN r.value END) AS CMC,
    MAX(CASE WHEN r.property_type_id = 1 THEN r.temperature END) AS CMC_temperature,
    MAX(CASE WHEN r.property_type_id = 1 THEN l.doi END) AS CMC_doi,

    MAX(CASE WHEN r.property_type_id = 70 THEN r.value END) AS air_water_surface_tension_CMC,
    MAX(CASE WHEN r.property_type_id = 70 THEN r.temperature END) AS air_water_surface_tension_CMC_temperature,
    MAX(CASE WHEN r.property_type_id = 70 THEN l.doi END) AS air_water_surface_tension_CMC_doi,

    MAX(CASE WHEN r.property_type_id = 69 THEN r.value END) AS Gamma_max,
    MAX(CASE WHEN r.property_type_id = 69 THEN r.temperature END) AS Gamma_max_temperature,
    MAX(CASE WHEN r.property_type_id = 69 THEN l.doi END) AS Gamma_max_doi,

    MAX(CASE WHEN r.property_type_id = 68 THEN r.value END) AS pC20,
    MAX(CASE WHEN r.property_type_id = 68 THEN r.temperature END) AS pC20_temperature,
    MAX(CASE WHEN r.property_type_id = 68 THEN l.doi END) AS pC20_doi,

    MAX(CASE WHEN r.property_type_id = 2 THEN r.value END) AS Pi_CMC,
    MAX(CASE WHEN r.property_type_id = 2 THEN r.temperature END) AS Pi_CMC_temperature,
    MAX(CASE WHEN r.property_type_id = 2 THEN l.doi END) AS Pi_CMC_doi,

    MAX(CASE WHEN r.property_type_id = 71 THEN r.value END) AS Area_min,
    MAX(CASE WHEN r.property_type_id = 71 THEN r.temperature END) AS Area_min_temperature,
    MAX(CASE WHEN r.property_type_id = 71 THEN l.doi END) AS Area_min_doi

FROM compounds c
LEFT JOIN ranked r
    ON c.compound_id = r.compound_id
   AND r.rn = 1
LEFT JOIN citations cit
    ON cit.citation_id = r.citation_id
LEFT JOIN literature l
    ON cit.source_id = l.literature_id
GROUP BY c.compound_id, c.SMILES;
