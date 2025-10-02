from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from app.finance.tasks import process_financial_data

default_args = {
    'owner': 'finance',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def process_finance_data(**kwargs):
    """Wrapper function for Celery task"""
    data = kwargs.get('data', [])
    result = process_financial_data.delay(data)
    return result.get(timeout=300)

with DAG(
    'finance_data_pipeline',
    default_args=default_args,
    description='Financial data processing pipeline',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['finance'],
) as dag:

    process_data_task = PythonOperator(
        task_id='process_financial_data',
        python_callable=process_finance_data,
        op_kwargs={'data': ['item1', 'item2', 'item3']},
    )

    process_data_task