from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.core import mail


username = 'me'
password = 'mypw'
email = 'me@example.com'

def construct_activate_url(context):
	try:
		payload = {'activation_key': context[0].get('activation_key')}
	except KeyError:
		payload = {'activation_key': context[1].get('activation_key')}

	url = reverse('registration_activate', kwargs=payload)
	return url, payload

class TestRegistration(TestCase):
	def setUp(self):
		self.c = Client()
		self.good_payload = {'username': username, 'email': email,
					'password1': password, 'password2': password}

	def test_mismatched_pw(self):
		payload = {'username': username, 'email': email,
					'password1': 'pw1', 'password2': 'pw2'}
		response = self.c.post(reverse('registration_register'), payload)
		self.assertIn("The two password fields didn't match", response.content)

	def test_repeat_email_fails(self):
		# create user with different username and same email
		old_user = User.objects.create_user('othername', email, 'otherpw')

		# try to register
		response = self.c.post(reverse('registration_register'), self.good_payload)

		# new user not created
		self.assertEqual(User.objects.filter(email=email).count(), 1)
		self.assertEqual(User.objects.get(email=email).username, 'othername')

		# error in response
		self.assertIn("This email address is already in use", response.content)

	def test_success_redirects_to_complete(self):
		response = self.c.post(reverse('registration_register'), self.good_payload)
		self.assertRedirects(response, reverse('registration_complete'))

	def test_success_creates_inactive_user(self):
		response = self.c.post(reverse('registration_register'), self.good_payload)
		u = User.objects.get(username=username)
		self.assertIsNotNone(u)
		self.assertFalse(u.is_active)

	def test_success_sends_email(self):
		response = self.c.post(reverse('registration_register'), self.good_payload)
		self.assertEqual(len(mail.outbox), 1)

	def test_email_content(self):
		response = self.c.post(reverse('registration_register'), self.good_payload)
		self.assertEqual('Activate your account for the WattTime Impact API', mail.outbox[0].subject)
		self.assertIn('activate', mail.outbox[0].body)
		self.assertIn(reverse('home'), mail.outbox[0].body)
		activate_url, activate_payload = construct_activate_url(response.context)
		self.assertIn(activate_url, mail.outbox[0].body)

	def test_complete(self):
		response = self.c.get(reverse('registration_complete'))
		self.assertIn('A registration email is on the way!', response.content)


class TestActivation(TestCase):
	def setUp(self):
		self.c = Client()
		self.good_payload = {'username': username, 'email': email,
					'password1': password, 'password2': password}
		response = self.c.post(reverse('registration_register'), self.good_payload)
		self.activate_url, self.activate_payload = construct_activate_url(response.context)

	def test_success_redirects_to_complete(self):
		response = self.c.get(self.activate_url)
		self.assertRedirects(response, reverse('registration_activation_complete'))

	def test_success_activates_user(self):
		response = self.c.get(self.activate_url)
		u = User.objects.get(username=username)
		self.assertIsNotNone(u)
		self.assertTrue(u.is_active)

	def test_complete(self):
		response = self.c.get(reverse('registration_activation_complete'))
		self.assertIn('Woohoo, your account is active.', response.content)
