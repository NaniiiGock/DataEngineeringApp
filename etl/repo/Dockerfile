# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.6.3

# Switch to the airflow user
USER airflow

# Install necessary packages
RUN pip install --upgrade pip
RUN pip install --upgrade kaggle
RUN pip install --no-cache-dir duckdb pandas requests jupyter

# Set Jupyter Notebook to run on port 8888
EXPOSE 8888
