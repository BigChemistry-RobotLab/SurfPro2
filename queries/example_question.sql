-- "Find all nonionic surfactants with CMC < 1 mM measured between 20–30 °C by tensiometry"
SELECT DISTINCT
    c.compound_id,
    c.SMILES,
    c.InChI,
    c.Molecular_Weight
FROM measurements m
JOIN compounds c USING(compound_id)
JOIN property_types ptype USING(property_type_id)
JOIN methods meth USING(method_id)
WHERE
    ptype.name = 'CMC'
    AND c.Surfactant_Type = 'non-ionic'
    AND meth.name = 'tensiometry'
    AND m.value < 0.001
    AND m.temperature BETWEEN 20 AND 30
