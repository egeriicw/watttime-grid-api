from django.test import TestCase
from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from apps.griddata.models import DataPoint, DataSeries
from apps.gridentities.models import BalancingAuthority
from datetime import datetime
import pytz


class TestSeries(TestCase):
    fixtures = ['isos.json']
    def setUp(self):
        self.ba = BalancingAuthority.objects.get(pk=1)

    def test_failing_create(self):
        self.assertRaises(IntegrityError, DataSeries.objects.create)
        self.assertRaises(TransactionManagementError, DataSeries.objects.create,
                          ba=self.ba)
        
    def test_default_create(self):
        ds = DataSeries.objects.create(ba=self.ba)
        self.assertEqual(ds.series_type, DataSeries.HISTORICAL)
        self.assertEqual(ds.datapoints.count(), 0)
        for field in [ds.ba, ds.series_type]:
            self.assertIn(str(field), str(ds))


class TestPoint(TestCase):
    def test_failing_create(self):
        self.assertRaises(IntegrityError, DataPoint.objects.create)
        
    def test_default_create(self):
        dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()))
        self.assertEqual(dp.quality, DataPoint.HISTORICAL)
        self.assertEqual(dp.genmix.count(), 0)
        for field in [dp.timestamp, dp.quality]:
            self.assertIn(str(field), str(dp))
