FROM apache/airflow:2.6.3

# Install DBT as airflow user
USER airflow
RUN pip install --no-cache-dir dbt-core dbt-duckdb

# Switch to root to copy and adjust permissions for entrypoint script
USER root
WORKDIR /app
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch back to airflow user
USER airflow

# Use the dynamic entrypoint
ENTRYPOINT ["entrypoint.sh"]
