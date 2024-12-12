from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
import kaggle
import pandas as pd
import duckdb
from pathlib import Path
from zipfile import ZipFile
import kaggle.cli
import requests

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to download and extract the Kaggle dataset
def download_and_extract_dataset(dataset: str, zip_name: str):
    sys.argv = [sys.argv[0]] + f"datasets download {dataset}".split(" ")
    kaggle.cli.main()
    zip_path = Path(f"{zip_name}.zip")
    if zip_path.exists():
        with ZipFile(zip_path, 'r') as zfile:
            zfile.extractall('./data')
        zip_path.unlink()
    else:
        raise FileNotFoundError(f"{zip_name}.zip not found after download.")

# Function to load data into DuckDB
def load_to_duckdb(file_name: str, table_name: str):
    db_path = './data/my_duckdb_file.db'
    file_path = Path('./data') / file_name
    if file_path.exists():
        df = pd.read_csv(file_path)
        conn = duckdb.connect(database=db_path, read_only=False)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df;")
        conn.close()
    else:
        raise FileNotFoundError(f"File {file_name} not found in ./data")

# Function to extract COUNTYFIPS from DuckDB
def extract_countyfips():
    db_path = './data/my_duckdb_file.db'
    conn = duckdb.connect(database=db_path, read_only=False)
    query = "SELECT DISTINCT COUNTYFIPS FROM fortune_500"
    result = conn.execute(query).fetchall()
    conn.close()
    countyfips = [str(row[0]).zfill(5) for row in result]  # Ensure COUNTYFIPS is 5-digit
    with open('./data/countyfips.txt', 'w') as f:
        f.write('\n'.join(countyfips))
    print(f"Extracted COUNTYFIPS written to ./data/countyfips.txt")

# Function to query NOAA data
def query_noaa_data():
    with open('./data/countyfips.txt', 'r') as f:
        countyfips = f.read().splitlines()

    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
    headers = {"token": "sZVQPNCtOCPOzYcOAogKFjxUDUwqbFgc"}  # Replace with your NOAA API token
    params_template = {
        "datasetid": "GHCND",
        "datatypeid": ["PRCP", "TMAX", "TMIN", "TAVG"],
        "units": "metric",
        "startdate": "2016-01-01",
        "enddate": "2016-12-31",
        "limit": 1000,
    }

    # Iterate over COUNTYFIPS and query NOAA
    for county in countyfips:
        params = params_template.copy()
        params["locationid"] = f"FIPS:{county}"
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            with open(f'./data/noaa_{county}.json', 'w') as f:
                f.write(response.text)
            print(f"Data for FIPS {county} saved.")
        else:
            print(f"Failed to fetch data for FIPS {county}. Status code: {response.status_code}")

# Define the DAG
with DAG(
    'kaggle_to_noaa',
    default_args=default_args,
    description='Download Kaggle dataset, extract COUNTYFIPS, and query NOAA data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task to download and extract data from Kaggle
    download_data = PythonOperator(
        task_id='download_and_extract_kaggle_data',
        python_callable=download_and_extract_dataset,
        op_kwargs={
            'dataset': 'mannmann2/fortune-500-corporate-headquarters',
            'zip_name': 'fortune-500-corporate-headquarters',
        },
    )

    # Task to load data into DuckDB
    load_data = PythonOperator(
        task_id='load_data_to_duckdb',
        python_callable=load_to_duckdb,
        op_kwargs={
            'file_name': 'Fortune_500_Corporate_Headquarters.csv',
            'table_name': 'fortune_500',
        },
    )

    # Task to extract COUNTYFIPS
    extract_counties = PythonOperator(
        task_id='extract_countyfips',
        python_callable=extract_countyfips,
    )

    # Task to query NOAA data
    fetch_noaa = PythonOperator(
        task_id='fetch_noaa_data',
        python_callable=query_noaa_data,
    )

    # Define task dependencies
    download_data >> load_data >> extract_counties >> fetch_noaa
