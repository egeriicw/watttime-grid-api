from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.supply_demand.models import Load, TieFlow, Generation
from apps.griddata.models import DataPoint
from datetime import datetime
import pytz


class TestLoad(TestCase):
    fixtures = ['isos']

    def setUp(self):
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                          ba=BalancingAuthority.objects.get(pk=1))

    def test_failing_empty_create(self):
        self.assertRaises(IntegrityError, Load.objects.create)
        
    def test_create(self):
        l = Load.objects.create(value=100, dp=self.dp)
        self.assertEqual(l.value, 100)
        self.assertEqual(l.units, 'MW')

    def test_related_names(self):
        l = Load.objects.create(value=100, dp=self.dp)
        self.assertEqual(self.dp.load_set.first(), l)
        self.assertEqual(l.dp, self.dp)


class TestTieFlow(TestCase):
    fixtures = ['isos']

    def setUp(self):
        self.dp1 = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                          ba=BalancingAuthority.objects.first())
        self.dp2 = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                          ba=BalancingAuthority.objects.last())

    def test_failing_empty_create(self):
        self.assertRaises(IntegrityError, TieFlow.objects.create)
 
    def test_ok_dup_create(self):
        tf = TieFlow.objects.create(value=100, dp_source=self.dp1, dp_dest=self.dp1)
        self.assertEqual(tf.units, 'MW')

    def test_ok_nondup_create(self):
        tf = TieFlow.objects.create(value=100, dp_source=self.dp1, dp_dest=self.dp2)
        self.assertEqual(tf.units, 'MW')

    def test_related_names(self):
        tf = TieFlow.objects.create(value=100, dp_source=self.dp1, dp_dest=self.dp2)
        self.assertEqual(self.dp1.outflow.all().first(), tf)
        self.assertEqual(self.dp2.inflow.all().first(), tf)

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
