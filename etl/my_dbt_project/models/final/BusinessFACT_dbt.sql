WITH OrderedTable AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY RANK DESC) AS ID, -- Generate ID based on order
        ID AS BUSINESSID,
        RANK,
        EMPLOYEES,
        REVENUES,
        PROFIT
    FROM main_transformed.stg_Business
)
SELECT * 
FROM OrderedTable