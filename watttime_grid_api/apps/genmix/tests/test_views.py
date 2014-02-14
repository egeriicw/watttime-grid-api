from rest_framework import status
from rest_framework.test import APITestCase
from apps.genmix.models import GenMix
from apps.gridentities.models import BalancingAuthority
from datetime import datetime, timedelta
import pytz

class GenMixAPITest(APITestCase):
    fixtures = ['isos.json']

    def setUp(self):
        self.base_url = '/api/v1'
        GenMix.objects.create(ba=BalancingAuthority.objects.get(abbrev='ISNE'),
                              timestamp=pytz.utc.localize(datetime.utcnow()),
                              confidence_type=GenMix.TRUE)
        GenMix.objects.create(ba=BalancingAuthority.objects.get(abbrev='CISO'),
                              timestamp=pytz.utc.localize(datetime.utcnow()),
                              confidence_type=GenMix.FORECAST_GE)
        GenMix.objects.create(ba=BalancingAuthority.objects.get(abbrev='CISO'),
                              timestamp=pytz.utc.localize(datetime.utcnow()) + timedelta(days=1),
                              confidence_type=GenMix.FORECAST_GE)
        GenMix.objects.create(ba=BalancingAuthority.objects.get(abbrev='CISO'),
                              timestamp=pytz.utc.localize(datetime.utcnow()) - timedelta(days=1),
                              confidence_type=GenMix.FORECAST_GE)
        
    def _run_get(self, url, data, n_expected):
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_expected)        

    def test_get(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {},
                      GenMix.objects.count())                         
                         
    def test_filter_where_iso(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {'where': 'CISO'},
                      GenMix.objects.filter(ba__abbrev='CISO').count()) 
            
    def test_filter_how(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {'how': 'best'},
                      GenMix.objects.filter(confidence_type=GenMix.TRUE).count() +
                          GenMix.objects.filter(timestamp__gte=pytz.utc.localize(datetime.utcnow())).count())
        self._run_get(url, {'how': 'true'},
                      GenMix.objects.filter(confidence_type=GenMix.TRUE).count())
