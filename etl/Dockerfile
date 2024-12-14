FROM apache/airflow:2.6.3


USER airflow
RUN pip install --no-cache-dir dbt-core dbt-duckdb

USER root
RUN apt-get update && apt-get install -y git && apt-get clean

# RUN apt-get update && apt-get install -y wget && \
#     wget -O /usr/local/bin/duckdb https://github.com/duckdb/duckdb/releases/download/v0.8.1/duckdb_cli-linux-amd64 && \
#     chmod +x /usr/local/bin/duckdb

RUN mkdir -p /dbt/dbt_packages && \
    chown -R airflow:root /dbt && \
    chmod -R 775 /dbt

WORKDIR /app
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER airflow
# RUN pip install --no-cache-dir pyspark

ENTRYPOINT ["entrypoint.sh"]
