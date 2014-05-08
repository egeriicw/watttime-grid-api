from django.test import TestCase
from apps.griddata.models import DataSeries
from apps.supply_demand import tasks
from apps.supply_demand.models import Load, Generation
from datetime import datetime
import pytz


class TestInsertLoad(TestCase):
    fixtures = ['isos']

    def setUp(self):
        self.dp_dict = {'freq': '5m', 'ba_name': 'MISO', 'market': 'RT5M',
              'load_MW': 58906,
              'timestamp': pytz.utc.localize(datetime.utcnow())}

    def test_insert_one(self):
        dp_id = tasks.insert_load(self.dp_dict)
        load = Load.objects.get(dp__ba__abbrev=self.dp_dict['ba_name'])
        self.assertEqual(dp_id, load.dp.id)

    def test_insert_two(self):
        tasks.insert_load(self.dp_dict)
        tasks.insert_load(self.dp_dict)

    def test_insert_series(self):
        self.assertEqual(DataSeries.objects.count(), 0)
        tasks.insert_load(self.dp_dict)
        
        self.assertEqual(DataSeries.objects.count(), 1)
        self.assertEqual(DataSeries.objects.get(series_type=DataSeries.CURRENT).datapoints.count(), 1)

        tasks.insert_load(self.dp_dict)
        self.assertEqual(DataSeries.objects.count(), 1)
        self.assertEqual(DataSeries.objects.get(series_type=DataSeries.CURRENT).datapoints.count(), 1)


class TestInsertGeneration(TestCase):
    fixtures = ['isos', 'gentypes']

    def setUp(self):
        self.dp_dict = {'freq': '5m', 'ba_name': 'MISO', 'market': 'RT5M',
              'fuel_name': 'coal', 'gen_MW': 58906,
              'timestamp': pytz.utc.localize(datetime.utcnow())}

    def test_insert_one(self):
        dp_id = tasks.insert_generation(self.dp_dict)
        gen = Generation.objects.get(fuel__name=self.dp_dict['fuel_name'],
                                     mix__ba__abbrev=self.dp_dict['ba_name'])
        self.assertEqual(dp_id, gen.mix.id)

    def test_insert_two(self):
        tasks.insert_generation(self.dp_dict)
        tasks.insert_generation(self.dp_dict)

    def test_insert_series(self):
        self.assertEqual(DataSeries.objects.count(), 0)
        tasks.insert_generation(self.dp_dict)
        
        self.assertEqual(DataSeries.objects.count(), 1)
        self.assertEqual(DataSeries.objects.get(series_type=DataSeries.CURRENT).datapoints.count(), 1)

        tasks.insert_generation(self.dp_dict)
        self.assertEqual(DataSeries.objects.count(), 1)
        self.assertEqual(DataSeries.objects.get(series_type=DataSeries.CURRENT).datapoints.count(), 1)
