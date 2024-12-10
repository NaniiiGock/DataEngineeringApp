from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime
import duckdb
import pandas as pd

# Function to read the data from DuckDB
def read_data_from_duckdb():
    db_path = "./data/my_duckdb_file.db"
    conn = duckdb.connect(database=db_path, read_only=False)
    # Read the "weather_data" table into a pandas DataFrame
    df = conn.execute("SELECT * FROM weather_data").fetchdf()
    conn.close()
    return df

# Function to pivot the data
def pivot_data(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='read_data_from_duckdb')
    # Pivot the DataFrame
    pivot_df = df.pivot_table(index=['date', 'county_fips'], columns='datatype', values='value').reset_index()
    # Flatten the column names
    pivot_df.columns.name = None
    pivot_df.columns = [col if isinstance(col, str) else col[1] for col in pivot_df.columns]
    pivot_df['ID'] = pivot_df.index
    pivot_df.rename(columns={'date': 'DATE', 'county_fips': 'COUNTYFIPS'}, inplace=True)
    return {'WeatherFACT': pivot_df}

# Function to load the pivoted data back into DuckDB
def load_data_to_duckdb(**kwargs):
    tables = kwargs['ti'].xcom_pull(task_ids='transform_data')
    db_path = './data/my_duckdb_file.db'
    conn = duckdb.connect(database=db_path, read_only=False)
    
    # Load each DataFrame into DuckDB as a table if it doesn't exist
    for table_name, df in tables.items():
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} AS 
        SELECT * FROM df
        """)
    
    conn.close()

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2024, 12, 10),
    'catchup': False,
}

# Define the DAG
dag = DAG(
    'weather_data_processing',
    default_args=default_args,
    description='Process weather data and load it into DuckDB',
    schedule_interval=None,  # Can be set to a cron expression
)

# Define tasks
read_data_task = PythonOperator(
    task_id='read_data_from_duckdb',
    python_callable=read_data_from_duckdb,
    dag=dag,
)

pivot_data_task = PythonOperator(
    task_id='pivot_data',
    python_callable=pivot_data,
    provide_context=True,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data_to_duckdb',
    python_callable=load_data_to_duckdb,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
read_data_task >> pivot_data_task >> load_data_task
