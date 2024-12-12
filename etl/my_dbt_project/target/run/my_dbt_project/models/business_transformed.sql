
  
  create view "dev"."main"."business_transformed__dbt_tmp" as (
    SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'main'
  );
