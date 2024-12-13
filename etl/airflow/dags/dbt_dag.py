from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}


with DAG(
    dag_id='dbt_execution_dag1',
    default_args=default_args,
    description='Run dbt commands with Airflow',
    schedule_interval=None,  
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    run_my_table_model = BashOperator(
        task_id='run_my_table_model',
        bash_command='dbt run --project-dir /dbt --profiles-dir /dbt --select my_table'
        
    )

    run_my_table_model 
