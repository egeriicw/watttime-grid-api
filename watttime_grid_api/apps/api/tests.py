from django.test import TestCase, Client, TransactionTestCase
from django.contrib.gis.geos import Point
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.marginal.tasks import set_moers
from apps.marginal.models import StructuralModelSet
from apps.api.views import DataPointList
from apps.api.filters import DataPointFilter
from datetime import datetime, timedelta
import pytz


class TestDocs(TestCase):
    def test_docs(self):
        c = Client()
        response = c.get('/api/v1/docs/')
        self.assertEqual(response.status_code, 200)
        for test_str in ['swagger-ui-wrap']:
            self.assertIn(test_str, response.content)
            
    def test_datapoint_param_docs(self):
        for filterstr in DataPointFilter._meta.fields:
            self.assertIn(filterstr+' -- ', DataPointList.__doc__)
            

class BAAPITest(APITestCase):
    fixtures = ['bageom.json']
    
    def setUp(self):
        self.base_url = '/api/v1'
        
    def test_get(self):
        url = self.base_url + '/balancing_authorities/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         BalancingAuthority.objects.count())
                         
    def test_filter(self):
        url = self.base_url + '/balancing_authorities/'
        
        queries = [({'abbrev': 'ISONE'}, 1),
                   ({'ba_type': 'ISO'}, 8),
                   ]
        for query, n_expected in queries:
            response = self.client.get(url, data=query)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), n_expected)
            
    def test_geofilter(self):
        url = self.base_url + '/balancing_authorities/'
        
        # Amherst
        point = Point(-72.5196616, 42.3722951)
        
        # formats
        formatted_points = [point.geojson, point.wkt]
        queries = [({'loc': frm}, 1) for frm in formatted_points]
        
        for query, n_expected in queries:
            response = self.client.get(url, data=query)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), n_expected)


