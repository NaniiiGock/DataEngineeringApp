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
    dag_id='load_weather_json_to_iceberg',
    default_args=default_args,
    description='Load NOAA weather JSON files into Iceberg using Spark',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    process_weather_data = BashOperator(
        task_id='process_weather_data_to_iceberg',
        bash_command=(
            "docker exec spark_service spark-submit \
            --master local[*] \
            --jars /opt/spark/jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar \
            /app/etl/iceberg/iceberg_write.py"
        )
    )
    process_weather_data
