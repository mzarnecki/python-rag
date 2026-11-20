#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=${POSTGRES_PASSWORD} psql -h "postgres" -p "5432" -U${POSTGRES_USER} -d${POSTGRES_DB} -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

python /app/bin/load_documents.py

>&2 echo "Postgres is ready - executing command"
exec $cmd
