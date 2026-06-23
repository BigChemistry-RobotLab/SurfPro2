WITH full_table AS (
    SELECT
        c.SMILES,
        l.date as year,
        l.doi,
        l.keyid,
        meth.name AS method_name,
        m.value,
        m.temperature,
        p.name as property
    FROM measurements m
    JOIN property_types p USING(property_type_id)
    JOIN compounds c USING(compound_id)
    JOIN citations cit USING(citation_id)
    JOIN literature l ON cit.source_id = l.literature_id
    JOIN methods meth USING(method_id)
),
ranked_measurements AS (
SELECT
    row_number() OVER (
        PARTITION BY SMILES, property
        ORDER BY
            year ASC,
            (method_name IS NOT NULL) DESC,
            (method_name = "tensiometry") DESC,
            (temperature IS NULL),
            ABS(temperature - 25.0) ASC
    ) as ranking,
    SMILES,
    keyid,
    method_name,
    value,
    temperature,
    property,
    doi
    FROM full_table
),
surfpro AS (
    SELECT *
    FROM ranked_measurements
    WHERE ranking = 1
)
SELECT
    SMILES,
    MAX(value) FILTER (WHERE property = 'CMC') AS CMC,
    MAX(doi) FILTER (WHERE property = 'CMC') AS CMC_doi,
    MAX(temperature) FILTER (WHERE property = 'CMC') AS CMC_Temp_Celsius,

    MAX(value) FILTER (WHERE property = 'air_water_surface_tension_CMC') AS AW_ST_CMC,
    MAX(doi) FILTER (WHERE property = 'air_water_surface_tension_CMC') AS AW_ST_CMC_doi,
    MAX(temperature) FILTER (WHERE property = 'air_water_surface_tension_CMC') AS AW_ST_CMC_Temp_Celsius,

    MAX(value) FILTER (WHERE property = 'C20') AS C20,
    MAX(doi) FILTER (WHERE property = 'C20') AS C20_doi,
    MAX(temperature) FILTER (WHERE property = 'C20') AS C20_Temp_Celsius,

    MAX(value) FILTER (WHERE property = 'Gamma_max') AS Gamma_max,
    MAX(doi) FILTER (WHERE property = 'Gamma_max') AS Gamma_max_doi,
    MAX(temperature) FILTER (WHERE property = 'Gamma_max') AS Gamma_max_Temp_Celsius
FROM surfpro
GROUP BY SMILES;
