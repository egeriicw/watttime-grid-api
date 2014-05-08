from django.test import TestCase
from apps.griddata.models import DataSeries
from apps.supply_demand import tasks
from apps.supply_demand.models import Load
from datetime import datetime
import pytz


class TestInsert(TestCase):
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
