from celery.schedules import crontab
from celery import Celery
import os

app = Celery(
    "tasks",
    broker=os.getenv("URL_REDIS"),
    backend=os.getenv("URL_REDIS"),
    include=[
        "tasks.email_task",
        "tasks.query_task"
    ]
)

app.conf.beat_schedule = {
    "check-task-table": {
        "task": "tasks.query_task.check_table_stack",
        "schedule": crontab(minute=0, hour=0)
    },
}

app.conf.timezone = "UTC"
