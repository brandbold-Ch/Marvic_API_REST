from celery import Celery


email_app_task = Celery(
    "email_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
