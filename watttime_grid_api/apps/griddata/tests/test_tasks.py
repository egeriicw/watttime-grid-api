from django.test import TestCase
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataSeries, DataPoint
from apps.griddata import tasks
from datetime import datetime, timedelta
import pytz


class TestUpdateSeries(TestCase):
    fixtures = ['isos']

    def setUp(self):
        past = pytz.utc.localize(datetime.utcnow())-timedelta(hours=1)
        future = pytz.utc.localize(datetime.utcnow())+timedelta(hours=1)
        self.ba = BalancingAuthority.objects.first()
        dp_5m_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.RT5M)
        dp_hr_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.RTHR)
        dp_da_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.DAHR)
        dp_5m_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.RT5M)
        dp_hr_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.RTHR)
        dp_da_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.DAHR)
        self.best_pks = [dp_5m_past.pk, dp_da_future.pk]

    def test_failing_default(self):
        """Raises TypeError with no args"""
        self.assertRaises(TypeError, tasks.update_series)

    def test_no_dps(self):
        """No series before, no series after call with minimal args"""
        self.assertEqual(DataSeries.objects.all().count(), 0)
        tasks.update_series([])
        self.assertEqual(DataSeries.objects.all().count(), 0)

    def test_task(self):
        tasks.update_series(DataPoint.objects.all())
        series_contents_pks = DataSeries.objects.get(ba=self.ba).datapoints.values_list('pk', flat=True)
        print DataSeries.objects.get(ba=self.ba).datapoints.all()
        self.assertEqual(series_contents_pks, self.best_pks)
