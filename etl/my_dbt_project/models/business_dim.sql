WITH base AS (
    SELECT
        NAME,
        CAST(COUNTYFIPS AS STRING) AS COUNTYFIPS,
        ROW_NUMBER() OVER () AS ID
    FROM {{ source('duckdb_source', 'fortune_500') }}
)
SELECT 
    ID, 
    NAME, 
    COUNTYFIPS 
FROM base
