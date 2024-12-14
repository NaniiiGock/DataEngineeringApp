#!/bin/bash
set -e

POSTGRES_HOST=${POSTGRES_HOST:-postgres}

until pg_isready -h "$POSTGRES_HOST" -U airflow; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - running initialization commands"

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
