from django.core.management.base import BaseCommand, CommandError
from apps.griddata.models import DataPoint
from apps.marginal.models import MOERAlgorithm
from apps.etl.tasks import update_generation
from dateutil.parser import parse as dateutil_parse
import pytz
from optparse import make_option


class Command(BaseCommand):
    args = 'BA_NAME [--dates START_AT END_AT] [--market MARKET] [--moer MOER_ALG]'
    help = 'Add new generation data to the database from the given balancing authority.'
    option_list = BaseCommand.option_list + (
        make_option('--dates',
            action='store',
            nargs=2,
            help='Start and end dates for obtaining data. If not provided, get only the most recent data point.'),
        make_option('--market',
            action='store',
            nargs=1,
            help='Market type %s' % str(DataPoint.MARKET_CHOICES),
            default=DataPoint.RTHR,
            choices=[x[0] for x in DataPoint.MARKET_CHOICES]),
        make_option('--moer',
            action='store',
            nargs=1,
            help='MOER algorithm %s' % str(MOERAlgorithm.NAME_CHOICES),
            default=None,
            choices=[x[0] for x in MOERAlgorithm.NAME_CHOICES]),
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

        # update options with parsed args
        for base_opt in ['settings', 'pythonpath', 'verbosity', 'traceback']:
            options.pop(base_opt)
        options.update({'latest': latest, 'start_at': start_at, 'end_at': end_at})
            
        # run task
        update_generation.apply_async(args=[ba_name],
                           kwargs=options,
#                           queue='management'
                           )
