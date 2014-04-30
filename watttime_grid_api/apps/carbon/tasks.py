from __future__ import absolute_import
from celery import shared_task
import logging
from apps.griddata.models import DataPoint
from apps.carbon.models import Carbon

# set up logger
logger = logging.getLogger(__name__)

@shared_task
def set_average_carbons(dp_ids):
    """
    Set the average carbon intensity on every DataPoint in an iterable of DataPoint ids.
    """
    for dp in DataPoint.objects.filter(pk__in=dp_ids):
        # add carbon to data point
        c, created = Carbon.objects.get_or_create(dp=dp)
        # set value for carbon
        c.set_carbon()
        # save
        c.save()
