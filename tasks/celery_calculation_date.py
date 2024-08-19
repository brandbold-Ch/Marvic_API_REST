from celery import Celery


appt_calculate_task = Celery(
    "calculate_date",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)
