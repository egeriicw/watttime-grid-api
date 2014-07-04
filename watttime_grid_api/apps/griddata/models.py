from django.db import models
from apps.gridentities.models import BalancingAuthority
from datetime import datetime
import pytz


class DataPoint(models.Model):

    # timestamp data is valid at (in UTC) (can be present, past, or future)
    timestamp = models.DateTimeField(db_index=True)
    
    # timestamp data was created at (in UTC) (can be present or past)
    created_at = models.DateTimeField(auto_now_add=True)
                              
    # frequency
    HOURLY = '1hr'
    FIVEMIN = '5m'
    TENMIN = '10m'
    IRREGULAR = 'n/a'
    FREQ_CHOICES = (
        (HOURLY, 'hourly frequency'),
        (FIVEMIN, '5-minute frequency'),
        (IRREGULAR, 'irregular frequency'),
        (TENMIN, '10-minute frequency'),
    )
    freq = models.CharField(max_length=4, choices=FREQ_CHOICES,
                               default=HOURLY)

    # market
    RTHR = 'RTHR'
    RT5M = 'RT5M'
    DAHR = 'DAHR'
    MARKET_CHOICES = (
        (RTHR, 'real-time hourly market'),
        (RT5M, 'real-time 5-minute market'),
        (DAHR, 'day-ahead hourly market'),
    )    
    market = models.CharField(max_length=4, choices=MARKET_CHOICES,
                               default=RTHR)
    
    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)

    class Meta:
        unique_together = ('timestamp', 'ba', 'freq', 'market')
        ordering = ['-timestamp', 'ba']
        get_latest_by = 'timestamp'

    def __str__(self):
        return ' '.join([self.ba.abbrev, str(self.timestamp), self.freq, self.market])

    def is_forecast(self):
        """True if the data was obtained from a forecast, False if not"""
        return self.market == self.DAHR


class DataSeries(models.Model):
    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)
    
    # data series type
    HISTORICAL = 'PAST'
    BEST = 'BEST'
    CURRENT = 'NOW'
    SERIES_CHOICES = (
        (HISTORICAL, 'historical data'),
        (BEST, 'best-guess data (historical if available, best forecast if not)'),
        (CURRENT, 'current data'),
    )
    series_type = models.CharField(max_length=4, choices=SERIES_CHOICES,
                                       default=HISTORICAL)
                                       
    datapoints = models.ManyToManyField(DataPoint)

    def __str__(self):
        return '%s %s' % (self.ba, self.series_type)

    def clean(self):
        pass


class CurrentDataSet(models.Model):
    """Data collection of the best up-to-date data for a balancing authority"""
    # don't care about creation, just about last updated
    updated_at = models.DateTimeField(auto_now=True)

    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)
    
    # single current data point
    current = models.OneToOneField(DataPoint, null=True, blank=True)

    # many historical data points
    past = models.ManyToManyField(DataPoint, related_name='past_set')

    # many forecast data points
    forecast = models.ManyToManyField(DataPoint, related_name='forecast_set')

    def __str__(self):
        return '%s %s' % (self.ba, self.updated_at)

    def clean(self):
        """Update assignments to past, current, and forecast"""
        # concatenate qset of all data points
        concat = self.past.all() | self.forecast.all()
        if self.current:
            concat |= DataPoint.objects.filter(pk=self.current.pk)

        # force queryset evaluation before clearing old data
        dps = DataPoint.objects.filter(pk__in=[dp.pk for dp in concat])

        # clear past and forecast
        self.past.clear()
        self.forecast.clear()

        # get current time
        now = pytz.utc.localize(datetime.utcnow())

        # current is most recent or now (can be any market)
        self.current = dps.filter(timestamp__lte=now).latest()

        # past is historical data in the past
        self.past.add(*dps.filter(timestamp__lte=self.current.timestamp,
                                market__in=[DataPoint.RT5M, DataPoint.RTHR]))

        # past is also forecast data that's more recent than the latest real-time
        #    while still being before the present
        try:
            self.past.add(*dps.filter(timestamp__lte=self.current.timestamp,
                                        timestamp__gt=self.past.latest().timestamp,
                                        market__in=[DataPoint.DAHR]))
        except DataPoint.DoesNotExist: # no past data
            self.past.add(*dps.filter(timestamp__lte=self.current.timestamp,
                                        market__in=[DataPoint.DAHR]))

        # forecast is forecast data in the future
        self.forecast.add(*dps.filter(timestamp__gt=self.current.timestamp,
                                    market__in=[DataPoint.DAHR]))

    def insert(self, dp):
        """
        Assign to past or future based on current point.
        The clean method should be called after this.
        """
        if not self.current:
            # add to past by default
            self.past.add(dp)
        elif self.current.timestamp < dp.timestamp:
            # future in future
            self.forecast.add(dp)
        else:
            # past in past
            self.past.add(dp)


class BaseUnboundObservation(models.Model):
    """Base class for measured or predicted value, not bound to DataPoint"""
    # measured or predicted value
    value = models.FloatField(null=True, blank=True)

    # units
    DEFAULT_UNITS = ''
    units = models.CharField(max_length=100)

    # auto timestamps for creating and updating
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Set class-based defaults"""
        # http://stackoverflow.com/questions/3786987/class-based-default-value-for-field-in-django-model-inheritance-hierarchy
        super(BaseUnboundObservation, self).__init__(*args, **kwargs)
        if not self.pk and not self.units:
            self.units = self.DEFAULT_UNITS

    def __str__(self):
        try:
            return '%d %s' % (self.value, self.units)
        except TypeError: # if none
            return 'null'


class BaseObservation(BaseUnboundObservation):
    """Base class for measured or predicted value with a many-to-one relationship to DataPoint"""
    # data point
    dp = models.ForeignKey(DataPoint)

    class Meta:
        abstract = True
