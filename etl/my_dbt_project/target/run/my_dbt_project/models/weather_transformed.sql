
  
  create view "dev"."main"."weather_transformed__dbt_tmp" as (
    SELECT
  DATE,
  COUNTY_FIPS,
  DATATYPE,
  VALUE
FROM weather_data
  );
