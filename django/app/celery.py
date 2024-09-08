import os
from django.app.celery import Celery,shared_task
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@shared_task(name='celery.ping')
def ping():
    return 'pong'