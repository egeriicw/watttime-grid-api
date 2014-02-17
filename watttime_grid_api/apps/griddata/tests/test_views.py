from rest_framework import status
from rest_framework.test import APITestCase
from apps.griddata.models import DataSeries
from apps.gridentities.models import BalancingAuthority
from datetime import datetime, timedelta
import pytz


class SeriesAPITest(APITestCase):
    fixtures = ['isos.json']
    urls = 'apps.griddata.tests.test_urls'

    def setUp(self):
        # create sample data
        now = pytz.utc.localize(datetime.utcnow())
        tomorrow = now + timedelta(days=1)
        yesterday = now - timedelta(days=1)
        self.isne_true = DataSeries.objects.create(ba=BalancingAuthority.objects.get(abbrev='ISNE'),
                                  series_type=DataSeries.HISTORICAL)
        self.ciso_forecast = DataSeries.objects.create(ba=BalancingAuthority.objects.get(abbrev='CISO'),
                                  series_type=DataSeries.BEST)
        for ds in [self.isne_true, self.ciso_forecast]:
            for ts in [now, yesterday, tomorrow]:
                ds.datapoints.create(timestamp=ts, ba=ds.ba)

        # set up routes
        self.base_url = '/test_series/'
        
    def _run_get(self, url, data, n_expected):
        """boilerplate for testing status and number of objects in get requests"""
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), n_expected)        
        return response
        
    def test_get(self):
        """simple get should find the two objects created in setUp"""
        url = self.base_url
        self._run_get(url, {}, 2)
                         
    def test_filter_where_iso(self):
        """filter by where=[BalancingAuthority.abbrev]"""
        url = self.base_url
        self._run_get(url, {'where': 'CISO'}, 1) 
            
    def test_filter_how(self):
        """filter by how=[series_type]"""
        url = self.base_url
        self._run_get(url, {'how': 'best'}, 1)
        self._run_get(url, {'how': 'past'}, 1)
                      
    def test_multifilter(self):
        """filters should act like AND"""
        url = self.base_url
        self._run_get(url, {'how': 'best', 'where': 'ISNE'}, 0)
        self._run_get(url, {'how': 'best', 'where': 'CISO'}, 1)
        self._run_get(url, {'how': 'past', 'where': 'ISNE'}, 1)
        self._run_get(url, {'how': 'past', 'where': 'CISO'}, 0)
        
    def test_get_detail(self):
        """detail returns object with correct data"""
        url = self.base_url + '1/'
        response = self._run_get(url, {}, 3)
        
        # correct field names
        for field in ['datapoints', 'ba', 'series_type']:
            self.assertIn(field, response.data.keys())
            
        # correct number of datapoints
        self.assertEqual(len(response.data['datapoints']), 3)
        
