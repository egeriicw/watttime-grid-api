from django.test import TestCase
from django.db import IntegrityError
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataPoint
from apps.marginal.models import SimpleStructuralModel
from datetime import datetime, timedelta
import pytz


class TestSimpleStructuralModel(TestCase):
    fixtures = ['gentypes.json', 'isos.json']

    def setUp(self):
        self.ba = BalancingAuthority.objects.get(pk=1)
        self.ba_other = BalancingAuthority.objects.get(pk=2)
        self.good_params = {'beta1': 1.0, 'min_value': 0, 'max_value': 700, 'ba': self.ba}
        self.good_params_no_ba = {'beta1': 1.0, 'min_value': 0, 'max_value': 700}
        self.bad_params_high_vals = {'beta1': 1.0, 'min_value': 700, 'max_value': 1000, 'ba': self.ba}
        self.bad_params_low_vals = {'beta1': 1.0, 'min_value': 0, 'max_value': 100, 'ba': self.ba}
        self.bad_params_other_ba = {'beta1': 1.0, 'min_value': 0, 'max_value': 700, 'ba': self.ba_other}
        self.bad_params_validafter = {'beta1': 1.0, 'min_value': 0, 'max_value': 700, 'ba': self.ba,
                                      'valid_after': pytz.utc.localize(datetime.utcnow())+timedelta(hours=1)}
        self.good_inputs = {'bin_value': 600}

    def create_dp(self):
        # create dp
        self.dp = DataPoint.objects.create(timestamp=pytz.utc.localize(datetime.utcnow()),
                                           ba=self.ba)
    def test_default_create(self):
        """
        Structural model needs a beta and min/max vals
        """
        row = SimpleStructuralModel.objects.create(**self.good_params_no_ba)
        self.assertIsNotNone(row)

    def test_can_create_with_ba(self):
        """
        Structural model can have foreign key to BA
        """
        row = SimpleStructuralModel.objects.create(**self.good_params)
        self.assertIsNotNone(row)

    def test_unique_together(self):
        """One row for each (ba, bin). FAILING need validate_unique"""
        row = SimpleStructuralModel.objects.create(**self.good_params)

        # different BA, should pass
        different = SimpleStructuralModel.objects.create(**self.bad_params_other_ba)
        self.assertNotEqual(row, different)

        # same BA, should fail
        self.assertRaises(IntegrityError,
                          SimpleStructuralModel.objects.create,
                          **self.good_params)

    def test_cannot_match_dp_to_row_with_missing_inputs(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test can't find row for missing input
        bad_inputs = {'wrong_key': 10}
        self.assertRaises(ValueError, SimpleStructuralModel.best_model, dp, bad_inputs)

    def test_cannot_match_dp_to_row_with_wrong_ba(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test can't find row for wrong BA
        SimpleStructuralModel.objects.create(**self.bad_params_other_ba)
        self.assertRaises(ValueError, SimpleStructuralModel.best_model, dp, self.good_inputs)

    def test_cannot_match_dp_to_row_with_late_validafter(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test can't find row for wrong BA
        SimpleStructuralModel.objects.create(**self.bad_params_validafter)
        self.assertRaises(ValueError, SimpleStructuralModel.best_model, dp, self.good_inputs)

    def test_cannot_match_dp_to_row_with_high_vals(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

         # test can't find row for wrong values
        SimpleStructuralModel.objects.create(**self.bad_params_high_vals)
        self.assertRaises(ValueError, SimpleStructuralModel.best_model, dp, self.good_inputs)

    def test_cannot_match_dp_to_row_with_low_vals(self):
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

         # test can't find row for wrong values
        SimpleStructuralModel.objects.create(**self.bad_params_low_vals)
        self.assertRaises(ValueError, SimpleStructuralModel.best_model, dp, self.good_inputs)

    def test_can_match_dp_to_row(self):
        """Given a DataPoint, can identify the matching row of the structural model"""
        # set up dp
        self.create_dp()
        dp = DataPoint.objects.get()

        # test correct row can be found
        matching_row = SimpleStructuralModel.objects.create(**self.good_params)
        found_row = SimpleStructuralModel.best_model(dp, self.good_inputs)
        self.assertEqual(matching_row, found_row)

    def test_output(self):
        """Output is beta"""
        row = SimpleStructuralModel.objects.create(**self.good_params)
        self.assertEqual(row.output(), row.beta1)

    def test_valid_after(self):
        """Default is now"""
        row = SimpleStructuralModel.objects.create(**self.good_params)
        self.assertLess(row.valid_after, pytz.utc.localize(datetime.utcnow()))        
