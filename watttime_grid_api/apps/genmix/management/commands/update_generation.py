from django.core.management.base import BaseCommand, CommandError
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint, DataSeries
from apps.clients import client_factory
from apps.genmix.models import Generation
from dateutil.parser import parse as dateutil_parse
import pytz
from optparse import make_option


class Command(BaseCommand):
    args = 'BA_NAME [--dates START_AT END_AT] [--market MARKET]'
    help = 'Add new generation data to the database from the given balancing authority.'
    option_list = BaseCommand.option_list + (
        make_option('--dates',
            action='store',
            nargs=2,
            help='Start and end dates for obtaining data. If not provided, get only the most recent data point.'),
        make_option('--market',
            action='store',
            nargs=1,
            help='Market type',
            default=DataPoint.RTHR,
            choices=[x[0] for x in DataPoint.MARKET_CHOICES]),
        )
        
    def handle(self, ba_name, **options):
        # parse args
        try:
            start_at = pytz.utc.localize(dateutil_parse(options['dates'][0]))
            end_at = pytz.utc.localize(dateutil_parse(options['dates'][1]))
            latest = False
            self.stdout.write('Getting data between %s and %s...' % (start_at, end_at))
        except TypeError: # dates arg not provided
            latest = True
            start_at, end_at = None, None
            self.stdout.write('Getting the latest data...')
            
        # get data
        c = client_factory(ba_name)
        data = c.get_generation(latest=latest, start_at=start_at, end_at=end_at,
                                market=options['market'])
        self.stdout.write('Got the data, inserting...')
        
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
