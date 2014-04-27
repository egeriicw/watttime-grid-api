from django.core.management import call_command
from django.test import TestCase
from apps.genmix.models import Generation
from apps.gridentities.models import BalancingAuthority
from datetime import datetime


class TestCommand(TestCase):
    fixtures = ['isos', 'gentypes', 'fuelcarbonintensities']
    
    def _run_test(self, ba_name, **kwargs):
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev=ba_name).count(), 0)
        call_command('update_generation', ba_name, **kwargs)
        self.assertGreater(Generation.objects.filter(mix__ba__abbrev=ba_name).count(), 0)
            
    def test_no_kwargs(self):
        # get non-special-case ISO names
        special_cases = ['BPA', 'NYISO', 'ERCOT']
        ba_names = BalancingAuthority.objects.exclude(abbrev__in=special_cases).values_list('abbrev', flat=True)

        for ba_name in ba_names:
            self._run_test(ba_name)
        
    def test_failing_BPA_wo_kwargs(self):
        self.assertRaises(ValueError, self._run_test, 'BPA')
        
    def test_BPA_requires_kwargs(self):
        self._run_test('BPA', market='RT5M')

    def test_NYISO_fails(self):
        self.assertRaises(ValueError, self._run_test, 'NYISO')

    def test_ERCOT_fails_before_min33(self):
        if datetime.now().minute > 33:
            self._run_test('ERCOT')
        else:
            self.assertRaises(AssertionError, self._run_test, 'ERCOT')
