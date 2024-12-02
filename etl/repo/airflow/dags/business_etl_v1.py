from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import kaggle
import pandas as pd
import duckdb

# Set up default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to download dataset from Kaggle
def download_kaggle_dataset(dataset: str, file_name: str):
    # Use the Kaggle API to download the dataset
    kaggle.api.authenticate()
    kaggle.api.dataset_download_file(dataset, file_name, path='/data')
    # Unzip if necessary
    file_path = f'/data/{file_name}.zip'
    if os.path.exists(file_path):
        os.system(f'unzip -o {file_path} -d /data')
        os.remove(file_path)
    print(f"Dataset {file_name} downloaded and stored in /data")

# Function to load data into DuckDB
def load_to_duckdb(file_name: str, table_name: str):
    # Define the DuckDB file location
    db_path = '/data/my_duckdb_file.db'
    # Load the CSV data into a DuckDB table
    file_path = f'/data/{file_name}'
    if os.path.exists(file_path):
        # Read CSV with Pandas and load into DuckDB
        df = pd.read_csv(file_path)
        conn = duckdb.connect(database=db_path, read_only=False)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df;")
        conn.close()
        print(f"Data from {file_name} loaded into DuckDB table {table_name}")
    else:
        print(f"File {file_name} not found in /data")

# Define the DAG
with DAG(
    'kaggle_to_duckdb',
    default_args=default_args,
    description='Download a Kaggle dataset and store it in DuckDB',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task to download data from Kaggle
    download_data = PythonOperator(
        task_id='download_kaggle_data',
        python_callable=download_kaggle_dataset,
        op_kwargs={
            'dataset': 'mannmann2/fortune-500-corporate-headquarters',
            'file_name': 'business.csv',
        },
    )

    # Task to load data into DuckDB
    load_data = PythonOperator(
        task_id='load_data_to_duckdb',
        python_callable=load_to_duckdb,
        op_kwargs={
            'file_name': 'business.csv',
            'table_name': 'business',
        },
    )

    # Define task dependencies
    download_data >> load_data
