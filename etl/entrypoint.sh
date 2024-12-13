#!/bin/bash
set -e

POSTGRES_HOST=${POSTGRES_HOST:-postgres}

# Wait for the Postgres database to be ready
until pg_isready -h "$POSTGRES_HOST" -U airflow; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - running initialization commands"

# Run database initialization
airflow db init

# Create an admin user
airflow users create \
  --username admin \
  --password sergilolidtõeliseltsuuredkäed \
  --firstname Gustav \
  --lastname Nikopensius \
  --role Admin \
  --email gustav.nikopensius@ut.ee

# Start the Airflow webserver and scheduler
exec airflow webserver &
exec airflow scheduler
