from __future__ import unicode_literals
from django.test import TestCase
from django.test import Client
import factory
from django.contrib.auth.models import User
from django.core import mail
from imager_profile.models import ImagerProfile


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = 'bob'
    last_name = 'wehadababyitsaboy'
    email = 'bob@example.com'
    username = 'userbob'


class LoginOutTestCase(TestCase):
    def setUp(self):
        user = UserFactory()
        user.set_password('secret')
        user.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_login(self):
        c = Client()
        response = c.get('/')
        self.assertIn("Log In", response.content)
        response = c.post('/login/',
                          {'username': 'userbob', 'password': 'secret'},
                          follow=True)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='userbob')
        self.assertIn(user.username, response.content)

    def test_logout(self):
        c = Client()
        c.login(username='userbob', password='secret')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log In', response.content)

    def test_login_no_user(self):
        c = Client()
        response = c.post('/login/',
                          {'username': 'notthere', 'password': 'secret'})
        # return to login page
        self.assertIn('form method="post" action="/login/"',
                      response.content)


class RegisterTestCase(TestCase):
    def setUp(self):
        user = UserFactory()
        user.set_password('secret')
        user.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_register(self):
        c = Client()
        response = c.post(
            '/accounts/register/',
            {
                'username': 'user1',
                'email': 'bob@example.com',
                'password1': 'secret',
                'password2': 'secret',
            },
            follow=True)
        self.assertIn('check your email to complete the registration',
                      response.content)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Account activation on example.com')
        profile = ImagerProfile.objects.get(user__username='user1')
        self.assertEqual(profile.is_active, False)

    def test_register_already_exists(self):
        c = Client()
        response = c.post(
            '/accounts/register/',
            {
                'username': 'userbob',
                'email': 'bob@example.com',
                'password1': 'secret',
                'password2': 'secret',
            },
            follow=True)
        self.assertIn('<input id="id_password1"', response.content)
