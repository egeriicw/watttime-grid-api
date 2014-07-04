from __future__ import absolute_import
from celery import shared_task
from apps.griddata.models import CurrentDataSet, DataPoint
import logging

# set up logger
logger = logging.getLogger(__name__)


@shared_task
def update_current_set(dp_ids, do_clean=True):
    """Update current data set based new data provided"""
    # set up storage for modified data sets
    ds_pks = set([])

    # process each data point
    for dp in DataPoint.objects.filter(pk__in=dp_ids):
        # get series
        ds, created = CurrentDataSet.objects.get_or_create(ba=dp.ba)

        # add DataPoint to data set
        ds.insert(dp)

        # log data set pk
        ds_pks.add(ds.pk)

    # clean up
    if do_clean:
        for ds in CurrentDataSet.objects.filter(pk__in=ds_pks):
            ds.clean()
            ds.save()