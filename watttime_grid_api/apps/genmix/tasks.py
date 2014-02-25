from __future__ import absolute_import
from celery import shared_task
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.genmix.models import Generation
from apps.griddata.models import DataPoint, DataSeries


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
    