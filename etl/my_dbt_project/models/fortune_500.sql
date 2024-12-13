select
    RANK,
    NAME,
    STATE,
    COUNTY,
    EMPLOYEES,
    REVENUES,
    COUNTYFIPS,
    PROFIT
from {{ source('raw_data', 'fortune_500') }}
