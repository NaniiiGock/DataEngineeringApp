FROM python:3.9-slim
RUN apt-get update && apt-get install -y bash git

RUN pip install dbt-core dbt-duckdb

WORKDIR /dbt

COPY . /dbt

ENV DBT_PROFILES_DIR=/dbt

CMD ["dbt", "--help"]
