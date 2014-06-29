from django.test import TestCase
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import CurrentDataSet, DataPoint
from apps.griddata import tasks
from datetime import datetime, timedelta
import pytz


class TestUpdateCurrentSet(TestCase):
    fixtures = ['isos']

    def setUp(self):
        now = pytz.utc.localize(datetime.utcnow())
        past = now-timedelta(hours=1)
        future = now+timedelta(hours=1)
        self.ba = BalancingAuthority.objects.first()
        dp_5m_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.FIVEMIN,
                                      ba=self.ba, market=DataPoint.RT5M)
        dp_da_past = DataPoint.objects.create(timestamp=past, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.DAHR)
        dp_5m_now = DataPoint.objects.create(timestamp=now, freq=DataPoint.FIVEMIN,
                                      ba=self.ba, market=DataPoint.RT5M)
        dp_da_now = DataPoint.objects.create(timestamp=now, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.DAHR)
        dp_da_future = DataPoint.objects.create(timestamp=future, freq=DataPoint.HOURLY,
                                      ba=self.ba, market=DataPoint.DAHR)
        self.past_pks = [dp_5m_now.pk, dp_5m_past.pk]
        self.forecast_pks = [dp_da_future.pk]
        self.current = dp_5m_now

    def test_failing_default(self):
        """Raises TypeError with no args"""
        self.assertRaises(TypeError, tasks.update_current_set)

    def test_no_dps(self):
        """No series before, no series after call with minimal args"""
        self.assertEqual(CurrentDataSet.objects.all().count(), 0)
        tasks.update_current_set([])
        self.assertEqual(CurrentDataSet.objects.all().count(), 0)

    def test_task_past(self):
        tasks.update_current_set(DataPoint.objects.all())
        pks = [dp.pk for dp in CurrentDataSet.objects.get(ba=self.ba).past.all()]
        self.assertEqual(pks, self.past_pks)

    def test_task_forecast(self):
        tasks.update_current_set(DataPoint.objects.all())
        pks = [dp.pk for dp in CurrentDataSet.objects.get(ba=self.ba).forecast.all()]
        self.assertEqual(pks, self.forecast_pks)

    def test_task_current(self):
        tasks.update_current_set(DataPoint.objects.all())
        self.assertEqual(self.current, CurrentDataSet.objects.get(ba=self.ba).current)
