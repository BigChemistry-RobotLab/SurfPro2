-- Find the number of property annotations for
-- each compound and the number of instances of
-- two properties being annotated for the same
-- compound.
WITH compound_properties AS (
    SELECT DISTINCT
        m.compound_id,
        pt.name AS property_name
    FROM measurements m
    JOIN property_types pt
        ON m.property_type_id = pt.property_type_id
),

total_counts AS (
    SELECT
        pt.name AS property_name,
        COUNT(*) AS num_entries
    FROM measurements m
    JOIN property_types pt
        ON m.property_type_id = pt.property_type_id
    GROUP BY pt.name
),

pair_counts AS (
    SELECT
        p1.property_name AS property_1,
        p2.property_name AS property_2,
        COUNT(*) AS compound_count
    FROM compound_properties p1
    JOIN compound_properties p2
        ON p1.compound_id = p2.compound_id
    GROUP BY
        p1.property_name,
        p2.property_name
)

SELECT
    pc.property_1,
    pc.property_2,
    CASE
        WHEN pc.property_1 = pc.property_2
        THEN tc.num_entries
        ELSE pc.compound_count
    END AS count
FROM pair_counts pc
LEFT JOIN total_counts tc
    ON pc.property_1 = tc.property_name
ORDER BY
    pc.property_1,
    pc.property_2;
