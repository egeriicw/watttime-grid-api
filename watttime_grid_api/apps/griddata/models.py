from django.db import models
from apps.gridentities.models import BalancingAuthority


class DataPoint(models.Model):

    # timestamp data is valid at (in UTC) (can be present, past, or future)
    timestamp = models.DateTimeField(db_index=True)
    
    # timestamp data was created at (in UTC) (can be present or past)
    created_at = models.DateTimeField(auto_now_add=True)

    # the quality or confidence we have in the data
    HISTORICAL = 'PAST'
    FORECAST_BA = 'FCBA'
    TYPICAL = 'TYP'
    PRELIM_HISTORICAL = 'PREH'
    QUALITY_CHOICES = (
        (HISTORICAL, 'historical data'),
        (FORECAST_BA, 'forecast provided by the balancing authority'),
        (TYPICAL, 'typical data based on time of year'),
        (PRELIM_HISTORICAL, 'preliminary historical data')
    )
    quality = models.CharField(max_length=4, choices=QUALITY_CHOICES,
                               default=HISTORICAL)
                               
    # frequency
    HOURLY = '1hr'
    FIVEMIN = '5m'
    TENMIN = '10m'
    IRREGULAR = 'n/a'
    FREQ_CHOICES = (
        (HOURLY, 'hourly frequency'),
        (FIVEMIN, '5-minute frequency'),
        (IRREGULAR, 'irregular frequency'),
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
    
    # marginal
    is_marginal = models.BooleanField(default=False)

    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)

    class Meta:
        unique_together = ('timestamp', 'quality', 'freq', 'market', 'is_marginal', 'ba')

    def __str__(self):
        if self.is_marginal:
            return ' '.join([self.ba.abbrev, str(self.timestamp), self.quality,
                             self.freq, self.market, 'marginal'])
        else:
            return ' '.join([self.ba.abbrev, str(self.timestamp), self.quality,
                             self.freq, self.market])


class DataSeries(models.Model):
    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)
    
    # data series type
    HISTORICAL = 'PAST'
    BEST = 'BEST'
    SERIES_CHOICES = (
        (HISTORICAL, 'historical data'),
        (BEST, 'best-guess data (historical if available, best forecast if not)'),
    )
    series_type = models.CharField(max_length=4, choices=SERIES_CHOICES,
                                       default=HISTORICAL)
                                       
    datapoints = models.ManyToManyField(DataPoint)

    def __str__(self):
        return '%s %s' % (self.ba, self.series_type)        
