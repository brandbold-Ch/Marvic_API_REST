from celery.schedules import crontab
from celery import Celery
from tasks.email_task import mail_sender


app = Celery(
    "queries",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=['tasks']
)


@app.task
def check_table_stack():
    mail_sender.delay("<h1>Hola<h1>", "Test", "jaredbrandon970@gmail.com")


app.conf.beat_schedule = {
    "check-task-table": {
        "task": "queries.check_table_stack",
        "schedule": crontab(minute="*")
    },
}

app.conf.timezone = "UTC"