class DataPointsAPITest(APITestCase):
    fixtures = ['bageom', 'gentypes', 'fuelcarbonintensities']

    def setUp(self):
        # set up times
        self.now = pytz.utc.localize(datetime.utcnow())
        self.tomorrow = self.now + timedelta(days=1)
        self.yesterday = self.now - timedelta(days=1)
        
        # create sample data points
        for ba in [BalancingAuthority.objects.get(abbrev='ISONE'),
                   BalancingAuthority.objects.get(abbrev='CAISO')]:
            for ts in [self.now, self.yesterday, self.tomorrow]:
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.FIVEMIN)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.IRREGULAR)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.TENMIN)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RTHR, freq=DataPoint.HOURLY)
                                         
        # add sample gens to data points
        for dp in DataPoint.objects.all():
            dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=100)
            dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=200)

        # number of expected objects of different types
        self.n_isos = 2
        self.n_times = 3
        self.n_at_time = 4
        self.n_gen = 2

        # set up routes
        self.base_url = '/api/v1/datapoints/'

        # authenticate client
        username = 'api_user'
        password = 'apipw'
        user = User.objects.create_user(username, 'api_user@example.com', password)
        authenticated = self.client.login(username=username, password=password)
        
    def _run_get(self, url, data, n_expected):
        """boilerplate for testing status and number of objects in get requests"""
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), n_expected)        
        return response
        
    def test_data_created(self):
        self.assertEqual(DataPoint.objects.all().count(),
                         self.n_isos*self.n_times*self.n_at_time)
        self.assertGreater(DataPoint.objects.all(), 1)
        
    def test_get(self):
        """get list"""
        # max per page is 12
        response = self._run_get(self.base_url, {}, 12)
        
        # test keys
        expected_keys = set(['results', 'previous', 'next', 'count'])
        self.assertEqual(expected_keys, set(response.data.keys()))

    def test_filter_ba_abbrev(self):
        """can filter by BA name"""
        n_expected = self.n_times*self.n_at_time
        response = self._run_get(self.base_url,
                                 {'ba': 'CAISO', 'page_size': n_expected},
                                 n_expected) 
                    
        for dp in response.data['results']:
            self.assertEqual(dp['ba'], 'CAISO')
        
    # def test_filter_ba_loc(self):
    #     """FAILING: can filter by location within BA"""
    #     # Amherst
    #     geojson = { "type": "Point",
    #                "coordinates": [ -72.5196616, 42.3722951 ] }
    #     n_expected = self.n_times*self.n_at_time
    #     response = self._run_get(self.base_url,
    #                              {'loc': geojson, 'page_size': n_expected},
    #                              n_expected)
        
    #     for dp in response.data['results']:
    #         self.assertEqual(dp['ba'], 'ISONE')

    def test_multifilter(self):
        """filters should act like AND"""
        pass
        
    def test_get_detail(self):
        """detail returns object with correct data"""
        pk = DataPoint.objects.all()[0].id
        url = self.base_url + '%d/' % pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
        
        # correct field names
        expected_keys = set(['ba', 'timestamp', 'genmix', 'carbon', 'created_at',
                             'url', 'freq', 'market'])
        self.assertEqual(expected_keys, set(response.data.keys()))
            
    def test_filter_start_iso(self):
        # like '2006-10-25T14:30:59+00:00'
        dtstr = self.now.isoformat()

        # start time inclusive
        n_expected = self.n_isos*(self.n_times-1)*self.n_at_time
        response = self._run_get(self.base_url,
                                 {'start_at': dtstr, 'page_size': n_expected},
                                 n_expected)

        for dp in response.data['results']:
            self.assertGreaterEqual(dp['timestamp'], self.now)

    def test_filter_start_day(self):
        # like '2006-10-25'
        dtstr = self.now.strftime('%Y-%m-%d')

        # start time inclusive
        n_expected = self.n_isos*(self.n_times-1)*self.n_at_time
        response = self._run_get(self.base_url,
                                 {'start_at': dtstr, 'page_size': n_expected},
                                 n_expected)
        for dp in response.data['results']:
            self.assertGreaterEqual(dp['timestamp'], self.now)

    def test_filter_start_hmz(self):
        # like '2006-10-25T14:30+0000'
        dtstr = self.now.strftime('%Y-%m-%dT%H:%M%z')

        # start time inclusive
        n_expected = self.n_isos*(self.n_times-1)*self.n_at_time
        response = self._run_get(self.base_url,
                                 {'start_at': dtstr, 'page_size': n_expected},
                                n_expected)
        for dp in response.data['results']:
            self.assertGreaterEqual(dp['timestamp'], self.now)

    def test_filter_start_hmsz(self):
        # like '2006-10-25T14:30:59+0000'
        dtstr = self.now.strftime('%Y-%m-%dT%H:%M:%S%z')
        
        # start time inclusive
        n_expected = self.n_isos*(self.n_times-1)*self.n_at_time
        response = self._run_get(self.base_url,
                                 {'start_at': dtstr, 'page_size': n_expected},
                                n_expected)
                                       
        for dp in response.data['results']:
            self.assertGreaterEqual(dp['timestamp'], self.now)

    def test_filter_end(self):
        # end time inclusive
        n_expected = self.n_isos*(self.n_times-1)*self.n_at_time
        response = self._run_get(self.base_url,
                                 {'end_at': self.now.isoformat(), 'page_size': n_expected},
                                 n_expected)
        for dp in response.data['results']:
            self.assertLessEqual(dp['timestamp'], self.now)
            
    def test_paginate(self):
        for n in range(1, self.n_isos*self.n_times*self.n_at_time):
            response = self._run_get(self.base_url,
                                     {'page_size': n},
                                    n)

    def test_filter_freq(self):
        for freq in ['5m', '1hr', 'n/a', '10m']:
            n_expected = DataPoint.objects.filter(freq=freq, ba__abbrev='CAISO').count()
            self.assertGreater(n_expected, 1)
            self.assertIn(freq, dict(DataPoint.FREQ_CHOICES).keys())
            response = self._run_get(self.base_url,
                                     {'freq': freq, 'ba': 'CAISO', 'page_size': n_expected},
                                    n_expected)
            for dp in response.data['results']:
                self.assertEqual(dp['freq'], freq)
                
    def test_filter_market(self):
        for market in ['RT5M', 'RTHR']:
            n_expected = DataPoint.objects.filter(market=market, ba__abbrev='CAISO').count()
            self.assertGreater(n_expected, 1)
            response = self._run_get(self.base_url,
                                     {'market': market, 'ba': 'CAISO', 'page_size': n_expected},
                                    n_expected)
            for dp in response.data['results']:
                self.assertEqual(dp['market'], market)

