from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import views


class TestDetailView(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_pw'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.c = Client()
        self.view_name = 'profile'

    def test_view_requires_login(self):
        response = self.c.get(reverse(self.view_name))
        self.assertRedirects(response, reverse('auth_login')+"?next="+reverse(self.view_name))

    def test_view_displays_username(self):
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(reverse(self.view_name))
        self.assertIn(self.username, response.content)

    def test_view_displays_email(self):
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(reverse(self.view_name))
        self.assertIn(self.email, response.content)

    def test_view_displays_pw_change(self):
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(reverse(self.view_name))
        self.assertIn(reverse('password_change'), response.content)
