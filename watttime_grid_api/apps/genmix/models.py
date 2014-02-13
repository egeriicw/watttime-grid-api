from django.db import models
from apps.gridentities.models import GridEntity


class GenMix(models.Model):
    # balancing authority or other grid entity
    ge = models.ForeignKey(GridEntity)

    # timestamp data is valid at (in UTC) (can be present, past, or future)
    timestamp = models.DateTimeField(db_index=True)
    
    # timestamp data was created at (in UTC) (can be present or past)
    created_at = models.DateTimeField(auto_now_add=True)

    # the confidence we have in the data
    TRUE = 'TRUE'
    FORECAST_GE = 'F_GE'
    CONFIDENCE_CHOICES = (
        (TRUE, 'true data'),
        (FORECAST_GE, 'forecast provided by the grid entity'),
    )
    confidence_type = models.CharField(max_length=4, choices=CONFIDENCE_CHOICES,
                                       default=TRUE)
    def __str__(self):
        return '%s %s %s' % (self.ge, self.timestamp, self.confidence_type)
        

class Generation(models.Model):
    # generation source type
    WIND = 'WIND'
    SOLAR = 'SOLR'
    NATGAS = 'NGAS'
    COAL = 'COAL'
    NUCLEAR = 'NCLR'
    HYDRO = 'HYDR'
    THERMAL = 'THRM'
    OTHER_REN = 'OREN'
    OTHER = 'OTHR'
    SOURCE_CHOICES = (
        (WIND, 'wind'),
        (SOLAR, 'solar'),
        (NATGAS, 'natural gas'),
        (COAL, 'coal'),
        (NUCLEAR, 'nuclear'),
        (HYDRO, 'hydroelectric'),
        (THERMAL, 'thermal (unknown type)'),
        (OTHER_REN, 'renewable (unknown type)'),
        (OTHER, 'other (unknown type'),
    )
    fuel = models.CharField(max_length=4, choices=SOURCE_CHOICES)

    # how much power was generated
    gen_MW = models.FloatField()
    
    # the mix
    mix = models.ManyToManyField(GenMix, related_name='sources')

    def __str__(self):
        return '%s: %.1f MW' % (self.fuel, self.gen_MW)
