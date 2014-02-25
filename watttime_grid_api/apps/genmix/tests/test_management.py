from django.core.management import call_command
from django.test import TestCase
from apps.genmix.models import Generation


class TestCommand(TestCase):
    fixtures = ['isos', 'gentypes']
    
    def _run_test(self, ba_name, **kwargs):
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev=ba_name).count(), 0)
        call_command('update_generation', ba_name, **kwargs)
        self.assertGreater(Generation.objects.filter(mix__ba__abbrev=ba_name).count(), 0)
            
    def test_no_kwargs(self):
        for ba_name in ['CAISO', 'ISONE', 'PJM', 'SPP', 'MISO']:
            self._run_test(ba_name)
        
        self.assertRaises(ValueError, self._run_test, 'BPA')
        
    def test_market_kwargs(self):
        self._run_test('BPA', market='RT5M')
        