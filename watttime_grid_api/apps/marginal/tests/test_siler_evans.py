from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import FuelType, BalancingAuthority
from apps.griddata.models import DataPoint
from apps.marginal.models import SilerEvansMOER, SilerEvansModel
from .test_base import TestSimpleStructuralModel
from datetime import datetime
import pytz


class TestModel(TestSimpleStructuralModel):
    def create_genmix(self):
        # add generation to data point
        self.dp.genmix.create(fuel=FuelType.objects.get(name='coal'), gen_MW=100)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=300)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=200)

        self.total_gen = 100 + 300 + 200

    def test_input(self):
        """Input value is total generation"""
        # set up dp
        self.create_dp()
        self.create_genmix()
        dp = DataPoint.objects.get()

        # get inputs
        inputs = SilerEvansModel.inputs(dp)

        # should have value = total generation
        self.assertEqual(inputs['bin_value'], self.total_gen)


    def test_predict(self):
        """Prediction is beta"""
        # set up dp
        self.create_dp()
        self.create_genmix()
        dp = DataPoint.objects.get()

        # set up row
        model = SilerEvansModel.objects.create(**self.good_params)

        # get prediction
        prediction = SilerEvansModel.predict(dp)
        self.assertEqual(prediction, model.beta1)


class TestMOER(TestCase):
    fixtures = ['isos.json']

    def setUp(self):
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)

    def test_default_create_fails(self):
        self.assertRaises(IntegrityError, SilerEvansMOER.objects.create)

    def test_minimal_create(self):
        moer = SilerEvansMOER.objects.create(dp=self.dp)
        self.assertIsNotNone(moer)

    def test_related_name(self):
        moer = SilerEvansMOER.objects.create(dp=self.dp)
        dp = DataPoint.objects.get(id=self.dp.id)
#        self.assertEqual(dp.siler_evans_moer, moer)
        self.assertEqual(dp, moer.dp)

    def test_units(self):
        moer = SilerEvansMOER.objects.create(dp=self.dp)
        self.assertEqual(moer.units, 'lb/MW')
