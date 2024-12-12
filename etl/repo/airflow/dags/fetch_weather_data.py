from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

# NOAA API base URL
BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2/"

# Your NOAA API token
API_TOKEN = "sZVQPNCtOCPOzYcOAogKFjxUDUwqbFgc"

# Headers for authentication
HEADERS = {"token": API_TOKEN}

# Function to fetch data from NOAA API
def fetch_noaa_data(dataset, start_date, end_date, location_id, datatype):
    endpoint = f"{BASE_URL}data"
    params = {
        "datasetid": dataset,  # Dataset, e.g., 'GHCND'
        "startdate": start_date,
        "enddate": end_date,
        "locationid": location_id,  # Location, e.g., "FIPS:37" (North Carolina)
        "datatypeid": datatype,    # Data type, e.g., 'TMAX' (Max Temperature)
        "limit": 1000,             # Max records per request
    }
    
    response = requests.get(endpoint, headers=HEADERS, params=params)
    response.raise_for_status()  # Raise error if request fails
    
    return pd.DataFrame(response.json().get('results', []))


def fetch_noaa_data_task(**kwargs):
    # Fetch NOAA data (use function above)
    dataset = "GHCND"
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')
    location_id = kwargs.get('location_id')
    datatype = kwargs.get('datatype')
    return fetch_noaa_data(dataset, start_date, end_date, location_id, datatype)

with DAG(
    dag_id="noaa_data_fetch",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="Fetch NOAA GHCND data",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:
    
    fetch_data = PythonOperator(
        task_id="fetch_noaa_data",
        python_callable=fetch_noaa_data_task,
        op_kwargs={
            "start_date": "2016-01-01",
            "end_date": "2016-12-31",
            "location_id": "FIPS:37",
            "datatype": "TMAX",
        },
    )

    fetch_data