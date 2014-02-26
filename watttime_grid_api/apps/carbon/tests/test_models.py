from django.test import TestCase
from django.db import IntegrityError
from apps.griddata.models import DataPoint
from apps.gridentities.models import FuelType, BalancingAuthority
from apps.carbon.models import Carbon, FuelCarbonIntensity
from apps.genmix.models import Generation
from datetime import datetime
import pytz


class TestCarbon(TestCase):
    fixtures = ['gentypes.json', 'isos.json']
    
    def setUp(self):
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

    def test_failing_create(self):
        self.assertRaises(IntegrityError, Carbon.objects.create)
        
    def test_default_create(self):
        c = Carbon.objects.create(dp=self.dp)
        self.assertIsNone(c.emissions_intensity)
        self.assertEqual(str(c), 'null')

    def test_null_carbon_wo_gen(self):
        c = Carbon.objects.create(dp=self.dp)
        c.set_carbon()
        self.assertIsNone(c.emissions_intensity)

    def test_autocreate_carbon_w_gens(self):
        self.add_gens()
        c, created = Carbon.objects.get_or_create(dp=self.dp)
        self.assertFalse(created)

    def test_autocreate_carbon_w_conversions(self):
        self.add_conversions()
        c, created = Carbon.objects.get_or_create(dp=self.dp)
        self.assertFalse(created)

    def test_null_carbon_wo_intensities(self):
        FuelCarbonIntensity.objects.all().delete()
        self.add_gens()
        c = Carbon.objects.get(dp=self.dp)
        c.set_carbon()
        self.assertIsNone(c.emissions_intensity)
        
    def test_autocalc_carbon(self):
        self.add_conversions()

        # autocalc on first new gen
        self.dp.genmix.create(fuel=FuelType.objects.get(name='coal'), gen_MW=100)
        self.assertAlmostEqual(Carbon.objects.get(dp=self.dp).emissions_intensity,
                         (100 * 1000) / 100.0)
        self.assertEqual(self.dp.carbon.fuel_carbons.count(), 1)
    
        # update on second new gen
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=200)
        self.assertAlmostEqual(Carbon.objects.get(dp=self.dp).emissions_intensity,
                         (100 * 1000 + 200 * 500) / 300.0)
        self.assertEqual(self.dp.carbon.fuel_carbons.count(), 2)
    
    def test_populated_carbon_intensities(self):
        self.add_conversions()
        self.add_gens()
        self.assertEqual(Carbon.objects.get(dp=self.dp).fuel_carbons.count(),
                         self.dp.genmix.count())
        
    def test_passing_on_dup_gen(self):
        self.add_conversions()
        self.add_gens()
        coal = FuelType.objects.get(name='coal')
        gens = Generation.objects.filter(mix=self.dp, fuel=coal)
        self.assertEqual(gens.count(), 1)
        gen = gens.get()
        gen.gen_MW = 200
        gen.save()
            
