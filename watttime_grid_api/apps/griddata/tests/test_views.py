from rest_framework import status
from rest_framework.test import APITestCase
from apps.griddata.models import DataSeries
from apps.gridentities.models import BalancingAuthority
from datetime import datetime, timedelta
from dateutil.parser import parse as dateutil_parse
import pytz


class SeriesAPITest(APITestCase):
    fixtures = ['isos.json']
    urls = 'apps.griddata.tests.test_urls'

    def setUp(self):
        # create sample data
        self.now = pytz.utc.localize(datetime.utcnow())
        self.tomorrow = self.now + timedelta(days=1)
        self.yesterday = self.now - timedelta(days=1)
        self.isne_true = DataSeries.objects.create(ba=BalancingAuthority.objects.get(abbrev='ISONE'),
                                  series_type=DataSeries.HISTORICAL)
        self.ciso_forecast = DataSeries.objects.create(ba=BalancingAuthority.objects.get(abbrev='CAISO'),
                                  series_type=DataSeries.BEST)
        for ds in [self.isne_true, self.ciso_forecast]:
            for ts in [self.now, self.yesterday, self.tomorrow]:
                ds.datapoints.create(timestamp=ts, ba=ds.ba)

        # set up routes
        self.base_url = '/test_series/'
        
    def _run_get(self, url, data, n_expected):
        """boilerplate for testing status and number of objects in get requests"""
        response = self.client.get(url, data=data)
        if response.status_code is not status.HTTP_200_OK:
            print response.data, url
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
        self._run_get(url, {'ba': 'CAISO'}, 1) 
            
    def test_filter_how(self):
        """filter by how=[series_type]"""
        url = self.base_url
        self._run_get(url, {'series_type': 'BEST'}, 1)
        self._run_get(url, {'series_type': 'PAST'}, 1)
        
    def test_multifilter(self):
        """filters should act like AND"""
        url = self.base_url
        self._run_get(url, {'series_type': 'BEST', 'ba': 'ISONE'}, 0)
        self._run_get(url, {'series_type': 'BEST', 'ba': 'CAISO'}, 1)
        self._run_get(url, {'series_type': 'PAST', 'ba': 'ISONE'}, 1)
        self._run_get(url, {'series_type': 'PAST', 'ba': 'CAISO'}, 0)
        
    def test_get_detail(self):
        """detail returns object with correct data"""
        pk = DataSeries.objects.all()[0].id
        url = self.base_url + '%d/' % pk
        response = self._run_get(url, {}, 3)
        
        # correct field names
        for field in ['datapoints', 'ba', 'series_type']:
            self.assertIn(field, response.data.keys())
            
        # correct number of datapoints
        self.assertEqual(len(response.data['datapoints']), 3)
        
    def test_filter_start(self):
        """filter by start=DATETIME"""
        url = self.base_url
        
        # start time inclusive
        response = self._run_get(url, {'start_at': self.now.isoformat()}, 2)
        for ds in response.data:
            self.assertEqual(len(ds['datapoints']), 2)
            for dp in ds['datapoints']:
                self.assertGreaterEqual(dateutil_parse(dp['timestamp']), self.now)

    def test_filter_end(self):
        """filter by end=DATETIME"""
        url = self.base_url
        
        # end time inclusive
        response = self._run_get(url, {'end_at': self.now.isoformat()}, 2)
        for ds in response.data:
            self.assertEqual(len(ds['datapoints']), 2)
            for dp in ds['datapoints']:
                self.assertLessEqual(dateutil_parse(dp['timestamp']), self.now)
