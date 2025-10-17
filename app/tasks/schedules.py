'''
Schedules for celery workers
'''
from celery.schedules import crontab

COMMON_SCHEDULE = crontab(hour=7, minute=0)
COMMON_OPTIONS = {
    "expires": 600,
    "store_errors_even_if_ignored": True,
}

TASKS = [
    "tasks.tasks.run_ecommerce_stores",
    "tasks.tasks.run_cigam_stores",
    "tasks.tasks.run_cigam_employees",
]

CELERY_BEAT_SCHEDULE = {
    task.split(".")[-1]: {
        "task": task,
        "schedule": COMMON_SCHEDULE,
        "options": COMMON_OPTIONS,
    }
    for task in TASKS
}