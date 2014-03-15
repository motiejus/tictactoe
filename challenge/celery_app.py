import os

from celery import Celery

from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'challenge.settings')

app = Celery('challenge')


class Config:
    CELERY_ACCEPT_CONTENT = ['msgpack', 'yaml']
    BROKER_URL = 'redis://'


app.config_from_object(Config)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
