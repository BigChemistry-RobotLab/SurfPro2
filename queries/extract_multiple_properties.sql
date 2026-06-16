WITH ranked_measurements AS (
    SELECT
        m.compound_id,
        m.property_type_id,
        m.value,
        m.temperature,
        ROUND(COALESCE(m.temperature, -9999), 0) AS rounded_temp,
        m.citation_id,
        l.date AS publication_year,
        l.doi,
        ROW_NUMBER() OVER (
            PARTITION BY
                m.compound_id,
                m.property_type_id,
                ROUND(COALESCE(m.temperature, -9999), 0)
            ORDER BY l.date ASC, m.created_at ASC, m.measurement_id ASC
        ) AS rank_n
    FROM measurements m
    JOIN citations c ON m.citation_id = c.citation_id
    JOIN literature l ON c.source_id = l.literature_id
),
pivoted_results AS (
    SELECT
        r.compound_id,
        comp.SMILES,
        comp.surfactant_type,
        r.rounded_temp AS temperature_bracket,
        COUNT(DISTINCT r.property_type_id) AS property_count,
        MAX(CASE WHEN p.name = 'CMC' THEN r.value END) AS cmc_value,
        MAX(CASE WHEN p.name = 'CMC' THEN r.doi END) AS cmc_first_doi,
        MAX(CASE WHEN p.name = 'air_water_surface_tension_CMC' THEN r.value END) AS aw_st_cmc_value,
        MAX(CASE WHEN p.name = 'air_water_surface_tension_CMC' THEN r.doi END) AS aw_st_cmc_first_doi,
        MAX(CASE WHEN p.name = 'Gamma_max' THEN r.value END) AS gamma_max_value,
        MAX(CASE WHEN p.name = 'Gamma_max' THEN r.doi END) AS gamma_max_doi,
        MAX(CASE WHEN p.name = 'pC20' THEN r.value END) AS pC20_value,
        MAX(CASE WHEN p.name = 'pC20' THEN r.doi END) AS pC20_doi,
        MAX(CASE WHEN p.name = 'Area_min' THEN r.value END) AS area_min_value,
        MAX(CASE WHEN p.name = 'Area_min' THEN r.doi END) AS area_min_doi,
        MAX(CASE WHEN p.name = 'Pi_CMC' THEN r.value END) AS pi_cmc_value,
        MAX(CASE WHEN p.name = 'Pi_CMC' THEN r.doi END) AS pi_cmc_doi
    FROM ranked_measurements r
    JOIN property_types p ON r.property_type_id = p.property_type_id
    JOIN compounds comp ON r.compound_id = comp.compound_id
    WHERE r.rank_n = 1
      AND r.temperature BETWEEN 20 AND 30
    GROUP BY r.compound_id, comp.SMILES, comp.surfactant_type, r.rounded_temp
),
ranked_by_density AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY compound_id
            ORDER BY property_count DESC, ABS(temperature_bracket - 25) ASC
        ) AS density_rank
    FROM pivoted_results
)
SELECT
    SMILES,
    surfactant_type,
    temperature_bracket,
    cmc_value, cmc_first_doi,
    aw_st_cmc_value, aw_st_cmc_first_doi,
    gamma_max_value, gamma_max_doi,
    pC20_value, pC20_doi,
    area_min_value, area_min_doi,
    pi_cmc_value, pi_cmc_doi
FROM ranked_by_density
WHERE density_rank = 1;
