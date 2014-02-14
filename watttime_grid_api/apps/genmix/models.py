from django.db import models
from apps.gridentities.models import BalancingAuthority, GenType


class GenMix(models.Model):
    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)

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
        return '%s %s %s' % (self.ba, self.timestamp, self.confidence_type)
        

class Generation(models.Model):
    # generation source type
    fuel = models.ForeignKey(GenType, related_name='data')

    # generation source type
    mix = models.ForeignKey(GenMix, related_name='mix')

    # how much power was generated
    gen_MW = models.FloatField()
    
    def __str__(self):
        return '%s: %.1f MW' % (self.fuel, self.gen_MW)
