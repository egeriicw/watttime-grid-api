from django.core.management import call_command
from django.test import TestCase
from apps.supply_demand.models import Generation
from apps.etl.models import ETLJob
from datetime import datetime


class TestCommand(TestCase):
    fixtures = ['isos', 'gentypes', 'fuelcarbonintensities']
    
    def _run_test(self, ba_name, **kwargs):
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev=ba_name).count(), 0)
        call_command('update_generation', ba_name, **kwargs)
        self.assertGreater(Generation.objects.filter(mix__ba__abbrev=ba_name).count(), 0)
            
    def test_passing_CAISO_no_kwargs(self):
        self._run_test('CAISO')

    def test_passing_ISONE_no_kwargs(self):
        self._run_test('ISONE')

    def test_passing_MISO_no_kwargs(self):
        self._run_test('MISO')

    def test_passing_PJM_no_kwargs(self):
        self._run_test('PJM')

    def test_failing_SPP_no_kwargs(self):
        """SPP gets no data"""
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev='SPP').count(), 0)
        call_command('update_generation', 'SPP')
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev='SPP').count(), 0)
        
    def test_failing_BPA_wo_kwargs(self):
        call_command('update_generation', 'BPA')
        job = ETLJob.objects.filter(args__contains='BPA').latest()
        self.assertIn('Market must be RT5M', job.errors)
        self.assertFalse(job.success)
        
    def test_BPA_requires_kwargs(self):
        self._run_test('BPA', market='RT5M')
        job = ETLJob.objects.filter(args__contains='BPA').latest()
        self.assertEqual(len(job.errors), 0)
        self.assertTrue(job.success)

    def test_NYISO_fails(self):
        call_command('update_generation', 'NYISO')
        job = ETLJob.objects.filter(args__contains='NYISO').latest()
        self.assertIn('No client found for name NYISO', job.errors)
        self.assertFalse(job.success)

    def test_ERCOT_fails_before_min33(self):
        if datetime.now().minute > 33:
            self._run_test('ERCOT')
        else:
            self.assertRaises(AssertionError, self._run_test, 'ERCOT')
