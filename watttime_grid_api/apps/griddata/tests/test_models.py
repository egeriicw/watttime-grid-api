from django.test import TestCase
from django.db import IntegrityError
from django.db.transaction import TransactionManagementError
from apps.griddata.models import DataPoint, DataSeries
from apps.gridentities.models import BalancingAuthority
from datetime import datetime, timedelta
import pytz


class TestSeries(TestCase):
    fixtures = ['bageom.json']
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
            
    # def test_filter_in_ba(self):
    #     """FAILING: ba__geom__contains_properly doesn't work"""
    #     isone = BalancingAuthority.objects.get(abbrev='ISONE')
    #     DataSeries.objects.create(ba=isone)
        
    #     # passing
    #     self.assertEqual(DataSeries.objects.filter(ba=isone).count(), 1)

    #     # passing
    #     self.assertEqual(DataSeries.objects.filter(ba__geom=isone.geom).count(), 1)
        
    #     # failing
    #     qs = DataSeries.objects.filter(ba__geom__contains_properly=isone.geom.centroid)
    #     self.assertEqual(qs.count(), 1)

    def test_filter_in_dp(self):
        ds = DataSeries.objects.create(ba=self.ba)
        now = pytz.utc.localize(datetime.utcnow())
        dp = DataPoint.objects.create(timestamp=now, ba=self.ba)
        ds.datapoints.add(dp)
        self.assertEqual(ds.datapoints.count(), 1)
        
        qs = DataSeries.objects.filter(datapoints__timestamp__gte=now)
        self.assertEqual(qs.count(), 1)
        

class TestPoint(TestCase):
    fixtures = ['isos.json']

    def test_failing_create(self):
        self.assertRaises(IntegrityError, DataPoint.objects.create)
        
    def test_default_create(self):
        dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                      ba=BalancingAuthority.objects.get(pk=1))
        self.assertEqual(dp.freq, DataPoint.HOURLY)
        self.assertEqual(dp.market, DataPoint.RTHR)
        self.assertEqual(dp.genmix.count(), 0)
        for field in [dp.timestamp, dp.ba.abbrev, dp.market, dp.freq]:
            self.assertIn(str(field), str(dp))
            
    def test_unique(self):
        now = pytz.utc.localize(datetime.utcnow())
        dp = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)

        change_ts = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()), freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)

        change_fq = DataPoint.objects.create(timestamp=now, freq=DataPoint.FIVEMIN,
                                      ba=BalancingAuthority.objects.get(pk=2), market=DataPoint.RT5M)

        change_ba = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=2), market=DataPoint.RT5M)

        change_mk = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RTHR)

        # can't reuse everything
        self.assertRaises(IntegrityError, DataPoint.objects.create,
                            timestamp=now, freq=DataPoint.HOURLY,
                            ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)
                                        
    def test_latest_and_ordering(self):
        now = pytz.utc.localize(datetime.utcnow())
        dp1 = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)
        
        dp2 = DataPoint.objects.create(timestamp=now-timedelta(hours=1), freq=DataPoint.HOURLY,
                                       ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)
                                        
        # test latest
        self.assertEqual(DataPoint.objects.earliest(), dp2)
        self.assertEqual(DataPoint.objects.latest(), dp1)
        
        # test ordering: latest first
        self.assertEqual(DataPoint.objects.all()[1], DataPoint.objects.earliest())
        self.assertEqual(DataPoint.objects.all()[0], DataPoint.objects.latest())
        
    def test_expected_freq_choices(self):
        expected_choices = set(['5m', '10m','1hr', 'n/a'])
        actual_choices = set(dict(DataPoint.FREQ_CHOICES).keys())
        self.assertEqual(expected_choices, actual_choices)
        
    def test_expected_market_choices(self):
        expected_choices = set(['RT5M', 'RTHR', 'DAHR'])
        actual_choices = set(dict(DataPoint.MARKET_CHOICES).keys())
        self.assertEqual(expected_choices, actual_choices)

    def test_is_forecast(self):
        """is_forecast based on market, not timestamp"""
        past = pytz.utc.localize(datetime.utcnow())-timedelta(hours=1)
        future = pytz.utc.localize(datetime.utcnow())+timedelta(hours=1)

        # real-time markets in past are not forecast
        dp_5m_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)
        dp_hr_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RTHR)
        self.assertFalse(dp_5m_past.is_forecast())
        self.assertFalse(dp_hr_past.is_forecast())

        # day-ahead market in past is forecast
        dp_da_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.DAHR)
        self.assertTrue(dp_da_past.is_forecast())

        # real-time markets in future are not forecast
        dp_5m_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RT5M)
        dp_hr_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.RTHR)
        self.assertFalse(dp_5m_future.is_forecast())
        self.assertFalse(dp_hr_future.is_forecast())

        # day-ahead market in future is forecast
        dp_da_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=BalancingAuthority.objects.get(pk=1), market=DataPoint.DAHR)
        self.assertTrue(dp_da_future.is_forecast())

