WITH full_table AS ( -- 1. create a table for all measurements
    SELECT
        c.SMILES,
        l.date as year,
        l.doi,
        l.keyid,
        meth.name AS method_name,
        m.value,
        COALESCE(m.temperature, -9999) AS temperature,
        p.name as property
    FROM measurements m
    LEFT JOIN property_types p USING(property_type_id)
    LEFT JOIN compounds c USING(compound_id)
    LEFT JOIN citations cit USING(citation_id)
    LEFT JOIN literature l ON cit.source_id = l.literature_id
    LEFT JOIN measurement_flags m_flag USING(measurement_id)
    LEFT JOIN methods meth USING(method_id)
    WHERE m_flag.data_flag_id IS NULL -- remove flagged data
),
ranked_measurements AS ( -- 2. Rank measurements in the full table
SELECT
    row_number() OVER (
        PARTITION BY SMILES, property
        ORDER BY
            year ASC, -- prefer most recent reported values
            (method_name IS NOT NULL) DESC, -- prefer annotated methods
            (method_name = "tensiometry") DESC, -- prefer tensiometry
            (temperature IS NULL), -- prefer a temperature annotation
            ABS(temperature - 25.0) ASC -- prefer temperature closer to 25.0 °C
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
surfpro AS ( -- 3. Select the top ranked measurements for each compound
    SELECT *
    FROM ranked_measurements
    WHERE ranking = 1
)
SELECT -- 4. Pivot the table -> one compound, multiple properties
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
