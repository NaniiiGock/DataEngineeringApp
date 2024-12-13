from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import json
import duckdb
from pathlib import Path
import re
import pandas as pd

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Directory containing the JSON files
DATA_DIR = '/app/data'

def load_weather_data_to_duckdb():
    db_path = os.path.join(DATA_DIR, 'my_duckdb_file.db')
    conn = duckdb.connect(database=db_path, read_only=False)
    table_name = 'weather_data'

    # Initialize table if it doesn't exist
    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} (
            date TIMESTAMP,
            county_fips TEXT,
            datatype TEXT,
            value FLOAT
        )
    """)

    # Regex pattern to match weather JSON files
    pattern = re.compile(r'^noaa_.*\.json$')
    for file_name in os.listdir(DATA_DIR):
        if pattern.match(file_name):
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    # Skip empty JSON files
                    if not data.get('results'):
                        continue
                    
                    # Convert station IDs to COUNTYFIPS (from file name or mapping logic)
                    # Assuming file names like 'noaa_<county_fips>.json'
                    county_fips = file_name.split('_')[1].split('.')[0]

                    # Aggregate data by date and datatype
                    df = pd.DataFrame(data['results'])
                    df['county_fips'] = county_fips
                    aggregated_df = (
                        df.groupby(['date', 'datatype'])['value']
                        .mean()
                        .reset_index()
                    )
                    aggregated_df['county_fips'] = county_fips

                    # Insert rows into DuckDB
                    conn.executemany(f"""
                        INSERT INTO {table_name} (date, datatype, value, county_fips)
                        VALUES (?, ?, ?, ?)
                    """, aggregated_df.values.tolist())

                    print(f"Processed file: {file_name}")
                except json.JSONDecodeError:
                    print(f"Invalid JSON: {file_name}")
    
    conn.close()
    print(f"Aggregated weather data loaded into DuckDB table: {table_name}")

# Define the DAG
with DAG(
    'process_weather_data',
    default_args=default_args,
    description='Load weather data from JSON files into DuckDB',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task to process JSON files and load into DuckDB
    process_files = PythonOperator(
        task_id='load_weather_data_to_duckdb',
        python_callable=load_weather_data_to_duckdb
    )
    
    process_files
