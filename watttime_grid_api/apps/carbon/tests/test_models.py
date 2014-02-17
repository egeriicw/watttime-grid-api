from django.test import TestCase
from django.db import IntegrityError
from apps.griddata.models import DataPoint
from apps.gridentities.models import FuelType
from apps.carbon.models import Carbon, FuelCarbonIntensity
from datetime import datetime
import pytz


class TestCarbon(TestCase):
    fixtures = ['gentypes.json']
    
    def setUp(self):
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()))
        self.dp.genmix.create(fuel=FuelType.objects.get(name='coal'), gen_MW=100)

    def test_failing_create(self):
        self.assertRaises(IntegrityError, Carbon.objects.create)
        
    def test_create(self):
        Carbon.objects.create(dp=self.dp)

    def test_null_carbon_wo_gen(self):
        c = Carbon.objects.create(dp=self.dp)
        self.assertIsNone(c.carbon)

    