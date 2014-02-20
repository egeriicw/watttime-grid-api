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
    fixtures = ['isos.json']

    def test_failing_create(self):
        self.assertRaises(IntegrityError, DataPoint.objects.create)
        
    def test_default_create(self):
        dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                      ba=BalancingAuthority.objects.get(pk=1))
        self.assertEqual(dp.quality, DataPoint.HISTORICAL)
        self.assertEqual(dp.freq, DataPoint.HOURLY)
        self.assertEqual(dp.market, DataPoint.RTHR)
        self.assertEqual(dp.is_marginal, False)
        self.assertEqual(dp.genmix.count(), 0)
        for field in [dp.timestamp, dp.quality, dp.ba.abbrev, dp.market, dp.freq]:
            self.assertIn(str(field), str(dp))
            
    def test_unique(self):
        now = pytz.utc.localize(datetime.utcnow())
        dp = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RT5M,
                                        is_marginal=False)

        change_ts = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()), freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RT5M,
                                        is_marginal=False)

        change_fq = DataPoint.objects.create(timestamp=now, freq=DataPoint.FIVEMIN,
                                      ba=BalancingAuthority.objects.get(pk=2),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RT5M,
                                        is_marginal=False)

        change_ba = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=2),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RT5M,
                                        is_marginal=False)

        change_ql = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=2),
                                        quality=DataPoint.FORECAST_BA, market=DataPoint.RT5M,
                                        is_marginal=False)

        change_mk = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RTHR,
                                        is_marginal=False)

        change_mg = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=2),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RT5M,
                                        is_marginal=True)

        # can't reuse everything
        self.assertRaises(IntegrityError, DataPoint.objects.create,
                          timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1),
                                        quality=DataPoint.HISTORICAL, market=DataPoint.RT5M,
                                        is_marginal=False)
