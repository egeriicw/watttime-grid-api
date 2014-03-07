from django.core.management.base import BaseCommand, CommandError
from apps.griddata.models import DataPoint
from apps.genmix.tasks import update
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
            
        # run task
        update.apply_async(args=[ba_name],
                           kwargs={'latest': latest, 'start_at': start_at, 'end_at': end_at, 'market': options['market']},
#                           queue='management'
                           )
