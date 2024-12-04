from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import duckdb
import os

# Set default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to validate the DuckDB file and table content
def check_duckdb_file(db_path: str, table_name: str):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"DuckDB file not found at {db_path}")

    # Connect to the DuckDB database
    conn = duckdb.connect(database=db_path, read_only=True)
    
    # Check if the table exists
    try:
        result = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
        if result.empty:
            print(f"Table {table_name} exists but contains no rows.")
        else:
            print(f"First few rows from {table_name}:")
            print(result)
    except Exception as e:
        raise ValueError(f"Error accessing table {table_name}: {e}")
    finally:
        conn.close()

# Define the DAG
with DAG(
    'verify_duckdb',
    default_args=default_args,
    description='Verify that the DuckDB file exists and contains data',
    schedule_interval=None,  # Run manually
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Task to validate DuckDB file and table
    validate_duckdb = PythonOperator(
        task_id='validate_duckdb',
        python_callable=check_duckdb_file,
        op_kwargs={
            'db_path': './data/my_duckdb_file.db', 
            'table_name': 'fortune_500', 
        },
    )

    validate_duckdb
