from celery import Celery

app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

app.conf.update(
    result_backend='redis://redis:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)
