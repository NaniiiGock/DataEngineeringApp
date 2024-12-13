SELECT
    id,
    name,
    created_at,
    CASE
        WHEN status = 'active' THEN 'yes'
        ELSE 'no'
    END AS is_active
FROM raw_data_table
WHERE created_at >= '2023-01-01';
