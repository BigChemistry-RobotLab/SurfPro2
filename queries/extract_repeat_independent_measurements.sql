WITH unique_identifiers AS (
    SELECT
        compound_id,
        identifier
    FROM identifiers
    GROUP BY compound_id
)
SELECT
    c.compound_id,
    i.identifier,
    c.SMILES,
    p.name,
    m.value,
    meth.name as method,
    m.temperature,
    l.doi,
    l.keyid
FROM measurements m
LEFT JOIN compounds c ON c.compound_id = m.compound_id
LEFT JOIN citations cit ON m.citation_id = cit.citation_id
LEFT JOIN literature l ON cit.source_id = l.literature_id
LEFT JOIN unique_identifiers i ON i.compound_id = m.compound_id
LEFT JOIN property_types p ON m.property_type_id = p.property_type_id
LEFT JOIN methods meth ON meth.method_id = m.method_id
WHERE p.name = "CMC"
AND ABS(m.temperature - 25.0) <= 1.0
AND cit.cited_id IS NULL
AND m.compound_id IN (
    SELECT
        compound_id
    FROM measurements m2
    LEFT JOIN citations cit2 USING(citation_id)
    LEFT JOIN property_types p2 USING(property_type_id)
    WHERE cit2.cited_id IS NULL
    AND p2.name = "CMC"
    AND ABS(m2.temperature - 25.0) <= 1.0
    GROUP BY m2.compound_id
    HAVING COUNT(*) > 3
);
