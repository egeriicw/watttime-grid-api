from __future__ import absolute_import
from celery import shared_task, group
from django.db import IntegrityError
from apps.clients.tasks import get_generation
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.genmix.models import Generation
from apps.griddata.models import DataPoint, DataSeries
import logging

# set up logger
logger = logging.getLogger(__name__)

@shared_task
def insert_generation(gen_obs):
    # get metadata
    ba = BalancingAuthority.objects.get(abbrev=gen_obs['ba_name'])
    fuel = FuelType.objects.get(name=gen_obs['fuel_name'])
    
    # insert data
    dp, dp_created = DataPoint.objects.get_or_create(ba=ba,
                                                     timestamp=gen_obs['timestamp'],
                                                     freq=gen_obs['freq'],
                                                     market=gen_obs['market'])
    try:
        gen = Generation.objects.create(mix=dp, fuel=fuel, gen_MW=gen_obs['gen_MW'])
        gen_created = True
    except IntegrityError:
        gen = Generation.objects.get(mix=dp, fuel=fuel)
        gen.gen_MW = gen_obs['gen_MW']
        gen.save()
        gen_created = False
    
    # update counters
    if dp_created:
        ds, ds_created = DataSeries.objects.get_or_create(ba=ba,
                                                          series_type=DataSeries.HISTORICAL)
        ds.datapoints.add(dp)
        ds.save()

    return gen_created, dp_created    

@shared_task
def update(ba_name, **kwargs):    
    # get data
    logger.info('%s: Getting data with args %s' % (ba_name, kwargs))
    data = get_generation.delay(ba_name, **kwargs).get()

    # insert data
    logger.info('%s: Got %d data points, inserting...' % (ba_name, len(data)))
    res = group([insert_generation.s(x) for x in data])().get()
    
    # check for inserts
    n_new_gens = sum([x[0] for x in res])
    n_new_dps = sum([x[1] for x in res])
    logger.info('%s: Inserted %d new generation value(s) at %d new data point(s).' % (ba_name, n_new_gens, n_new_dps))
