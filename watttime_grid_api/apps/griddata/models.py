from django.db import models
from apps.gridentities.models import BalancingAuthority


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
