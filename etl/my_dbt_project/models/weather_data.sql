select
    date,
    county_fips,
    datatype,
    value
from {{ source('raw_data', 'weather_data') }}
