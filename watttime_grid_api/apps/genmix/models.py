from django.db import models
from apps.gridentities.models import BalancingAuthority, FuelType


class DataPoint(models.Model):

    # timestamp data is valid at (in UTC) (can be present, past, or future)
    timestamp = models.DateTimeField(db_index=True)
    
    # timestamp data was created at (in UTC) (can be present or past)
    created_at = models.DateTimeField(auto_now_add=True)

    # the quality or confidence we have in the data
    HISTORICAL = 'PAST'
    FORECAST_BA = 'FCBA'
    TYPICAL = 'TYP'
    QUALITY_CHOICES = (
        (HISTORICAL, 'historical data'),
        (FORECAST_BA, 'forecast provided by the balancing authority'),
        (TYPICAL, 'typical data based on time of year')
    )
    quality = models.CharField(max_length=4, choices=QUALITY_CHOICES,
                               default=HISTORICAL)

    def __str__(self):
        return '%s %s' % (self.timestamp, self.quality)        


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


class Generation(models.Model):
    # generation source type
    fuel = models.ForeignKey(FuelType)

    # generation source type
    mix = models.ForeignKey(DataPoint, related_name='genmix')

    # how much power was generated
    gen_MW = models.FloatField()
    
    def __str__(self):
        return '%s: %.1f MW' % (self.fuel, self.gen_MW)
