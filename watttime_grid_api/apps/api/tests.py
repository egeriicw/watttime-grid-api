from django.test import TestCase, Client


class TestDocs(TestCase):
    def test_docs(self):
        c = Client()
        response = c.get('/api/v1/docs/')
        self.assertEqual(response.status_code, 200)
        for test_str in ['django-rest-swagger']:
            self.assertIn(test_str, response.content)
