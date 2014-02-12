from django.test import TestCase
from .models import GridEntity

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