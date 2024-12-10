# The Datasets

This ETL process combines two datasets:
* Business data - The Forbes 500 Corporate Headquarters dataset from Kaggle, and
* Weather data - Weather observations from NOAA.
These datasets will be linked together by the **counties** in which the headquarters are located.

# Walkthrough of the ETL
## High-level walkthrough

The ETL can be broken down into two basic steps:
1) ETL the business data,
2) ETL the weather data.

To ETL the Business data, we
1) download the data from Kaggle,
2) load it into DuckDB,
3) transform the data using Pandas.
During this process, we also extract the **county identifiers** from the raw business dataset that we will use to extract the weather data and, later, join the two datasets in our analytical queries.

To ETL the Weather data, we
1) send requests to the NOAA API using the county identifiers we got from the Business ETL process,
2) save the results as json files, we have to do this piecemeal, one county at a time, since the API has rate limits.
- this results in as many json files as there are counties.
3) These json files are then combined into a single weather table and loaded into the DuckDB database.
4) This data is then transformed using Pandas.

## Transformations in detail
The Business transformations consist mostly of breaking the source dataset down into three tables to fit the start schema:
1) BusinessFACT which contains
* the company identifier (business id),
* measurables like revenue, profits and number of employees for a given company
2) BusinessDIM which contains
* id and name, and
* the county id (the county in which the head is quartered)
3) CountyDIM which contains
* county id and name, and
* state to which the county belongs (e.g Wichita county belongs to Texas state.)

The Weather transformations result in a single table:
1) WeatherFACT which contains
* date,
* county id,
* and the weather observations for
- minimum temperature,
- maximum temperature,
- average temperature,
- amount of precipitation.
Each row in the WeatherFACT table now describes the weather of a single day in a single county with these four measurements.

## Transformation as DAGs
In /etl/repo/airflow/dags we have 4 important python files:
* business_etl_v1.py
* business_transform.py
* weather_to_duckdb.py
* weather_transform.py

**business_etl_v1.py**
An important part is to have something to tie the business and weather data together. The businesses are headquartered in counties and we can aggregate the weather observations to county level averages.
We extract the county identifiers from the business dataset and use these to fetch only the weather observations that are relevant to our business data.
- DAG name: 'kaggle_to_noaa'
1) pulls the business dataset from Kaggle,
2) extracts the county fips codes (used to pull corresponding weather data later),
3) loads the raw business data into the database, and
4) fetches the weather data from NOAA, does a simple aggregation to county level averages, and 
5) saves it in json format, a json file for each county

**business_transform.py**
We want the data in star schema, thus we break down the dataset into facts and dimensions.
- DAG name: 'fortune_500_data_processing'
1) reads business data from DuckDB,
2) transforms the business data as described previously in "Transformations in detail" under Business transformations,
3) loads the data back into DuckDB database.

**weather_to_duckdb.py**
We pulled the weather data as separate json files for each county.
Now we want to combine them into a single table and load that into a database.
- DAG name: 'process_weather_data'
1) locates the weather jsons in the data folder,
2) reads and combines these into a single dataframe,
3) loads that into the DuckDB databse.

**weather_transform.py**
The big weather table we loaded into DuckDB has four columns:
* date, county, datatype, value
datatype has four possible values:
* TMIN, TAVG, TMAX and PRCP.
These are weather observations like minimum temperature or amount of precipitation.
For ease of use, we want to have a column for each observation. To accomplish this, we need to pivot the table.
- DAG name: 'weather_data_processing'
1) reads the big weather table from DuckDB,
2) pivots the table,
3) loads the pivoted table back into the database.

# The datasets in more detail
We are working with two data sources
1) The Corporate Headquarters dataset (or the business data)
2) Weather observations for the counties of these headquarters

The Corporate Headquarters' data is for the Fortune 500 companies of 2017.
It's a dataset from Kaggle.
Pulled using kaggle.cli as part of a Airflow DAG.
It goes into DuckDB for storage.
pull data >> store data in duckdb

The weather data is from NOAA.
It's pulled using NOAA's API from the ghcnd dataset which is historical daily weather dataset.
The data query is filtered using the county fips codes (unique identifiers for US counties) which we get from the corporate headquarters dataset. That way we don't pull any irrelevant data.
Also, we only pull data for the year 2016 - which is the year on which the Fortune 500 2017 list was compiled.
pull corporate data >> store corporate data >> pull weather data

The data is stored first in json files - each json file contains weather observations for a single county. The contents of said json files are aggregated. The reason being, a single county will have multiple weather stations - we want to take an average over these different stations so that we have a single average measurement for each day.

# Debugging / problems

* If you're having problems with getting Docker up, try <docker build -t my_airflow_image .>
* After that, try to up Docker again.
* If you're still having issues, say Airflow isn't initializing, then the problem might be with initializing postgres for Airflow.
* run <docker-compose run airflow bash>
* in the bash <airflow db init>
* now and afterwards, Airflow should initialize fine.


