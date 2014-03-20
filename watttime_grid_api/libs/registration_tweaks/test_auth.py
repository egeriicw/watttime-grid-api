from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.core import mail


username = 'me'
password = 'mypw'
email = 'me@example.com'


class TestLogin(TestCase):
	def setUp(self):
		self.c = Client()
		self.u = User.objects.create_user(username, email, password)

	def test_no_password(self):
		payload = {'username': username}
		response = self.c.post(reverse('auth_login'), payload)
		self.assertIn('<div class="form-group has-error"><label>Password</label>',
						response.content)

	def test_no_username(self):
		payload = {'password': password}
		response = self.c.post(reverse('auth_login'), payload)
		self.assertIn('<div class="form-group has-error"><label>Username</label>',
						response.content)

	def test_bad_auth(self):
		payload = {'username': username, 'password': 'bad'}
		response = self.c.post(reverse('auth_login'), payload)
		self.assertIn('<div class="alert alert-danger', response.content)
		self.assertIn('Please enter a correct username and password', response.content)

	def test_success_directs_to_profile(self):
		payload = {'username': username, 'password': password}
		response = self.c.post(reverse('auth_login'), payload)
		self.assertRedirects(response, '/accounts/profile/')

	def test_success_auth(self):
		payload = {'username': username, 'password': password}
		response = self.c.post(reverse('auth_login'), payload)
		self.assertEqual(self.c.session['_auth_user_id'], self.u.pk)


class TestLogout(TestCase):
	def setUp(self):
		self.c = Client()
		self.u = User.objects.create_user(username, email, password)

	def test_success_directs_to_home(self):
		self.c.login(username=username, password=password)
		response = self.c.get(reverse('auth_logout'))
		self.assertRedirects(response, reverse('home'))

	def test_success_auth(self):
		self.c.login(username=username, password=password)
		response = self.c.get(reverse('auth_logout'))
		self.assertNotIn('_auth_user_id', self.c.session.keys())


class TestPasswordChange(TestCase):
	def setUp(self):
		self.c = Client()
		self.u = User.objects.create_user(username, email, password)
		self.new_pw = 'new_pw'
		self.good_payload = {'old_password': password, 'new_password1': self.new_pw, 'new_password2': self.new_pw}
		self.mismatch_new_payload = {'old_password': password, 'new_password1': 'pw1', 'new_password2': 'pw2'}
		self.wrong_old_payload = {'old_password': 'wrong', 'new_password1': self.new_pw, 'new_password2': self.new_pw}

	def test_unauth_redirects_to_login(self):
		response = self.c.post(reverse('password_change'), self.good_payload)
		self.assertRedirects(response, reverse('auth_login')+'?next='+reverse('password_change'))

	def test_mismatch_new(self):
		self.c.login(username=username, password=password)
		response = self.c.post(reverse('password_change'), self.mismatch_new_payload)
		self.assertIn('<div class="form-group has-error"><label>New password confirmation</label>', response.content)
		self.assertIn('<span class=help-block>The two password fields didn&#39;t match.</span>', response.content)

	def test_wrong_old(self):
		self.c.login(username=username, password=password)
		response = self.c.post(reverse('password_change'), self.wrong_old_payload)
		self.assertIn('<div class="form-group has-error"><label>Old password</label>', response.content)
		self.assertIn('<span class=help-block>Your old password was entered incorrectly. Please enter it again.</span>', response.content)

	def test_success_redirects_to_done(self):
		self.c.login(username=username, password=password)
		response = self.c.post(reverse('password_change'), self.good_payload)
		self.assertRedirects(response, reverse('password_change_done'))

	def test_success_pw_changed(self):
		self.c.login(username=username, password=password)
		response = self.c.post(reverse('password_change'), self.good_payload)
		u = User.objects.get(username=username)
		self.assertTrue(u.check_password(self.new_pw))

	def test_done(self):
		self.c.login(username=username, password=password)
		response = self.c.get(reverse('password_change_done'))
		self.assertIn('Success! Your password has been changed.', response.content)


class TestPasswordReset(TestCase):
	def setUp(self):
		self.c = Client()
		self.u = User.objects.create_user(username, email, password)
		self.new_pw = 'new_pw'

	def _post_reset_request(self):
		# post request
		self.c.login(username=username, password=password)
		payload = {'email': email}
		response = self.c.post(reverse('password_reset'), payload)
		return response

	def _construct_confirm_url(self, context):
		try:
			confirm_payload = {'uidb64': context[0].get('uid'),
								'token': context[0].get('token'),}
		except KeyError:
			confirm_payload = {'uidb64': context[1].get('uid'),
								'token': context[1].get('token'),}

		confirm_url = reverse('password_reset_confirm', kwargs=confirm_payload)
		return confirm_url, confirm_payload

	def test_request_success_redirects_to_done(self):
		response = self._post_reset_request()
		self.assertRedirects(response, reverse('password_reset_done'))

	def test_request_success_sends_email(self):
		response = self._post_reset_request()
		self.assertEqual(len(mail.outbox), 1)

	def test_done(self):
		response = self.c.get(reverse('password_reset_done'))
		self.assertIn('A password reset email is on the way!', response.content)

	def test_email_content(self):
		response = self._post_reset_request()
		self.assertEqual('Reset your password for the WattTime Impact API', mail.outbox[0].subject)
		self.assertIn('password reset', mail.outbox[0].body)
		self.assertIn(email, mail.outbox[0].body)
		self.assertIn(reverse('home'), mail.outbox[0].body)
		confirm_url, confirm_payload = self._construct_confirm_url(response.context)
		self.assertIn(confirm_url, mail.outbox[0].body)

	def test_confirm_mismatch_pw(self):
		reset_response = self._post_reset_request()
		confirm_url, confirm_payload = self._construct_confirm_url(reset_response.context)
		confirm_payload.update({'new_password1': 'pw1', 'new_password2': 'pw2'})
		response = self.c.post(confirm_url, confirm_payload)
		self.assertIn('<div class="form-group has-error"><label>New password confirmation</label>', response.content)
		self.assertIn('<span class=help-block>The two password fields didn&#39;t match.</span>', response.content)

	def test_confirm_success_redirects_to_complete(self):
		reset_response = self._post_reset_request()
		confirm_url, confirm_payload = self._construct_confirm_url(reset_response.context)
		confirm_payload.update({'new_password1': self.new_pw, 'new_password2': self.new_pw})
		response = self.c.post(confirm_url, confirm_payload)
		self.assertRedirects(response, reverse('password_reset_complete'))

	def test_confirm_success_pw_changed(self):
		reset_response = self._post_reset_request()
		confirm_url, confirm_payload = self._construct_confirm_url(reset_response.context)
		confirm_payload.update({'new_password1': self.new_pw, 'new_password2': self.new_pw})
		response = self.c.post(confirm_url, confirm_payload)
		u = User.objects.get(username=username)
		self.assertTrue(u.check_password(self.new_pw))

	def test_complete(self):
		response = self.c.get(reverse('password_reset_complete'))
		self.assertIn('Woohoo, your password has been reset.', response.content)
