from django.test import TestCase
from django.db import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase
from apps.gridentities.models import BalancingAuthority, FuelType

class BATest(TestCase):
    def test_create(self):
        """test creation of every choice"""
        for (choice, verbose) in BalancingAuthority.BA_TYPE_CHOICES:
            ba = BalancingAuthority.objects.create(ba_type=choice,
                                                   name='test '+verbose,
                                                   abbrev=choice)
            self.assertIsNotNone(ba)
            
    def test_choices(self):
        """test that all expected choices exist"""
        choices = set(x[0] for x in BalancingAuthority.BA_TYPE_CHOICES)
        expected_choices = set([BalancingAuthority.ISO, BalancingAuthority.BA])
        self.assertEqual(choices, expected_choices)
        
    def test_unique_abbrev(self):
        choice, verbose = BalancingAuthority.BA_TYPE_CHOICES[0]
        ba = BalancingAuthority.objects.create(ba_type=choice,
                                               name='test 1',
                                               abbrev=choice)
        self.assertRaises(IntegrityError, BalancingAuthority.objects.create,
                          ba_type='test', name='test 2', abbrev=choice)
        

class FuelTest(TestCase):
    def test_full_create(self):
        fuel = FuelType(name='coal', description='coal-fired thermal power plant')
        self.assertIsNotNone(fuel)

    def test_default_create(self):
        fuel = FuelType(name='coal')
        self.assertEqual(fuel.description, '')
        
    def test_unique_name(self):
        fuel = FuelType.objects.create(name='coal')
        self.assertRaises(IntegrityError, FuelType.objects.create, name='coal')
        

class BAAPITest(APITestCase):
    fixtures = ['isos.json']
    
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
                   ({'name': 'Midwest ISO'}, 1),
                   ]
        for query, n_expected in queries:
            response = self.client.get(url, data=query)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), n_expected)
            
