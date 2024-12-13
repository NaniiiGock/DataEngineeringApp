WITH unique_countyfips AS (
    SELECT DISTINCT 
        CAST(COUNTYFIPS AS STRING) AS COUNTYFIPS
    FROM {{ source('duckdb_source', 'fortune_500') }}
)
SELECT 
    LPAD(COUNTYFIPS, 5, '0') AS COUNTYFIPS
FROM unique_countyfips
