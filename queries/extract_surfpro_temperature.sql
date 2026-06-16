WITH source_grouped AS (
    SELECT
        m.compound_id,
        comp.SMILES,
        comp.surfactant_type,
        ROUND(m.temperature, 0) AS temperature,
        l.doi AS primary_source_doi,
        COUNT(DISTINCT m.property_type_id) AS property_count,
        MAX(CASE WHEN p.name = 'CMC' THEN m.value END) AS cmc_value,
        MAX(CASE WHEN p.name = 'air_water_surface_tension_CMC' THEN m.value END) AS aw_st_cmc_value,
        MAX(CASE WHEN p.name = 'Gamma_max' THEN m.value END) AS gamma_max_value,
        MAX(CASE WHEN p.name = 'pC20' THEN m.value END) AS pC20_value,
        MAX(CASE WHEN p.name = 'Area_min' THEN m.value END) AS area_min_value,
        MAX(CASE WHEN p.name = 'Pi_CMC' THEN m.value END) AS pi_cmc_value
    FROM measurements m
    JOIN citations c ON m.citation_id = c.citation_id
    JOIN literature l ON c.source_id = l.literature_id
    JOIN property_types p ON m.property_type_id = p.property_type_id
    JOIN compounds comp ON m.compound_id = comp.compound_id
    WHERE ROUND(m.temperature, 0) > 1
    GROUP BY
        m.compound_id,
        comp.SMILES,
        comp.surfactant_type,
        ROUND(m.temperature, 0),
        l.doi
),
ranked_sources AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY compound_id, temperature
            ORDER BY property_count DESC
        ) AS rank_n
    FROM source_grouped
)
SELECT
    SMILES,
    surfactant_type,
    temperature,
    primary_source_doi,
    property_count,
    cmc_value,
    aw_st_cmc_value,
    gamma_max_value,
    pC20_value,
    area_min_value,
    pi_cmc_value
FROM ranked_sources
WHERE rank_n = 1
ORDER BY SMILES, temperature;










-- WITH source_temp_counts AS (
--     SELECT
--         m.compound_id,
--         c.source_id,
--         COUNT(DISTINCT ROUND(m.temperature, 0)) AS temp_count
--     FROM measurements m
--     JOIN citations c ON m.citation_id = c.citation_id
--     GROUP BY
--         m.compound_id,
--         c.source_id
-- ),
-- source_grouped AS (
--     SELECT
--         m.compound_id,
--         comp.SMILES,
--         comp.surfactant_type,
--         ROUND(m.temperature, 0) AS temperature,
--         l.doi AS primary_source_doi,
--         stc.temp_count,
--         COUNT(DISTINCT m.property_type_id) AS property_count,
--         MAX(CASE WHEN p.name = 'CMC' THEN m.value END) AS cmc_value,
--         MAX(CASE WHEN p.name = 'air_water_surface_tension_CMC' THEN m.value END) AS aw_st_cmc_value,
--         MAX(CASE WHEN p.name = 'Gamma_max' THEN m.value END) AS gamma_max_value,
--         MAX(CASE WHEN p.name = 'pC20' THEN m.value END) AS pC20_value,
--         MAX(CASE WHEN p.name = 'Area_min' THEN m.value END) AS area_min_value,
--         MAX(CASE WHEN p.name = 'Pi_CMC' THEN m.value END) AS pi_cmc_value
--     FROM measurements m
--     JOIN citations c ON m.citation_id = c.citation_id
--     JOIN literature l ON c.source_id = l.literature_id
--     JOIN property_types p ON m.property_type_id = p.property_type_id
--     JOIN compounds comp ON m.compound_id = comp.compound_id
--     JOIN source_temp_counts stc ON m.compound_id = stc.compound_id AND c.source_id = stc.source_id
--     WHERE m.temperature > 0
--     GROUP BY
--         m.compound_id,
--         comp.SMILES,
--         comp.surfactant_type,
--         ROUND(m.temperature, 0),
--         l.doi,
--         stc.temp_count
-- ),
-- ranked_sources AS (
--     SELECT
--         *,
--         ROW_NUMBER() OVER (
--             PARTITION BY compound_id, temperature
--             ORDER BY temp_count DESC, property_count DESC
--         ) AS rank_n
--     FROM source_grouped
-- )
-- SELECT
--     SMILES,
--     surfactant_type,
--     temperature,
--     primary_source_doi,
--     temp_count,
--     property_count,
--     cmc_value,
--     aw_st_cmc_value,
--     gamma_max_value,
--     pC20_value,
--     area_min_value,
--     pi_cmc_value
-- FROM ranked_sources
-- WHERE rank_n = 1
-- ORDER BY SMILES, temperature;
