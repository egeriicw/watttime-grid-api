from __future__ import absolute_import
from celery import shared_task
from apps.gridentities.models import BalancingAuthority
from apps.supply_demand.models import Load
from apps.griddata.models import DataPoint, DataSeries
import logging

# set up logger
logger = logging.getLogger(__name__)

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
    return dp.id
