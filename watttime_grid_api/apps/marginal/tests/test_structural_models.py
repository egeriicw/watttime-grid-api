from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataPoint
from apps.marginal.models import SimpleStructuralModel, StructuralModelSet, MOERAlgorithm
from datetime import datetime, timedelta
import pytz


class TestStructuralModelSet(TestCase):
    fixtures = ['isos.json']
    def setUp(self):
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.ba_other = BalancingAuthority.objects.get(pk=2)
        self.algorithm = MOERAlgorithm.objects.create(name=MOERAlgorithm.SILEREVANS_GEN,
                                                      binner=MOERAlgorithm.TOTAL_GEN,
                                                      predictor=MOERAlgorithm.BETA)
        self.good_inputs = {'bin_value': 600}

    def create_dp(self):
        # create dp
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)
    #####################
    #### creation
    #####################

    def test_default_create(self):
        sset = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.algorithm)
        self.assertIsNotNone(sset)

    def test_valid_after(self):
        """Default is now"""
        row = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.algorithm)
        self.assertLess(row.valid_after, pytz.utc.localize(datetime.utcnow()))        

    #####################
    #### best manager
    #####################

    def test_cannot_match_dp_to_set_with_wrong_ba(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test can't find set for wrong set
        StructuralModelSet.objects.create(ba=self.ba_other, algorithm=self.algorithm)
        self.assertRaises(ValueError, StructuralModelSet.objects.all().best, dp, self.algorithm.name)

    def test_cannot_match_dp_to_set_with_wrong_alg(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test can't find set for wrong set
        StructuralModelSet.objects.create(ba=self.ba_other, algorithm=self.algorithm)
        self.assertRaises(ValueError, StructuralModelSet.objects.all().best, dp, 'test')

    def test_cannot_match_dp_to_set_with_late_validafter(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test can't find set for wrong dates
        StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm,
            valid_after=pytz.utc.localize(datetime.utcnow())+timedelta(hours=1))
        self.assertRaises(ValueError, StructuralModelSet.objects.all().best, dp, self.algorithm.name)

    def test_can_match_dp_to_set(self):
        """Given a DataPoint, can identify the matching set of structural models"""
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test correct set can be found
        matching_row = StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm)
        found_row = StructuralModelSet.objects.all().best(dp, self.algorithm.name)
        self.assertEqual(matching_row, found_row)
        self.assertIsNotNone(found_row)

    #####################
    #### models
    #####################

    def test_models(self):
        sset = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.algorithm)
        qset = sset.models()
        self.assertEqual(qset.count(), 0)
        qset.create(beta1=1, min_value=1, max_value=2)
        self.assertEqual(qset.count(), 1)

    #####################
    #### best_model
    #####################

    def test_cannot_match_dp_to_row_with_high_vals(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # set up set
        sset = StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm)
        sset.models().create(beta1=1, min_value=1, max_value=2)

         # test can't find row for wrong values
        self.assertRaises(ValueError, sset.best, {'bin_value': 0})

    def test_cannot_match_dp_to_row_with_low_vals(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # set up set
        sset = StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm)
        sset.models().create(beta1=1, min_value=1, max_value=2)

         # test can't find row for wrong values
        self.assertRaises(ValueError, sset.best, {'bin_value': 3})

    def test_cannot_match_dp_to_row_with_missing_inputs(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # set up set
        sset = StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm)
        sset.models().create(beta1=1, min_value=1, max_value=2)

        # test can't find row for missing input
        self.assertRaises(ValueError, sset.best, {'wrong_key': 10})

    def test_cannot_match_dp_to_row_with_no_models(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # set up set
        sset = StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm)
        self.assertEqual(sset.models().count(), 0)

        # test can't find row for no models
        self.assertRaises(ValueError, sset.best, self.good_inputs)

    def test_can_match_dp_to_row_with_good_vals(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # set up set
        sset = StructuralModelSet.objects.create(ba=dp.ba, algorithm=self.algorithm)
        expected_m = sset.models().create(beta1=1, min_value=1, max_value=2)
        wrong_m = sset.models().create(beta1=1, min_value=2, max_value=3)

         # find row for good values
        found_m = sset.best({'bin_value': 1.5})
        self.assertEqual(found_m, expected_m)


class TestSimpleStructuralModel(TestCase):
    fixtures = ['isos.json']

    def setUp(self):
        # BAs
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.ba_other = BalancingAuthority.objects.get(pk=2)

        # sets
        self.algorithm = MOERAlgorithm.objects.create(name='test', binner=MOERAlgorithm.TOTAL_GEN, predictor=MOERAlgorithm.BETA)
        self.set = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.algorithm)
        self.set_other = StructuralModelSet.objects.create(ba=self.ba_other, algorithm=self.algorithm)
        self.set_later = StructuralModelSet.objects.create(ba=self.ba, algorithm=self.algorithm,
            valid_after=pytz.utc.localize(datetime.utcnow())+timedelta(hours=1))

        # params
        self.good_params = {'beta1': 1.0, 'min_value': 0, 'max_value': 700, 'model_set': self.set}
        self.good_params_no_set = {'beta1': 1.0, 'min_value': 0, 'max_value': 700}
        self.bad_params_high_vals = {'beta1': 1.0, 'min_value': 700, 'max_value': 1000, 'model_set': self.set}
        self.bad_params_low_vals = {'beta1': 1.0, 'min_value': 0, 'max_value': 100, 'model_set': self.set}
        self.bad_params_other_set = {'beta1': 1.0, 'min_value': 0, 'max_value': 700, 'model_set': self.set_other}
        self.bad_params_validafter = {'beta1': 1.0, 'min_value': 0, 'max_value': 700, 'model_set': self.set_later}
        self.good_inputs = {'bin_value': 600}

    def create_dp(self):
        # create dp
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)

    def test_failing_minimal_create(self):
        """
        Structural model fails without set
        """
        self.assertRaises(IntegrityError, SimpleStructuralModel.objects.create, **self.good_params_no_set)

    def test_can_create_with_set(self):
        """
        Structural model can have foreign key to model set
        """
        row = SimpleStructuralModel.objects.create(**self.good_params)
        self.assertIsNotNone(row)
