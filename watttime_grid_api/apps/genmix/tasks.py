from __future__ import absolute_import
from celery import shared_task, subtask, group
from django.db import IntegrityError
from pyiso.tasks import get_generation
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
    # get_or_create will update an existing entry with the new gen value
    gen, gen_created = Generation.objects.get_or_create(mix=dp, fuel=fuel,
                                                        defaults={'gen_MW': gen_obs['gen_MW']})
    if gen_created:
        logger.debug('Generation for %s with %s inserted with %s MW' % (dp, fuel, gen.gen_MW))

    # add to "current" series
    if dp_created:
        series, series_created = DataSeries.objects.get_or_create(ba=ba, series_type=DataSeries.CURRENT)
        try:
            if dp.timestamp > series.datapoints.latest().timestamp:
                series.datapoints.clear()
                series.datapoints.add(dp)
        except DataPoint.DoesNotExist: # no datapoints in series
            series.datapoints.add(dp)
            
    # return
    return gen_created, dp_created
    
@shared_task
def cmap(it, callback):
    """Apply a task to each element of a task result, in series"""
    # NOT this solution http://stackoverflow.com/questions/13271056/how-to-chain-a-celery-task-that-returns-a-list-into-a-group
    return [callback(x) for x in it]
    
@shared_task(ignore_result=True)
def log_update(res_list, ba_name):
    n_new_gen = sum([x[0] for x in res_list])
    n_new_dp = sum([x[1] for x in res_list])
    logger.info('%s: Created %d new generations at %d new datapoints' % (ba_name, n_new_gen, n_new_dp))
    
@shared_task(ignore_result=True)
def update(ba_name, **kwargs):    
    # pre-log
    logger.info('%s: Getting data with args %s' % (ba_name, kwargs))
    
    # run chain
    chain = (get_generation.s(ba_name, **kwargs) | cmap.s(insert_generation) | log_update.s(ba_name))
    chain()
