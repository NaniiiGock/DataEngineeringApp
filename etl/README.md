The corporate headquarters' data is for the Fortune 500 companies of 2017.
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