class PerformanceTest(TransactionTestCase):
    fixtures = ['bageom', 'gentypes', 'fuelcarbonintensities']

    def setUp(self):
        # set up times
        self.now = pytz.utc.localize(datetime.utcnow())
        self.tomorrow = self.now + timedelta(days=1)
        self.yesterday = self.now - timedelta(days=1)
        
        # create sample data points
        for ba in [BalancingAuthority.objects.get(abbrev='ISONE'),
                   BalancingAuthority.objects.get(abbrev='CAISO')]:
            for ts in [self.now, self.yesterday, self.tomorrow]:
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.FIVEMIN)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.IRREGULAR)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.TENMIN)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RTHR, freq=DataPoint.HOURLY)
                                         
        # add sample gens to data points
        for dp in DataPoint.objects.all():
            dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=100)
            dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=200)

        # number of expected objects of different types
        self.n_isos = 2
        self.n_times = 3
        self.n_at_time = 4
        self.n_gen = 2

        # set up routes
        self.base_url = '/api/v1/datapoints/'

        # authenticate client
        username = 'api_user'
        password = 'apipw'
        User.objects.create_user(username, 'api_user@example.com', password)
        self.client.login(username=username, password=password)

    def test_n_db_calls(self):
        with self.assertNumQueries(7):
            self.client.get(self.base_url)


class DataPointsMOERAPITest(DataPointsAPITest):
    fixtures = ['bageom', 'gentypes', 'silerevans_gen_pjm']

    def setUp(self):
        # set up times
        self.now = pytz.utc.localize(datetime.utcnow())
        self.tomorrow = self.now + timedelta(days=1)
        self.yesterday = self.now - timedelta(days=1)
        
        # create sample data points
        for ba in [BalancingAuthority.objects.get(abbrev='PJM'),
                   BalancingAuthority.objects.get(abbrev='CAISO')]:
            for ts in [self.now, self.yesterday, self.tomorrow]:
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.FIVEMIN)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.IRREGULAR)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RT5M, freq=DataPoint.TENMIN)
                DataPoint.objects.create(timestamp=ts, ba=ba,
                                         market=DataPoint.RTHR, freq=DataPoint.HOURLY)
                                         
        # add sample gens to data points
        for dp in DataPoint.objects.all():
            dp.genmix.create(fuel=FuelType.objects.get(name='wind'), gen_MW=30000)
            dp.genmix.create(fuel=FuelType.objects.get(name='natgas'), gen_MW=60000)

        # add MOER
        sset = StructuralModelSet.objects.first()
        sset.ba = BalancingAuthority.objects.get(abbrev='PJM')
        sset.save()
        set_moers(DataPoint.objects.filter(ba__abbrev='PJM').values_list('pk', flat=True),
                  sset.algorithm.name)

        # number of expected objects of different types
        self.n_isos = 2
        self.n_times = 3
        self.n_at_time = 4
        self.n_gen = 2

        # set up routes
        self.base_url = '/api/v1/marginal/'

        # authenticate client
        username = 'api_user'
        password = 'apipw'
        user = User.objects.create_user(username, 'api_user@example.com', password)
        user.is_staff = True
        user.save()
        authenticated = self.client.login(username=username, password=password)

    def test_get_detail(self):
        """detail returns object with correct data"""
        pk = DataPoint.objects.filter(ba__abbrev='PJM').first().id
        url = self.base_url + '%d/' % pk
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
        
        # correct field names
        expected_keys = set(['ba', 'timestamp', 'genmix', 'moer_set', 'created_at',
                             'url', 'freq', 'market'])
        self.assertEqual(expected_keys, set(response.data.keys()))

        # moer has data
        self.assertEqual(len(response.data['moer_set']), 1)
        self.assertEqual(response.data['moer_set'][0].keys(), ['value', 'units', 'structural_model'])

    def test_must_be_authenticated(self):
        self.client.logout()
        response = self.client.get(self.base_url)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')


