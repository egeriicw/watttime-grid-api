from rest_framework import status
from rest_framework.test import APITestCase
from apps.genmix.models import DataSeries
from apps.gridentities.models import BalancingAuthority
from datetime import datetime, timedelta
import pytz

class GenMixAPITest(APITestCase):
    fixtures = ['isos.json']

    def setUp(self):
        self.base_url = '/api/v1'
        now = pytz.utc.localize(datetime.utcnow())
        tomorrow = now + timedelta(days=1)
        yesterday = now - timedelta(days=1)
        self.isne_true = DataSeries.objects.create(ba=BalancingAuthority.objects.get(abbrev='ISNE'),
                                  series_type=DataSeries.HISTORICAL)
        self.ciso_forecast = DataSeries.objects.create(ba=BalancingAuthority.objects.get(abbrev='CISO'),
                                  series_type=DataSeries.BEST)
        for ds in [self.isne_true, self.ciso_forecast]:
            for ts in [now, yesterday, tomorrow]:
                ds.datapoints.create(timestamp=ts)
        
    def _run_get(self, url, data, n_expected):
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_expected)        

    def test_get(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {}, 2)                         
                         
    def test_filter_where_iso(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {'where': 'CISO'}, 1) 
            
    def test_filter_how(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {'how': 'best'}, 1)
        self._run_get(url, {'how': 'past'}, 1)
                      
    def test_multifilter(self):
        url = self.base_url + '/genmix/'
        self._run_get(url, {'how': 'best', 'where': 'ISNE'}, 0)
        self._run_get(url, {'how': 'best', 'where': 'CISO'}, 1)
        self._run_get(url, {'how': 'past', 'where': 'ISNE'}, 1)
        self._run_get(url, {'how': 'past', 'where': 'CISO'}, 0)
        
