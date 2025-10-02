from celery import Celery
from app.settings import AIRFLOW__CELERY__BROKER_URL, CELERY_BEAT_SCHEDULE

def create_celery_app():
    celery_app = Celery(
        'airflow_project',
        broker=AIRFLOW__CELERY__BROKER_URL,
        include=[
            'app.finance.tasks',
        ]
    )
    
    celery_app.conf.update(
        result_backend='rpc://',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        beat_schedule=CELERY_BEAT_SCHEDULE,
    )
    
    return celery_app

celery_app = create_celery_app()