class MockView(APIView):
    def get(self, request):
        return Response('foo')


class TestThrottle(APITestCase):
    def setUp(self):
        """
        Reset the cache so that no throttles will be active
        """
        cache.clear()
        self.factory = APIRequestFactory()
        self.n_anon_throttle_requests = 25
        self.n_anon_throttle_rate = 3600 # 1 hour

    def get_throttle_classes(self):
        return MockView().throttle_classes

    def get_throttler(self):
        classes = self.get_throttle_classes()
        first_class = classes[0]
        return first_class()

    def test_anon_throttle_on_by_default(self):
        """Only default throttler should be AnonRateThrottle"""
        throttle_classes = self.get_throttle_classes()
        self.assertEqual(len(throttle_classes), 1)
        self.assertIn(AnonRateThrottle, throttle_classes)

    def test_number_anon_allowed_requests_is_expected(self):
        throttler = self.get_throttler()
        n_requests, n_sec = throttler.parse_rate(throttler.get_rate())
        self.assertEqual(n_requests, self.n_anon_throttle_requests)

    def test_anon_requests_are_throttled(self):
        """
        Ensure request rate is limited for anonymous
        """
        # surpass limit
        request = self.factory.get('/')
        for dummy in range(self.n_anon_throttle_requests+1):
            response = MockView.as_view()(request)

        # response code is 429
        self.assertEqual(429, response.status_code)

    def test_throttle_response(self):
        """
        Error message and header are correct
        """
        # surpass limit
        request = self.factory.get('/')
        for dummy in range(self.n_anon_throttle_requests+1):
            response = MockView.as_view()(request)

        # error message
        msg = "Request was throttled.Expected available in %d seconds." % (self.n_anon_throttle_rate-1)
        self.assertEqual(response.render().data,
                    {"detail": msg})

        # header
        self.assertEqual(response['X-Throttle-Wait-Seconds'], '%d' % self.n_anon_throttle_rate)

    def test_auth_requests_are_not_throttled(self):
        """
        Ensure allowed request rate for user is higher than anonymous rate
        """
        # set up request with token
        User.objects.create_user(username='myname', password='secret')
        user = User.objects.get(username='myname')
        header = "Token %s" % user.auth_token.key
        request = self.factory.get('/', HTTP_AUTHORIZATION=header)

        # test rate
        for dummy in range(self.n_anon_throttle_requests+1):
            response = MockView.as_view()(request)
        self.assertEqual(200, response.status_code)

    def test_throttle_rate_documented(self):
        throttler = self.get_throttler()
        n_requests, n_sec = throttler.parse_rate(throttler.get_rate())
        if n_sec == 3600*24:
            intervalstr = 'day'
        elif n_sec == 3600:
            intervalstr = 'hour'
        elif n_sec == 60:
            intervalstr == 'minute'
        else:
            intervalstr == 'second'
        docstr = '%d views per %s' % (n_requests, intervalstr)

        response = self.client.get('/api/v1/docs/')
        self.assertIn(docstr, response.content)
