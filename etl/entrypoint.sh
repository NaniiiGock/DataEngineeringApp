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

airflow users create \
  --username admin \
  --password sergilolidtõeliseltsuuredkäed \
  --firstname Gustav \
  --lastname Nikopensius \
  --role Admin \
  --email gustav.nikopensius@ut.ee


exec airflow webserver &
exec airflow scheduler
