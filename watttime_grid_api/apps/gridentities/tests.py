from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from apps.gridentities.models import GridEntity

class EntityTest(TestCase):
    def test_create(self):
        """test creation of every choice"""
        for (choice, verbose) in GridEntity.ENTITY_TYPE_CHOICES:
            ge = GridEntity.objects.create(entity_type=choice, name='test '+verbose)
            self.assertIsNotNone(ge)
            
    def test_choices(self):
        """test that all expected choices exist"""
        choices = set(x[0] for x in GridEntity.ENTITY_TYPE_CHOICES)
        expected_choices = set([GridEntity.ISO, GridEntity.BA, GridEntity.GEN])
        self.assertEqual(choices, expected_choices)
        

class EntityAPITest(APITestCase):
    fixtures = ['isos.json']
    
    def setUp(self):
        self.base_url = '/api/v1'
        
    def test_get(self):
        url = self.base_url + '/balancing_authorities/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         GridEntity.objects.filter(entity_type__in=[GridEntity.BA, GridEntity.ISO]).count())