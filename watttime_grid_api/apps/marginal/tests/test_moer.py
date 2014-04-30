from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.marginal.models import MOER, StructuralModelSet, MOERAlgorithm
from datetime import datetime
import pytz


class TestMOER(TestCase):
    fixtures = ['isos', 'gentypes']

    def setUp(self):
        # data point
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=100)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=200)

        # structural model
        self.alg = MOERAlgorithm.objects.create(binner=MOERAlgorithm.TOTAL_GEN,
                                                predictor=MOERAlgorithm.BETA,
                                                name=MOERAlgorithm.SILEREVANS_GEN)
        self.sset = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.alg)
        self.sset.models().create(beta1=1, min_value=1, max_value=400)


    def test_default_create_fails(self):
        self.assertRaises(IntegrityError, MOER.objects.create)

    def test_minimal_create(self):
        moer = MOER.objects.create(dp=self.dp)
        self.assertIsNotNone(moer)

    def test_related_name(self):
        moer = MOER.objects.create(dp=self.dp)
        dp = DataPoint.objects.get(id=self.dp.id)
        self.assertEqual(dp.moer_set.first(), moer)
        self.assertEqual(dp, moer.dp)

    def test_units(self):
        moer = MOER.objects.create(dp=self.dp)
        self.assertEqual(moer.units, 'lb/MW')

    def test_compute_fails_without_sm(self):
        moer = MOER.objects.create(dp=self.dp)
        self.assertRaises(AttributeError, moer.compute)

    def test_compute_success_with_sm(self):
        moer = MOER.objects.create(dp=self.dp, structural_model=self.sset)
        val = moer.compute()

        # val should be beta1
        self.assertEqual(val, 1)

    def test_set(self):
        moer = MOER.objects.create(dp=self.dp, structural_model=self.sset)
        self.assertIsNone(moer.value)

        # after setting, val should be set on saved moer
        moer.set()
        self.assertEqual(MOER.objects.get(pk=moer.pk).value, 1)
