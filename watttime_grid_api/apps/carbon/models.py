from django.db import models
from django.db.models.signals import post_save
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.genmix.models import Generation
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
    
    class Meta:
        get_latest_by = 'valid_after'
    
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
        try:
            return '%d' % (self.carbon)
        except TypeError: # if none
            return 'null'
        
    def set_carbon(self):
        """Calculate carbon intensity for this data point"""
        # clear fuel carbons
        self.fuel_carbons.clear()
        
        # set up numerator and denominator of average
        lb_CO2 = 0
        total_MW = 0
        
        # accumulate emissions for all generations
        for gen in self.dp.genmix.all():
            try:
                # get conversion factors for this fuel and BA
                fuel_to_carbons = FuelCarbonIntensity.objects.filter(fuel=gen.fuel, ba=self.dp.ba)
                # the best one is the latest before the data point
                fuel_to_carbon = fuel_to_carbons.filter(valid_after__lte=self.dp.timestamp).latest()
            except FuelCarbonIntensity.DoesNotExist:
                # if a single conversion factor is missing, clear everything
                self.fuel_carbons.clear()
                self.carbon = None
                return

            # add to sums
            lb_CO2 += fuel_to_carbon.lb_CO2_per_MW * gen.gen_MW
            total_MW += gen.gen_MW
            
            # save conversion factor
            self.fuel_carbons.add(fuel_to_carbon)
            
        # set carbon
        try:
            self.carbon = lb_CO2 / total_MW
        except ZeroDivisionError:
            self.carbon = None
                    
  #  def generation_updated(self, sender, instance, **kwargs):
        
# hooks for calculating carbon intensity
def reset_carbon_on_instance(sender, instance, **kwargs):
    instance.set_carbon()

# every time a Carbon model is saved, update its value
post_save.connect(reset_carbon_on_instance, Carbon)
