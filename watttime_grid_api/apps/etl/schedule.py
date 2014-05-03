from celery.schedules import crontab


# clear schedule
schedule = {}

# tasks every 5 min
EVERY_FIVE_PLUS_ONE = ','.join([str(i*5+1) for i in range(12)])
schedule.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.etl.tasks.update_generation',
        'schedule': crontab(minute=EVERY_FIVE_PLUS_ONE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['ISONE', 'MISO']
})
EVERY_FIVE_PLUS_THREE = ','.join([str(i*5+3) for i in range(12)])
schedule.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.etl.tasks.update_generation',
        'schedule': crontab(minute=EVERY_FIVE_PLUS_THREE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['BPA']
})
EVERY_FIVE_PLUS_ZERO = ','.join([str(i*5) for i in range(12)])
schedule.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.etl.tasks.update_generation',
        'schedule': crontab(minute=EVERY_FIVE_PLUS_THREE),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M', 'moer_alg_name': '1'},
    } for ba_name in ['PJM']
})

# tasks every 10 min
EVERY_TEN_PLUS_TWO = ','.join([str(i*10+2) for i in range(6)])
schedule.update({
    'update-%s-genmix-latest' % ba_name.lower(): {
        'task': 'apps.etl.tasks.update_generation',
        'schedule': crontab(minute=EVERY_TEN_PLUS_TWO),
        'args': [ba_name.upper()],
        'kwargs': {'latest': True, 'market': 'RT5M'},
    } for ba_name in ['CAISO']
})

# other tasks
schedule.update({
    # ERCOT on minute 34
    'update-ercot-genmix-latest': {
        'task': 'apps.etl.tasks.update_generation',
        'schedule': crontab(minute='34'),
        'args': ['ERCOT'],
        'kwargs': {'latest': True, 'market': 'RTHR'},
    },
    # yesterday in SPP (should change to every 5 minutes once new scraper is working)
    # 'update-spp-genmix-yesterday': {
    #     'task': 'apps.etl.tasks.update_generation',
    #     'schedule': crontab(hour='14,15', minute='*/10'),
    #     'args': ['SPP'],
    #     'kwargs': {'yesterday': True, 'market': 'RT5M'},
    # },
    # yesterday in CAISO every hour (should be once, just after midnight Pacific time)
    'update-caiso-genmix-yesterday': {
        'task': 'apps.etl.tasks.update_generation',
        'schedule': crontab(hour='7', minute='20'),
        'args': ['CAISO'],
        'kwargs': {'yesterday': True, 'market': 'RTHR'},
    },
})
