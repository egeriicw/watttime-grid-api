from django.core.management.base import BaseCommand, CommandError
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint, DataSeries
from apps.clients import client_factory
from apps.genmix.models import Generation


class Command(BaseCommand):
    args = 'BA_NAME'
    help = 'Add new generation data to the database from the given balancing authority.'

    def handle(self, ba_name, **options):
        # get data
        c = client_factory(ba_name)
        data = c.get_generation(latest=True)

        # process data
        n_new_dps = 0
        n_new_gens = 0
        for gen_dp in data:
            # get metadata
            ba = BalancingAuthority.objects.get(abbrev=gen_dp['ba_name'])
            fuel = FuelType.objects.get(name=gen_dp['fuel_name'])
            
            # insert data
            dp, dp_created = DataPoint.objects.get_or_create(ba=ba,
                                                             timestamp=gen_dp['timestamp'],
                                                             freq=gen_dp['freq'],
                                                             market=gen_dp['market'])
            gen, gen_created = Generation.objects.get_or_create(mix=dp, fuel=fuel,
                                                                gen_MW=gen_dp['gen_MW'])
            
            # update counters
            if dp_created:
                n_new_dps += 1
                ds, ds_created = DataSeries.objects.get_or_create(ba=ba,
                                                                  series_type=DataSeries.HISTORICAL)
                ds.datapoints.add(dp)
                ds.save()
            if gen_created:
                n_new_gens += 1
            
        # log
        self.stdout.write('Inserted %d new generation value(s) at %d new data point(s) in %s.' % (n_new_gens, n_new_dps, ba_name))
