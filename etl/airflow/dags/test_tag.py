from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# Initialize the DAG
with DAG(
    dag_id='dbt_debug_dag',
    default_args=default_args,
    description='DAG to debug dbt project',
    schedule_interval=None,  # Trigger manually
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:
    # Task to debug the dbt project
    dbt_debug_task = BashOperator(
        task_id='dbt_debug',
        bash_command='dbt debug --project-dir /dbt --profiles-dir /dbt'
    )
    dbt_debug_task