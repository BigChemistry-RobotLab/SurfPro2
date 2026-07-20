-- Extract all measurements from the database which are not flagged
SELECT
    p.name AS property,
    p.latex_math_text,
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

LEFT JOIN measurement_flags m_flag
    USING(measurement_id)

LEFT JOIN methods meth
    USING(method_id)

LEFT JOIN property_types p
    USING(property_type_id)

WHERE m_flag.data_flag_id IS NULL;
