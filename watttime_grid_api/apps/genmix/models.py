from django.db import models
from apps.gridentities.models import FuelType
from apps.griddata.models import DataPoint

class Generation(models.Model):
    # generation source type
    fuel = models.ForeignKey(FuelType)

    # generation source type
    mix = models.ForeignKey(DataPoint, related_name='genmix')

    # how much power was generated
    gen_MW = models.FloatField()
    
    def __str__(self):
        return '%s: %.1f MW' % (self.fuel, self.gen_MW)
