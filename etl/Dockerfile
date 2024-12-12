FROM apache/airflow:2.6.3

USER airflow

# Update pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade kaggle
RUN pip install --no-cache-dir duckdb pandas requests jupyter dbt-duckdb pyspark

# Expose port
EXPOSE 8888

# Set working directory
WORKDIR /app

# Copy your DBT project
COPY ./my_dbt_project /app/my_dbt_project
ENV DBT_PROFILES_DIR=/app/my_dbt_project

# Copy the Iceberg script and required JAR file
COPY ./etl/iceberg /app/iceberg

# Execute the Iceberg script
RUN python /app/iceberg/iceberg_write.py

# Set the default entrypoint
ENTRYPOINT ["/bin/bash"]
