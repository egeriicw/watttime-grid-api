from django.db import models
#from django.db.models.signals import post_save
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.genmix.models import DataPoint#, Generation
from datetime import datetime
import pytz


class FuelCarbonIntensity(models.Model):
    # fuel source type
    fuel = models.ForeignKey(FuelType)

    # balancing authority
    ba = models.ForeignKey(BalancingAuthority)
    
    # conversion between generation and emissions
    lb_CO2_per_MW = models.FloatField()

    # timestamp data validity begins (in UTC) (can be present, past, or future)
    valid_after = models.DateTimeField(default=pytz.utc.localize(datetime.utcnow()))
    
    def __str__(self):
        return '%s in %s is %.1f Lb/MW after %s' % (self.fuel,
                                                    self.ba,
                                                    self.lb_CO2_per_MW,
                                                    self.valid_after)


class Carbon(models.Model):
    # fuel-to-carbon conversions
    fuel_carbons = models.ManyToManyField(FuelCarbonIntensity)

    # data point
    dp = models.OneToOneField(DataPoint, related_name='carbon')

    # how much carbon was emitted
    # units: lb per MW
    carbon = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return '%.1f' % (self.carbon)
