from django.test import TestCase
from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from apps.genmix.models import GenMix, Generation
from apps.gridentities.models import BalancingAuthority, GenType
from datetime import datetime
import pytz


class TestGeneration(TestCase):
    fixtures = ['isos.json', 'gentypes.json']

    def test_failing_create(self):
        self.assertRaises(IntegrityError, Generation.objects.create)
        
    def test_create_each_fuel(self):
        genmix = GenMix.objects.create(ba=BalancingAuthority.objects.get(pk=1),
                                       timestamp=pytz.utc.localize(datetime.utcnow()))
        for fuel in GenType.objects.all():
            Generation.objects.create(fuel=fuel, gen_MW=100, mix=genmix)


class TestGenMix(TestCase):
    fixtures = ['isos.json']
    def setUp(self):
        self.ba = BalancingAuthority.objects.get(pk=1)

    def test_failing_create(self):
        self.assertRaises(IntegrityError, GenMix.objects.create)
        self.assertRaises(TransactionManagementError, GenMix.objects.create,
                          timestamp=pytz.utc.localize(datetime.utcnow()))
        self.assertRaises(TransactionManagementError, GenMix.objects.create,
                          ba=self.ba)
        
    def test_default_create(self):
        genmix = GenMix.objects.create(ba=self.ba,
                                       timestamp=pytz.utc.localize(datetime.utcnow()))
        self.assertEqual(genmix.confidence_type, GenMix.TRUE)
        self.assertEqual(genmix.mix.count(), 0)
        for field in [genmix.ba, genmix.timestamp, genmix.confidence_type]:
            self.assertIn(str(field), str(genmix))