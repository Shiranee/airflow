import os
from pathlib import Path
from celery.schedules import crontab
from datetime import timedelta

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Airflow configuration
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', BASE_DIR / 'airflow')
AIRFLOW__CORE__DAGS_FOLDER = os.getenv('AIRFLOW__CORE__DAGS_FOLDER', BASE_DIR / 'dags')
AIRFLOW__CORE__LOAD_EXAMPLES = os.getenv('AIRFLOW__CORE__LOAD_EXAMPLES', 'false')

# Database
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN = os.getenv(
    'AIRFLOW__DATABASE__SQL_ALCHEMY_CONN',
    'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow'
)

# Celery configuration
AIRFLOW__CELERY__RESULT_BACKEND = os.getenv(
    'AIRFLOW__CELERY__RESULT_BACKEND',
    'db+postgresql://airflow:airflow@postgres:5432/airflow'
)
AIRFLOW__CELERY__BROKER_URL = os.getenv(
    'AIRFLOW__CELERY__BROKER_URL',
    'redis://redis:6379/0'
)

# Executor
AIRFLOW__CORE__EXECUTOR = os.getenv('AIRFLOW__CORE__EXECUTOR', 'CeleryExecutor')

# Webserver
AIRFLOW__WEBSERVER__WEB_SERVER_PORT = os.getenv('AIRFLOW__WEBSERVER__WEB_SERVER_PORT', 8080)

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    'finance-daily-report': {
        'task': 'app.finance.tasks.generate_daily_report',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}

# Custom settings
FINANCE_API_KEY = os.getenv('FINANCE_API_KEY', '')
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))