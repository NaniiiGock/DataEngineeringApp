from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime
import duckdb
import pandas as pd

# Function to read the data from DuckDB
def read_data_from_duckdb():
    db_path = "./repo/data/my_duckdb_file.db"
    conn = duckdb.connect(database=db_path, read_only=False)
    # Read the "fortune_500" table into a pandas DataFrame
    df = conn.execute("SELECT * FROM fortune_500").fetchdf()
    conn.close()
    return df

# Function to transform the data into the star schema
def transform_data(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='read_data_from_duckdb')

    # Only keep the relevant columns
    df = df[['RANK', 'NAME', 'STATE', 'COUNTY', 'EMPLOYEES', 'REVENUES', 'COUNTYFIPS', 'PROFIT']]
    
    # Generate IDs for business and county dimensions
    df['ID'] = df['NAME'].astype('category').cat.codes
    df['BUSINESSID'] = df['ID']
    
    # Create Business fact table
    business_fact = df.copy()[['BUSINESSID', 'RANK', 'EMPLOYEES', 'REVENUES', 'PROFIT']]
    business_fact['ID'] = business_fact.index

    # Create Business dimension table
    business_dim = df.copy()[['ID', 'NAME', 'COUNTYFIPS']]

    # Create County dimension table
    county_dim = df.copy()[['COUNTYFIPS', 'COUNTY', 'STATE']]
    county_dim = county_dim.drop_duplicates()

    # Return transformed tables
    return {'business_fact': business_fact, 'business_dim': business_dim, 'county_dim': county_dim}

# Function to load the transformed data into DuckDB
def load_data_to_duckdb(**kwargs):
    tables = kwargs['ti'].xcom_pull(task_ids='transform_data')
    db_path = "./repo/data/my_duckdb_file.db"
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
    'fortune_500_data_processing',
    default_args=default_args,
    description='Process Fortune 500 data and load it into DuckDB in star schema',
    schedule_interval=None,  # Can be set to a cron expression
)

# Define tasks
read_data_task = PythonOperator(
    task_id='read_data_from_duckdb',
    python_callable=read_data_from_duckdb,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
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
read_data_task >> transform_data_task >> load_data_task
