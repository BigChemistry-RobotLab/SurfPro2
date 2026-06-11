SELECT
	c.compound_id,
	c.SMILES,
	i.identifier,
	m.value,
	p.name as "property",
	u.name as "unit",
	l.keyid as "source citation key",
	l2.keyid as "citated citation key"
FROM measurements m
LEFT JOIN compounds c ON m.compound_id = c.compound_id
LEFT JOIN property_types p ON p.property_type_id = m.property_type_id
LEFT JOIN units u ON u.unit_id = m.unit_id
LEFT JOIN identifiers i ON i.compound_id = c.compound_id
LEFT JOIN citations cit ON cit.citation_id = m.citation_id
LEFT JOIN literature l ON l.literature_id = cit.source_id
LEFT JOIN literature l2 ON l2.literature_id = cit.cited_id
WHERE c.SMILES = ?
