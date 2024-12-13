WITH unique_counties AS (
    SELECT DISTINCT 
        COUNTYFIPS,
        COUNTY,
        STATE
    FROM {{ source('duckdb_source', 'fortune_500') }}
)
SELECT 
    COUNTYFIPS, 
    COUNTY, 
    STATE 
FROM unique_counties
