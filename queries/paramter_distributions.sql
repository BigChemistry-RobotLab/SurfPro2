-- Extract the values of for measurements in SurfPro2 by property for all
-- temperatures, methods and primary literature sources, with flagged values
-- omitted.
SELECT
    c.compound_id,
    c.SMILES,
    c.Surfactant_Type,
    m.value,
    meth.name AS method,
    u.latex_math_text AS unit_latex
FROM measurements m
LEFT JOIN compounds c
    ON c.compound_id = m.compound_id
LEFT JOIN units u
    ON u.unit_id = m.unit_id
LEFT JOIN measurement_flags mf
    USING(measurement_id)
LEFT JOIN methods meth
    USING(method_id)
LEFT JOIN citations cit USING(citation_id)
WHERE
    m.property_type_id = :prop_id
    AND cit.cited_id IS NULL
    AND mf.data_flag_id IS NULL;
