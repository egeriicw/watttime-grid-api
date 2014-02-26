from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'watttime_grid_api.settings.dev')
app = Celery('watttime_grid_api')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

# autodiscover tasks in any app
app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

####################
# CONSTRUCT CRONTAB
####################
# clear schedule
app.conf.CELERYBEAT_SCHEDULE = {}

# tasks every 5 min
EVERY_FIVE_PLUS_ONE = ','.join([str(i*5+1) for i in range(12)])
app.conf.CELERYBEAT_SCHEDULE.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute=EVERY_FIVE_PLUS_ONE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['BPA', 'ISONE', 'MISO', 'SPP']
})

# tasks every 10 min
EVERY_TEN_PLUS_ONE = ','.join([str(i*10+1) for i in range(6)])
app.conf.CELERYBEAT_SCHEDULE.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute=EVERY_TEN_PLUS_ONE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['CAISO']
})

# other tasks
app.conf.CELERYBEAT_SCHEDULE.update({
    # ERCOT on minute 33
    'update-ercot-genmix-latest': {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute='33'),
        'args': ['ERCOT'],
        'kwargs': {'latest': True, 'market': 'RTHR'},
    },
})