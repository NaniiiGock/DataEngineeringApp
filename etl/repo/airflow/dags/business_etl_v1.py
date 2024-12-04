from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import pandas as pd
from pathlib import Path
from zipfile import ZipFile
import duckdb
import kaggle.cli

# Set up default arguments for the DAG
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
    # Use kaggle.cli to download the dataset
    sys.argv = [sys.argv[0]] + f"datasets download {dataset}".split(" ")
    kaggle.cli.main()
    
    # Extract the downloaded zip file
    zip_path = Path(f"{zip_name}.zip")
    if zip_path.exists():
        with ZipFile(zip_path, 'r') as zfile:
            zfile.extractall('./data')
        zip_path.unlink()  # Remove the zip file after extraction
        print(f"Dataset {zip_name} downloaded and extracted to ./data")
    else:
        raise FileNotFoundError(f"{zip_name}.zip not found after download.")

# Function to load data into DuckDB
def load_to_duckdb(file_name: str, table_name: str):
    # Define the DuckDB file location
    db_path = './data/my_duckdb_file.db'
    file_path = Path('./data') / file_name
    if file_path.exists():
        # Load CSV data using Pandas and insert into DuckDB
        df = pd.read_csv(file_path)
        conn = duckdb.connect(database=db_path, read_only=False)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df;")
        conn.close()
        print(f"Data from {file_name} loaded into DuckDB table {table_name}")
    else:
        raise FileNotFoundError(f"File {file_name} not found in ./data")

# Define the DAG
with DAG(
    'kaggle_to_duckdb',
    default_args=default_args,
    description='Download a Kaggle dataset and store it in DuckDB',
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

    # Define task dependencies
    download_data >> load_data
