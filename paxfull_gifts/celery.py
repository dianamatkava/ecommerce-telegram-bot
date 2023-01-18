import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paxfull_gifts.settings")

app = Celery("paxfull_gifts")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()