from .celery import app as celery_app
from .task import *

__all__ = ("celery_app",)


