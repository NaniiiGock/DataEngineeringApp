WITH raw_weather AS (
    SELECT 
        DATE AS DATE,
        CAST(county_fips AS STRING) AS COUNTYFIPS,
        datatype AS DATATYPE,
        value AS VALUE
    FROM {{ source('duckdb_source', 'weather_data') }}
),
pivoted_weather AS (
    SELECT 
        DATE,
        COUNTYFIPS,
        MAX(CASE WHEN DATATYPE = 'PRCP' THEN VALUE END) AS PRCP,
        MAX(CASE WHEN DATATYPE = 'TMAX' THEN VALUE END) AS TMAX,
        MAX(CASE WHEN DATATYPE = 'TMIN' THEN VALUE END) AS TMIN,
        MAX(CASE WHEN DATATYPE = 'TAVG' THEN VALUE END) AS TAVG
    FROM raw_weather
    GROUP BY DATE, COUNTYFIPS
)
SELECT 
    ROW_NUMBER() OVER () AS ID,
    DATE,
    COUNTYFIPS,
    PRCP,
    TMAX,
    TMIN,
    TAVG
FROM pivoted_weather
