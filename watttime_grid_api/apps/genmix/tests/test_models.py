from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import FuelType, BalancingAuthority
from apps.griddata.models import DataPoint
from apps.supply_demand.models import Generation
from datetime import datetime
import pytz


class TestGeneration(TestCase):
    fixtures = ['gentypes.json', 'isos.json']

    def test_failing_create(self):
        self.assertRaises(IntegrityError, Generation.objects.create)
        
    def test_create_each_fuel(self):
        dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                          ba=BalancingAuthority.objects.get(pk=1))
        for fuel in FuelType.objects.all():
            Generation.objects.create(fuel=fuel, gen_MW=100, mix=dp)

    def test_uniqueness(self):
        # set up
        dp1 = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                          ba=BalancingAuthority.objects.get(pk=1))
        dp2 = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                          ba=BalancingAuthority.objects.get(pk=2))                                         
        fuel1 = FuelType.objects.get(pk=1)
        fuel2 = FuelType.objects.get(pk=2)

        # create with ba1 and fuel1
        dp1.genmix.create(fuel=fuel1, gen_MW=100)
        
        # passes with ba2 and fuel1
        dp2.genmix.create(fuel=fuel1, gen_MW=100)

        # passes with ba1 and fuel2
        dp1.genmix.create(fuel=fuel2, gen_MW=100)

        # fails with ba1 and fuel1
        self.assertRaises(IntegrityError, dp1.genmix.create, fuel=fuel1, gen_MW=200)        
        