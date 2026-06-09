-- Create a table of all values and properties in the database including
-- compound and citation information
SELECT
	c.SMILES,
	p.name as property,
	m.value,
	u.name as unit,
	m.temperature as "temperature/ °C",
	l.doi as "source doi"
FROM measurements m
LEFT JOIN compounds c ON c.compound_id = m.compound_id
LEFT JOIN units u ON m.unit_id = u.unit_id
LEFT JOIN property_types p on p.property_type_id = m.property_type_id
LEFT JOIN citations cit on cit.citation_id = m.citation_id
LEFT JOIN literature l ON l.literature_id = cit.source_id
ORDER BY property, value;
