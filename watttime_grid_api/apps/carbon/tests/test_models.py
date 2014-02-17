from django.test import TestCase
from django.db import IntegrityError
from apps.griddata.models import DataPoint
from apps.gridentities.models import FuelType, BalancingAuthority
from apps.carbon.models import Carbon, FuelCarbonIntensity
from datetime import datetime
import pytz


class TestCarbon(TestCase):
    fixtures = ['gentypes.json', 'isos.json']
    
    def setUp(self):
        # set up carbon intensities
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='coal'),
                                            lb_CO2_per_MW=1000)
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='natgas'),
                                            lb_CO2_per_MW=500)
        FuelCarbonIntensity.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                           fuel=FuelType.objects.get(name='wind'),
                                            lb_CO2_per_MW=0)

        # set up data point
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=BalancingAuthority.objects.get(pk=1))
                                           
        # add generation to data point
        self.dp.genmix.create(fuel=FuelType.objects.get(name='coal'), gen_MW=100)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=300)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=200)

    def test_failing_create(self):
        self.assertRaises(IntegrityError, Carbon.objects.create)
        
    def test_create(self):
        Carbon.objects.create(dp=self.dp)

    def test_null_carbon_wo_gen(self):
        self.dp.genmix.all().delete()
        c = Carbon.objects.create(dp=self.dp)
        self.assertIsNone(c.carbon)

    def test_null_carbon_wo_intensities(self):
        FuelCarbonIntensity.objects.all().delete()
        c = Carbon.objects.create(dp=self.dp)
        self.assertIsNone(c.carbon)

    def test_autocalc_carbon(self):
        c = Carbon.objects.create(dp=self.dp)
        expected_carbon_intensity = (1000 * 100 + 500 * 300 + 0 * 200) / float(100 + 300 + 200)
        self.assertEqual(c.carbon, expected_carbon_intensity)
    
    def test_populated_carbon_intensities(self):
        c = Carbon.objects.create(dp=self.dp)
        self.assertEqual(c.fuel_carbons.count(), self.dp.genmix.count())
    