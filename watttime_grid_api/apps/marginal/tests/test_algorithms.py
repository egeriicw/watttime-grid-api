from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import FuelType, BalancingAuthority
from apps.griddata.models import DataPoint
from apps.marginal.models import MOERAlgorithm
from collections import namedtuple
from datetime import datetime
import pytz


MockModel = namedtuple('MockModel', ['beta1'])


class TestBaseAlgorithm(TestCase):
    fixtures = ['gentypes.json', 'isos.json']
    def setUp(self):
        # BAs
        self.ba = BalancingAuthority.objects.get(pk=1)

        # create dp
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)

        # add generation to data point
        self.dp.genmix.create(fuel=FuelType.objects.get(name='coal'), gen_MW=100)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=300)
        self.dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=200)
        self.total_gen = 100 + 300 + 200

        # add load to data point
        self.dp.load_set.create(value=123)
        self.total_load = 123

        # set up mocks
        self.mock_model = MockModel(beta1=1000)

    def test_unique_together(self):
        """binner and predictor should be unique together"""
        # clear
        MOERAlgorithm.objects.all().delete()

        # first alg
        MOERAlgorithm.objects.create(name='test1', binner='testbin1', predictor='testpred1')

        # ok to add with different predictor
        MOERAlgorithm.objects.create(name='test2', binner='testbin1', predictor='testpred2')

        # ok to add with different binner
        MOERAlgorithm.objects.create(name='test3', binner='testbin2', predictor='testpred1')

        # not ok to add with same bin+pred
        self.assertRaises(IntegrityError, MOERAlgorithm.objects.create, name='test4', binner='testbin1', predictor='testpred1')

    def test_unique_name(self):
        # clear
        MOERAlgorithm.objects.all().delete()

        # first alg
        MOERAlgorithm.objects.create(name='test1', binner='testbin1', predictor='testpred1')

        # not ok to add with same name
        self.assertRaises(IntegrityError, MOERAlgorithm.objects.create, name='test1', binner='testbin2', predictor='testpred2')

    def test_predict(self):
        """Integration test"""
        # set up row
        try:
            algorithm = self.create_algorithm()
        except AttributeError: # on base
            return True

        # get prediction
        prediction = algorithm.predict(dp=self.dp, model=self.mock_model)
        self.assertEqual(prediction, algorithm.prediction_result(model=self.mock_model))


class TestSilerEvansGen(TestBaseAlgorithm):
    def create_algorithm(self):
        return MOERAlgorithm.objects.create(name=MOERAlgorithm.SILEREVANS_GEN,
                             binner=MOERAlgorithm.TOTAL_GEN,
                             predictor=MOERAlgorithm.BETA)

    def test_bin_value(self):
        """
        Bin value is total generation
        """
        algorithm = self.create_algorithm()
        
        # get inputs
        inputs = algorithm.bin_value(dp=self.dp)

        # should have value = total generation
        self.assertEqual(inputs['bin_value'], self.total_gen)

    def test_prediction_result(self):
        """Prediction is beta"""
        # set up row
        algorithm = self.create_algorithm()

        # get prediction
        prediction = algorithm.prediction_result(model=self.mock_model)
        self.assertEqual(prediction, self.mock_model.beta1)


class TestSilerEvans(TestBaseAlgorithm):
    def create_algorithm(self):
        return MOERAlgorithm.objects.create(name=MOERAlgorithm.SILEREVANS,
                             binner=MOERAlgorithm.TOTAL_LOAD,
                             predictor=MOERAlgorithm.BETA)

    def test_bin_value(self):
        """
        Bin value is total load
        TODO: failing because load not implemented
        """
        algorithm = self.create_algorithm()
        
       # get inputs
        inputs = algorithm.bin_value(dp=self.dp)

        # should have value = total generation
        self.assertEqual(inputs['bin_value'], self.total_load)

    def test_prediction_result(self):
        """Prediction is beta"""
        # set up row
        algorithm = self.create_algorithm()

        # get prediction
        prediction = algorithm.prediction_result(model=self.mock_model)
        self.assertEqual(prediction, self.mock_model.beta1)

