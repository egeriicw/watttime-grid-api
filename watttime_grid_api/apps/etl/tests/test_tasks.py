from django.test import TestCase
from apps.etl import tasks
from apps.genmix.models import Generation
from apps.etl.models import ETLJob


class TestUpdate(TestCase):
    fixtures = ['isos', 'gentypes']

    def test_update_generation(self):
    	# test for blank slate
        self.assertEqual(Generation.objects.filter(mix__ba__abbrev='CAISO').count(), 0)
        self.assertEqual(ETLJob.objects.filter(args__contains='CAISO').count(), 0)

        # run task
        tasks.update_generation('CAISO', latest=True)

        # test for side effects
        job = ETLJob.objects.filter(args__contains='CAISO').latest()
        gens = Generation.objects.filter(mix__ba__abbrev='CAISO')
        self.assertEqual(len(job.errors), 0)
        self.assertTrue(job.success)
        self.assertEqual(job.datapoints.count(), 1)
        self.assertGreater(gens.count(), 0)
        for gen in gens:
	        self.assertEqual(gen.mix.id, job.datapoints.first().id)