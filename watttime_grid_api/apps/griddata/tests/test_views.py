from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json


class TestMap(TestCase):
    fixtures = ['bageom', 'griddata']

    def test_loads(self):
        """page response has status 200"""
        response = Client().get(reverse('map'))
        self.assertEqual(response.status_code, 200)
        
    def test_geojson_in_context(self):
        """response context has geojson data"""
        # get data
        response = Client().get(reverse('map'))
        data = response.context['geojson']
        
        # test string length
        self.assertGreater(len(data), 0)
        
    def test_geojson_valid(self):
        """geojson data has expected json content"""
        # get data
        response = Client().get(reverse('map'))
        data = response.context['geojson']
        
        # test json
        jsoned = json.loads(data)
        self.assertIn('features', jsoned.keys())
        

class TestDashboard(TestCase):
    fixtures = ['bageom', 'griddata']

    def test_loads(self):
        """page response has status 200"""
        response = Client().get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)        
              