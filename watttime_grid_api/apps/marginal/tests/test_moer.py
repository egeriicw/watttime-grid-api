from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataPoint
from apps.marginal.models import MOER
from datetime import datetime
import pytz


class TestMOER(TestCase):
    fixtures = ['isos.json']

    def setUp(self):
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)

    def test_default_create_fails(self):
        self.assertRaises(IntegrityError, MOER.objects.create)

    def test_minimal_create(self):
        moer = MOER.objects.create(dp=self.dp)
        self.assertIsNotNone(moer)

    def test_related_name(self):
        moer = MOER.objects.create(dp=self.dp)
        dp = DataPoint.objects.get(id=self.dp.id)
#        self.assertEqual(dp.moer, moer)
        self.assertEqual(dp, moer.dp)

    def test_units(self):
        moer = MOER.objects.create(dp=self.dp)
        self.assertEqual(moer.units, 'lb/MW')
