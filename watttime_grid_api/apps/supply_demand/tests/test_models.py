from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority
from apps.supply_demand.models import Load, TieFlow
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
