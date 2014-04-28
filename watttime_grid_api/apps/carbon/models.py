from django.db import models
from django.db.models.signals import post_save
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.genmix.models import Generation
from datetime import datetime
import pytz
import logging


logger = logging.getLogger(__name__)

class FuelCarbonIntensity(models.Model):
    # fuel source type
    fuel = models.ForeignKey(FuelType)

    # balancing authority
    ba = models.ForeignKey(BalancingAuthority, null=True, blank=True)
    
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
    emissions_intensity = models.FloatField(null=True, blank=True)
    units = "lb/MW"
    
    def __str__(self):
        try:
            return '%d %s' % (self.emissions_intensity, self.units)
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
            # get conversion factors for this fuel and BA
            fuel_to_carbons = FuelCarbonIntensity.objects.filter(fuel=gen.fuel,
                                                                 ba=self.dp.ba)
            
            # if empty, get for null BA
            if not fuel_to_carbons.exists():
                fuel_to_carbons = FuelCarbonIntensity.objects.filter(fuel=gen.fuel,
                                                                     ba=None)

            try:
                # the best one is the latest before the data point
                fuel_to_carbon = fuel_to_carbons.filter(valid_after__lte=self.dp.timestamp).latest()
            except FuelCarbonIntensity.DoesNotExist:
                # if a single conversion factor is missing, clear everything
                self.fuel_carbons.clear()
                self.emissions_intensity = None
                logger.error('No carbon intensity found for %s in %s at %s' % (gen.fuel.name,
                                                                                    self.dp.ba.abbrev,
                                                                                    self.dp.timestamp))
                return

            # add to sums
            lb_CO2 += fuel_to_carbon.lb_CO2_per_MW * gen.gen_MW
            total_MW += gen.gen_MW
            
            # save conversion factor
            self.fuel_carbons.add(fuel_to_carbon)
            
        # set carbon
        try:
            self.emissions_intensity = lb_CO2 / total_MW
        except ZeroDivisionError:
            self.emissions_intensity = None


# every time a FuelCarbonIntensity model is saved, update its related carbon value
def reset_carbon_on_fuelcarbon(sender, instance, **kwargs):
    # get affected data points
    dps = DataPoint.objects.filter(timestamp__gt=instance.valid_after)
    
    # filter by balancing authority, if any
    if instance.ba:
        dps = dps.filter(ba=instance.ba)
        
    # filter by later valid fuel carbon
    try:
        next_instance = instance.get_next_by_valid_after()
        dps = dps.filter(timestamp__lte=next_instance.valid_after)
    except FuelCarbonIntensity.DoesNotExist:
        pass

    # reset carbon on each point
    for dp in dps:
        c, created = Carbon.objects.get_or_create(dp=dp)
        c.set_carbon()
        c.save()
post_save.connect(reset_carbon_on_fuelcarbon, FuelCarbonIntensity)
