# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.6.3

# Switch to the airflow user
USER airflow

# Install necessary packages
RUN pip install --upgrade pip
RUN pip install --upgrade kaggle
RUN pip install --no-cache-dir duckdb pandas requests jupyter dbt-duckdb

# Set Jupyter Notebook to run on port 8888
EXPOSE 8888

# Set up working directory for dbt
WORKDIR /app

# Copy dbt project from repo folder
COPY ./repo/my_dbt_project /app/my_dbt_project

# Set dbt profiles directory (for connecting to DuckDB)
ENV DBT_PROFILES_DIR=/app/my_dbt_project

# Set the default entry point as a shell
ENTRYPOINT ["/bin/bash"]
