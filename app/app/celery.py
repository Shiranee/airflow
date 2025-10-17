from django.db.backends.postgresql.base import DatabaseWrapper
import os
import warnings
from celery import Celery
from django.conf import settings
import tasks.tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

def skip_version_check(self):
    warnings.warn(
        "PostgreSQL version is below Django's supported minimum. Proceeding anyway."
    )

DatabaseWrapper.check_database_version_supported = skip_version_check

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(["app"])

from tasks.schedules import CELERY_BEAT_SCHEDULE
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
