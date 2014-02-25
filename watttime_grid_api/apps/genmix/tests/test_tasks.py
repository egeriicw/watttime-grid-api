from django.test import TestCase
from apps.genmix import tasks


class TestUpdate(TestCase):
    fixtures = ['isos', 'gentypes']

    def test_update(self):
        tasks.update('CAISO', latest=True)
