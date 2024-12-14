SELECT
    county_fips,
    AVG(value) AS avg_value,
    datatype
FROM main_transformed.stg_weather_data
GROUP BY county_fips, datatype