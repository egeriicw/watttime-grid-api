from django.test import TestCase
from apps.genmix import tasks
from apps.genmix.models import Generation
from datetime import datetime
import pytz


class TestUpdate(TestCase):
    fixtures = ['isos', 'gentypes']

    def test_update(self):
        tasks.update('CAISO', latest=True)


class TestInsert(TestCase):
    fixtures = ['isos', 'gentypes', 'fuelcarbonintensities']

    def setUp(self):
        self.dp_dict = {'freq': '5m', 'ba_name': 'MISO', 'market': 'RT5M',
              'fuel_name': 'coal', 'gen_MW': 58906,
              'timestamp': pytz.utc.localize(datetime.utcnow())}

    def test_insert_one(self):
        gen_created, dp_created = tasks.insert_generation(self.dp_dict)
        self.assertTrue(gen_created)
        self.assertTrue(dp_created)
        
    def test_insertion_creates_carbon(self):
        gen_created, dp_created = tasks.insert_generation(self.dp_dict)        
        gen = Generation.objects.get(fuel__name=self.dp_dict['fuel_name'],
                                     mix__ba__abbrev=self.dp_dict['ba_name'])
        self.assertGreater(gen.mix.carbon.emissions_intensity, 0)
        
    def test_insert_two(self):
        tasks.insert_generation(self.dp_dict)
        tasks.insert_generation(self.dp_dict)
        
