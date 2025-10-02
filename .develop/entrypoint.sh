#!/bin/bash

set -e  # Exit on any error

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done

# Create log directories if they don't exist (no permission issues since we're root)
echo "Creating log directories..."
mkdir -p /app/airflow/logs/webserver
mkdir -p /app/airflow/logs/scheduler
mkdir -p /app/airflow/logs/worker
mkdir -p /app/airflow/logs/triggerer
mkdir -p /app/airflow/logs/dag_processor

# Check if database needs initialization
if [ ! -f /app/airflow/airflow.db ]; then
    echo "Initializing Airflow database..."
    airflow db init
    
    echo "Creating admin user..."
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
else
    echo "Airflow database already exists, skipping initialization."
fi

# Always upgrade database to latest version
echo "Upgrading Airflow database..."
airflow db upgrade

echo "Starting Supervisor with all Airflow services..."
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf