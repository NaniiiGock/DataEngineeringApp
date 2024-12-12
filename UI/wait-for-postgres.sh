#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for PostgreSQL at $host:5432"

until pg_isready -h "$host" -p 5432; do
  echo "$(date) - Postgres is unavailable - sleeping"
  sleep 3
done

echo "Postgres is up - executing command"
exec $cmd
