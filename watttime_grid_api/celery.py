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
    } for ba_name in ['ISONE', 'MISO']
})
EVERY_FIVE_PLUS_THREE = ','.join([str(i*5+3) for i in range(12)])
app.conf.CELERYBEAT_SCHEDULE.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute=EVERY_FIVE_PLUS_THREE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['BPA']
})
EVERY_FIVE_PLUS_ZERO = ','.join([str(i*5) for i in range(12)])
app.conf.CELERYBEAT_SCHEDULE.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute=EVERY_FIVE_PLUS_THREE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['PJM']
})

# tasks every 10 min
EVERY_TEN_PLUS_TWO = ','.join([str(i*10+2) for i in range(6)])
app.conf.CELERYBEAT_SCHEDULE.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute=EVERY_TEN_PLUS_TWO),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['CAISO']
})

# other tasks
app.conf.CELERYBEAT_SCHEDULE.update({
    # ERCOT on minute 34
    'update-ercot-genmix-latest': {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(minute='34'),
        'args': ['ERCOT'],
        'kwargs': {'latest': True, 'market': 'RTHR'},
    },
    # yesterday in SPP every hour (should be once, just after midnight UTC)
#    'update-spp-genmix-yesterday': {
#        'task': 'apps.genmix.tasks.update',
#        'schedule': crontab(hour='14,15', minute='*/10'),
#        'args': ['SPP'],
#        'kwargs': {'yesterday': True, 'market': 'RT5M'},
#    },
    # yesterday in CAISO every hour (should be once, just after midnight Pacific time)
    'update-caiso-genmix-yesterday': {
        'task': 'apps.genmix.tasks.update',
        'schedule': crontab(hour='7', minute='20'),
        'args': ['CAISO'],
        'kwargs': {'yesterday': True, 'market': 'RTHR'},
    },
})
