from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_iceberg_script():
    script_path = '/app/etl/iceberg/write.py'
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running Iceberg script: {result.stderr}")
    print(result.stdout)

with DAG(
    dag_id='load_data_to_iceberg',
    default_args=default_args,
    description='Load and process data into Iceberg',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    load_data_task = PythonOperator(
        task_id='load_data_to_iceberg',
        python_callable=run_iceberg_script
    )

    load_data_task
