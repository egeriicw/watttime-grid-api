from __future__ import absolute_import
from celery import shared_task
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.supply_demand.models import Load, Generation
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
    series, series_created = DataSeries.objects.get_or_create(ba=ba, series_type=DataSeries.CURRENT)
    try:
        if dp.timestamp > series.datapoints.latest().timestamp:
            series.datapoints.clear()
            series.datapoints.add(dp)
    except DataPoint.DoesNotExist: # no datapoints in series
        series.datapoints.add(dp)
            
    # return
    return dp.id


@shared_task
def insert_load(obs):
    # get metadata
    ba = BalancingAuthority.objects.get(abbrev=obs['ba_name'])

    # insert DataPoint
    dp, dp_created = DataPoint.objects.get_or_create(ba=ba,
                                                     timestamp=obs['timestamp'],
                                                     freq=obs['freq'],
                                                     market=obs['market'])

    # insert Load
    # get_or_create will update an existing entry with the new gen value
    obj, obj_created = Load.objects.get_or_create(dp=dp,
                                                  defaults={'value': obs['load_MW']})
    if obj_created:
        logger.debug('Load for %s inserted with %s %s' % (dp, obj.value, obj.units))

    # return
    return dp.id
