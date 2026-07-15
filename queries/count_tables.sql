SELECT
    (SELECT COUNT(*) FROM compounds) AS n_compounds,
    (SELECT COUNT(*) FROM measurements) AS n_measurements,
    (SELECT COUNT(DISTINCT source_id) FROM citations) AS n_measurement_sources,
    (SELECT COUNT(*) FROM literature) AS n_literature,
    (SELECT COUNT(*) FROM methods) AS n_methods,
    (SELECT COUNT(*) FROM property_types) AS n_properties,
    (SELECT MIN(temperature) FROM measurements WHERE temperature IS NOT NULL) AS min_temp,
    (SELECT MAX(temperature) FROM measurements WHERE temperature IS NOT NULL) AS max_temp;
