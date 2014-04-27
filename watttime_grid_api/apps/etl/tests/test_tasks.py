from django.test import TestCase
from apps.etl import tasks
from apps.genmix.models import Generation


class TestUpdate(TestCase):
    fixtures = ['isos', 'gentypes']

    def test_update_generation(self):
    	# test for blank slate
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev='CAISO').count(), 0)

        # run task
        tasks.update_generation('CAISO', latest=True)

        # test for side effects
        self.assertGreater(Generation.objects.filter(mix__ba__abbrev='CAISO').count(), 0)
