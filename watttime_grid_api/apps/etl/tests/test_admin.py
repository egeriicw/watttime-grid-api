from django.test import TestCase
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.carbon.models import Carbon
from apps.etl.models import ETLJob


class TestAdmin(TestCase):
    fixtures = ['isos', 'gentypes', 'fuelcarbonintensities']

    def setUp(self):
        self.job = ETLJob.objects.create()

        # create dps
        self.job.datapoints.create(ba=BalancingAuthority.objects.first(),
                                    timestamp=self.job.created_at)
        self.job.datapoints.create(ba=BalancingAuthority.objects.last(),
                                    timestamp=self.job.created_at)

        # create gens
        self.job.datapoints.first().genmix.create(gen_MW=100,
                                                    fuel=FuelType.objects.first())
        self.job.datapoints.first().genmix.create(gen_MW=200,
                                                    fuel=FuelType.objects.last())

        # create carbon
        c = Carbon.objects.create(dp=self.job.datapoints.first())
        c.set_carbon()
        c.save()

        # create moer
        self.job.datapoints.first().moer_set.create()


    def test_dp_links(self):
        links = self.job.datapoints_admin_links()
        self.assertEqual(len(links), 2)
        for link in links:
            self.assertIn('/admin/griddata/datapoint/', link)
            self.assertIn('<a href=', link)
            self.assertIn('</a>', link)

    def test_gen_links(self):
        links = self.job.gen_admin_links()
        self.assertEqual(len(links), 2)
        for link in links:
            self.assertIn('/admin/genmix/generation/', link)
            self.assertIn('<a href=', link)
            self.assertIn('</a>', link)

    def test_carbon_links(self):
        links = self.job.carbon_admin_links()
        self.assertEqual(len(links), 1)
        for link in links:
            self.assertIn('/admin/carbon/carbon/', link)
            self.assertIn('<a href=', link)
            self.assertIn('</a>', link)

    def test_moer_links(self):
        links = self.job.moer_admin_links()
        self.assertEqual(len(links), 1)
        for link in links:
            self.assertIn('/admin/marginal/moer/', link)
            self.assertIn('<a href=', link)
            self.assertIn('</a>', link)
