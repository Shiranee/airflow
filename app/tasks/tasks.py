# app/tasks/tasks.py
from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

# @shared_task
# def run_ecommerce_stores():
#     call_command("call_ecommerce", type="stores")

# @shared_task
# def run_cigam_stores():
#     call_command("call_cigam", type="stores")

# @shared_task
# def run_cigam_employees():
#     call_command("call_cigam", type="employees")