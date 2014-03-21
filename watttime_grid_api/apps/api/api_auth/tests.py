from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
import views


class TestToken(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_pw'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.token = Token.objects.get()

    def test_key_attr(self):
        self.assertEqual(len(self.token.key), 40)
        self.assertTrue(self.token.key.isalnum())

    def test_user_attr(self):
        self.assertEqual(self.token.user, self.user)

    def test_related_name(self):
        self.assertEqual(self.token, self.user.auth_token)
        

class TestAPIViews(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_pw'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.obtain_token_view_name = 'obtain-token-auth'
        self.reset_token_view_name = 'reset-token-auth'

    def test_token_autocreate(self):
        """API tokens autocreate on user creation"""
        self.assertEqual(Token.objects.filter(user__username='other_user').count(), 0)
        u = User.objects.create_user('other_user', 'other@example.com', 'otherpw')
        self.assertEqual(Token.objects.filter(user__username='other_user').count(), 1)

    def test_obtain_token_success(self):
        # set up payload for post
        payload = {'username': self.username, 'password': self.password}

        # make request
        c = Client()
        response = c.post(reverse(self.obtain_token_view_name), data=payload)

        # test response
        self.assertEqual(['token'], response.data.keys())
        self.assertEqual(response.data['token'], Token.objects.get(user=self.user).key)

    def test_obtain_token_no_username(self):
        c = Client()
        response = c.post(reverse(self.obtain_token_view_name),
                            {'password': 'string'})
        self.assertEqual(response.data['username'], ["This field is required."])
        self.assertEqual(len(response.data.keys()), 1)

    def test_obtain_token_no_password(self):
        c = Client()
        response = c.post(reverse(self.obtain_token_view_name),
                            {'username': 'string'})
        self.assertEqual(response.data['password'], ["This field is required."])
        self.assertEqual(len(response.data.keys()), 1)
 
    def test_obtain_token_bad_credentials(self):
        c = Client()
        response = c.post(reverse(self.obtain_token_view_name),
                            {'username': 'no_user', 'password': 'no_pw'})
        self.assertEqual(response.data['non_field_errors'],
                        ["Unable to login with provided credentials."])
        self.assertEqual(response.data.keys(), ['non_field_errors'])

    def test_reset_token_success(self):
        # set up payload for post
        payload = {'username': self.username, 'password': self.password}
        old_token = Token.objects.get(user=self.user).key

        # make request
        c = Client()
        response = c.post(reverse(self.reset_token_view_name), data=payload)

        # test response
        new_token = Token.objects.get(user=self.user).key
        self.assertIn('token', response.data.keys())
        self.assertEqual(response.data['token'], new_token)
        self.assertIn('reset_success', response.data.keys())
        self.assertEqual(response.data['reset_success'], True)
        self.assertEqual(len(response.data.keys()), 2)

        # test token is new
        self.assertNotEqual(old_token, new_token)


class TestDetailView(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_pw'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.c = Client()

    def test_view_requires_login(self):
        response = self.c.get(reverse('token-detail'))
        self.assertRedirects(response, reverse('auth_login')+"?next="+reverse('token-detail'))

    def test_token_shown(self):
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(reverse('token-detail'))
        token = self.user.auth_token
        self.assertIn(token.key, response.content)

    def test_reset_link(self):
        self.c.login(username=self.username, password=self.password)
        response = self.c.get(reverse('token-detail'))
        self.assertIn(reverse('token-reset'), response.content)


class TestResetView(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_pw'
        self.user = User.objects.create_user(self.username, 'test@example.com', self.password)
        self.c = Client()
        self.factory = RequestFactory()

    def test_view_requires_login(self):
        response = self.c.post(reverse('token-reset'))
        self.assertRedirects(response, reverse('auth_login')+"?next="+reverse('token-reset'))

    def test_post_allowed(self):
        self.assertIn('post', views.TokenReset().http_method_names)

    def test_redirect_to_detail(self):
        request = self.factory.post(reverse('token-reset'))
        request.user = self.user
        response = views.TokenReset.as_view()(request)
        self.assertEqual(response.url, reverse('token-detail'))

    def test_token_reset(self):
        # get old token
        old_token = Token.objects.get(user=self.user)

        # carry out request
        request = self.factory.post(reverse('token-reset'))
        request.user = self.user
        response = views.TokenReset.as_view()(request)

        # test
        new_token = Token.objects.get(user=self.user)
        self.assertNotEqual(old_token, new_token)
