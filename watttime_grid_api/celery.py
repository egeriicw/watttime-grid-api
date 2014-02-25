from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watttime_grid_api.settings.dev')
app = Celery('watttime_grid_api')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

# autodiscover tasks in any app
settings.configure()
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
