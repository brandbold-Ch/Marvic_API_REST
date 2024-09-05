from celery.schedules import crontab
from celery import Celery


app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=['tasks.email_task', 'tasks.query_task']
)

app.conf.beat_schedule = {
    "check-task-table": {
        "task": "tasks.query_task.check_table_stack",
        "schedule": crontab(minute="*/5")
    },
}

app.conf.timezone = "UTC"
