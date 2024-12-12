from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

def execute_iceberg_script():
    import subprocess
    subprocess.run(
        ["/usr/local/bin/python3", "/opt/airflow/dags/iceberg_write.py"],
        check=True,
    )

dag = DAG(
    'write_to_iceberg',
    default_args=default_args,
    description='DAG to execute iceberg_write.py',
    schedule_interval=None,
    start_date=datetime(2024, 12, 12),
    catchup=False,
)

write_to_iceberg_task = PythonOperator(
    task_id='write_to_iceberg',
    python_callable=execute_iceberg_script,
    dag=dag,
)
