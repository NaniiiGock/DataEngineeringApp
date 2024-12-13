
FROM apache/airflow:2.6.3

USER airflow

RUN pip install --upgrade pip
RUN pip install --upgrade kaggle
RUN pip install --no-cache-dir duckdb pandas requests jupyter dbt-duckdb

EXPOSE 8888

WORKDIR /app

# CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--port", "8888", "--no-browser", "--allow-root"]

