WITH base AS (
    SELECT
        ROW_NUMBER() OVER () AS BUSINESSID,
        RANK,
        EMPLOYEES,
        REVENUES,
        PROFIT
    FROM {{ source('duckdb_source', 'fortune_500') }}
)
SELECT 
    BUSINESSID, 
    RANK, 
    EMPLOYEES, 
    REVENUES, 
    PROFIT 
FROM base
