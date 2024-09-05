from celery.schedules import crontab
from dotenv import load_dotenv
from celery import Celery
import os

load_dotenv()

app = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
    include=['tasks.email_task', 'tasks.query_task']
)

app.conf.beat_schedule = {
    "check-task-table": {
        "task": "tasks.query_task.check_table_stack",
        "schedule": crontab(minute="*/5")
    },
}

app.conf.timezone = "UTC"
