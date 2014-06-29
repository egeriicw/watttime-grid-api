from __future__ import absolute_import
from celery import shared_task
from apps.griddata.models import DataSeries, CurrentDataSet
import logging

# set up logger
logger = logging.getLogger(__name__)


@shared_task
def update_series(dps, series_type=DataSeries.BEST, do_clean=True):
    """Update data series based new data provided"""
    # set up storage for modified series
    series_pks = set([])

    # process each data point
    for dp in dps:
        # get series
        series, created = DataSeries.objects.get_or_create(series_type=series_type, ba=dp.ba)

        # add DataPoint to series
        series.datapoints.add(dp)

        # log series pk
        series_pks.add(series.pk)

    # clean up
    if do_clean:
        for series in DataSeries.objects.filter(pk__in=series_pks):
            series.clean()


@shared_task
def update_current_set(dps, do_clean=True):
    """Update current data set based new data provided"""
    # set up storage for modified data sets
    ds_pks = set([])

    # process each data point
    for dp in dps:
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