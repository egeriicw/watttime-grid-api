from __future__ import absolute_import
from celery import shared_task, subtask, group
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
    
    # insert DataPoint
    dp, dp_created = DataPoint.objects.get_or_create(ba=ba,
                                                     timestamp=gen_obs['timestamp'],
                                                     freq=gen_obs['freq'],
                                                     market=gen_obs['market'])
                                                     
    # insert Generation
    # do this instead of try: ... except IntegrityError: ...
    #     because IntegrityError has different behavior on sqlite3 and postgres
    gens = Generation.objects.filter(mix=dp, fuel=fuel)
    if gens.count() == 1:
        gen = gens.get()
        gen.gen_MW = gen_obs['gen_MW']
        gen.save()
        gen_created = False
        logger.info('Generation for %s with %s updated to %s MW' % (dp, fuel, gen.gen_MW))
    elif gens.count() == 0:
        gen = Generation.objects.create(mix=dp, fuel=fuel, gen_MW=gen_obs['gen_MW'])
        gen_created = True
        logger.info('Generation for %s with %s inserted with %s MW' % (dp, fuel, gen.gen_MW))
    else:
        logger.error('Uncaught integrity error in Generation? %s' % gens)
        gen_created = False
    
    # update counters
    if dp_created:
        ds, ds_created = DataSeries.objects.get_or_create(ba=ba,
                                                          series_type=DataSeries.HISTORICAL)
        ds.datapoints.add(dp)
        ds.save()

    return gen_created, dp_created
    
@shared_task
def cmap(it, callback):
    # Map a callback over an iterator and return as a group
    # see http://stackoverflow.com/questions/13271056/how-to-chain-a-celery-task-that-returns-a-list-into-a-group
  #  callback = subtask(callback)
  #  return group(callback.clone([arg,]) for arg in it)()
    return [callback(x) for x in it]

@shared_task
def update(ba_name, **kwargs):    
    # pre-log
    logger.info('%s: Getting data with args %s' % (ba_name, kwargs))
   # prev_latest_date = Generation.objects.filter(mix__ba__abbrev=ba_name).latest().datetime
    
    # run chain
    chain = (get_generation.s(ba_name, **kwargs) | cmap.s(insert_generation))
    res = chain()
    return res
    # check for inserts
 #   new_latest_date = Generation.objects.filter(mix__ba__abbrev=ba_name).latest().datetime
  #  logger.info('%s: Inserted %d new generation value(s) at %d new data point(s).' % (ba_name, n_new_gens, n_new_dps))
