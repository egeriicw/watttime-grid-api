from django.test import TestCase
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.carbon.models import Carbon, FuelCarbonIntensity
from apps.carbon import tasks
from datetime import datetime
import pytz


class TestSetTask(TestCase):
    fixtures = ['isos', 'gentypes', 'fuelcarbonintensities']

    def add_dp(self):
        # set up data point
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=BalancingAuthority.objects.get(pk=1))

    def add_gens(self):                              
        # add generation to data point
        self.dp.genmix.create(fuel=FuelType.objects.get(name='coal'), gen_MW=100)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=300)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=200)

    def add_conversions(self):
        # set up carbon intensities
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='coal'),
                                            lb_CO2_per_MW=1000)
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='natgas'),
                                            lb_CO2_per_MW=500)
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='oil'),
                                            lb_CO2_per_MW=2000)
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='wind'),
                                            lb_CO2_per_MW=0)
        FuelCarbonIntensity.objects.create(fuel=FuelType.objects.get(name='wind'),
                                            lb_CO2_per_MW=0)

    def test_set(self):
        self.add_conversions()
        self.add_dp()
        self.add_gens()

        # carbon not set
        self.assertEqual(Carbon.objects.filter(dp__id=self.dp.id).count(), 0)

        # set with task
        tasks.set_average_carbons([self.dp.id])

        # test set
        self.assertAlmostEqual(self.dp.carbon.emissions_intensity, (100*1000.0 + 200*0.0 + 300*500.0) / (100+200+300))