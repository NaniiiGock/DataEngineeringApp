
FROM apache/airflow:2.6.3

USER airflow

RUN pip install --upgrade pip
RUN pip install --upgrade kaggle
RUN pip install --no-cache-dir duckdb pandas requests jupyter dbt-duckdb

EXPOSE 8888

WORKDIR /app

COPY ./my_dbt_project /app/my_dbt_project

ENV DBT_PROFILES_DIR=/app/my_dbt_project

ENTRYPOINT ["/bin/bash"]
