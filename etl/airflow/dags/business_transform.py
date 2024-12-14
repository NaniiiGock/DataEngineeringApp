from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime
import duckdb
import pandas as pd


DATA_DIR = '/app/data'

def read_data_from_duckdb():
    db_path = f'{DATA_DIR}/my_duckdb_file.db'
    conn = duckdb.connect(database=db_path, read_only=False)
    df = conn.execute("SELECT * FROM fortune_500").fetchdf()
    conn.close()
    return df

def transform_data(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='read_data_from_duckdb')
    df = df[['RANK', 'NAME', 'STATE', 'COUNTY', 'EMPLOYEES', 'REVENUES', 'COUNTYFIPS', 'PROFIT']]
    df['ID'] = df['NAME'].astype('category').cat.codes
    df['BUSINESSID'] = df['ID']
    
    business_fact = df.copy()[['BUSINESSID', 'RANK', 'EMPLOYEES', 'REVENUES', 'PROFIT']]
    business_fact['ID'] = business_fact.index

    business_dim = df.copy()[['ID', 'NAME', 'COUNTYFIPS']]

    county_dim = df.copy()[['COUNTYFIPS', 'COUNTY', 'STATE']]
    county_dim = county_dim.drop_duplicates()

    return {'BusinessFACT': business_fact, 'BusinessDIM': business_dim, 'CountyDIM': county_dim}

def load_data_to_duckdb(**kwargs):
    tables = kwargs['ti'].xcom_pull(task_ids='transform_data')
    db_path = f'{DATA_DIR}/my_duckdb_file.db'
    conn = duckdb.connect(database=db_path, read_only=False)
    
    for table_name, df in tables.items():
        conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} AS 
        SELECT * FROM df
        """)
    
    conn.close()

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2024, 12, 10),
    'catchup': False,
}

dag = DAG(
    'fortune_500_data_processing',
    default_args=default_args,
    description='Process Fortune 500 data and load it into DuckDB in star schema',
    schedule_interval=None, 
)

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

read_data_task >> transform_data_task >> load_data_task
