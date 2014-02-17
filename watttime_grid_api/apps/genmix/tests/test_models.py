from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import FuelType
from apps.griddata.models import DataPoint
from apps.genmix.models import Generation
from datetime import datetime
import pytz


class TestGeneration(TestCase):
    fixtures = ['gentypes.json']

    def test_failing_create(self):
        self.assertRaises(IntegrityError, Generation.objects.create)
        
    def test_create_each_fuel(self):
        genmix = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()))
        for fuel in FuelType.objects.all():
            Generation.objects.create(fuel=fuel, gen_MW=100, mix=genmix)
