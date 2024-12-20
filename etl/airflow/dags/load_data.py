from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='load_and_transform_data',
    default_args=default_args,
    description='Load and transform raw data using dbt',
    schedule_interval=None, 
    start_date=datetime(2024, 12, 13),
    catchup=False,
) as dag:

    load_fortune_500 = BashOperator(
        task_id='load_fortune_500',
        bash_command=(
            'duckdb /dbt/data/my_duckdb_file.db "CREATE TABLE IF NOT EXISTS fortune_500 AS '
            'SELECT * FROM read_csv_auto(\'/dbt/data/Fortune_500_Corporate_Headquarters.csv\');"'
        ),
    )

    load_noaa_data = BashOperator(
        task_id='load_noaa_data',
        bash_command=(
            'duckdb /dbt/data/my_duckdb_file.db "CREATE OR REPLACE TABLE weather_data AS '
            'SELECT * FROM read_json_auto(\'/dbt/data/noaa_*.json\');"'
        ),
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir /dbt --profiles-dir /dbt',
    )

    [load_fortune_500, load_noaa_data] >> dbt_run
