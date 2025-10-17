FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    supervisor \
    netcat-openbsd \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set Airflow version and environment
ENV AIRFLOW_VERSION=2.8.1
ENV AIRFLOW_HOME=/app/airflow
ENV AIRFLOW__CORE__LOAD_EXAMPLES=false
ENV AIRFLOW__CORE__DAGS_FOLDER=/app/app/core/dags
ENV PYTHONPATH=/app/app

# Download constraints file
RUN wget https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.11.txt -O constraints.txt

# Install Airflow with constraints
RUN pip install --no-cache-dir \
    "apache-airflow[celery,redis,postgres]==${AIRFLOW_VERSION}" \
    --constraint "constraints.txt"

# Install additional packages
RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.9 \
    python-dotenv==1.0.0

# Create all necessary directories
RUN mkdir -p \
    /app/airflow/dags \
    /app/airflow/logs \
    /app/airflow/logs/webserver \
    /app/airflow/logs/scheduler \
    /app/airflow/logs/worker \
    /app/airflow/logs/triggerer \
    /app/airflow/logs/dag_processor \
    /var/log/supervisor \
    /var/run/supervisor

# Copy application and scripts
COPY app/ ./app/
COPY .develop/config/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY .develop/entrypoint.sh /entrypoint.sh

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

# Expose ports
EXPOSE 8080 5555

# Use entrypoint script
CMD ["/entrypoint.sh"]