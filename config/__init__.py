# these settings are required for celery to work properly & added after we created the celery.py file in the config folder
from .celery import app as celery_app

__all__ = ("celery_app",)