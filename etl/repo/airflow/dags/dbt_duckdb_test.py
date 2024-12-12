from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import duckdb

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Path to DuckDB database file
DUCKDB_PATH = './data/my_duckdb_file.db'

# Query to fetch the head of the new table
def query_duckdb_head():
    conn = duckdb.connect(DUCKDB_PATH)
    new_table_name = 'test_copy_table'
    result = conn.execute(f"SELECT * FROM {new_table_name} LIMIT 5").fetchall()
    print(f"Head of {new_table_name}:", result)

# Define the DAG
with DAG(
    'dbt_dag_example',
    default_args=default_args,
    description='Run dbt inside Docker and query DuckDB',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    
    check_dir = BashOperator(
    task_id='check_current_directory',
    bash_command='ls'  # This will print the current directory
    )

    # Task 1: Run dbt inside Docker
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='cd /opt/airflow/my_dbt_project && ls && dbt run --models business_transformed'
    )




    # Task 2: Query the new table in DuckDB
    query_duckdb = PythonOperator(
        task_id='query_duckdb',
        python_callable=query_duckdb_head,
    )

    # Define task dependencies
    check_dir >> run_dbt >> query_duckdb
