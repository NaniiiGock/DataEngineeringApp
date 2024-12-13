from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Initialize the DAG
with DAG(
    dag_id='dbt_execution_dag',
    default_args=default_args,
    description='Run dbt commands with Airflow',
    schedule_interval=None,  # Trigger manually or use a CRON expression
    start_date=datetime(2024, 12, 13),
    catchup=False,
) as dag:
    
    # Task to run dbt debug
    dbt_debug = BashOperator(
        task_id='dbt_debug',
        bash_command='dbt debug --project-dir /dbt --profiles-dir /dbt'
    )

    # Task to run dbt run
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir /dbt --profiles-dir /dbt'
    )

    # Task to run dbt test
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --project-dir /dbt --profiles-dir /dbt'
    )

    # Define task dependencies
    dbt_debug >> dbt_run >> dbt_test
