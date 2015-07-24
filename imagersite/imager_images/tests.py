from __future__ import unicode_literals
from django.test import TestCase
import factory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from faker import Faker as fake_factory

fake = fake_factory()


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda x:
                                  '{0}@example.com'.format(x.first_name))
    username = factory.Sequence(lambda n: 'user{}'.format(n))


class ProfileTestCase(TestCase):
    users = []

    @classmethod
    def setUpClass(self):
        for i in range(1000):
            user = UserFactory.create()
            user.save()
            self.users.append(user)

    @classmethod
    def tearDownClass(self):
        pass

    def test_profile_is_created_when_user_is_saved(self):
        self.assertTrue(ImagerProfile.objects.count() == 1000)

    def test_profile_str_is_user_username(self):
        profile = ImagerProfile.objects.get(user__username='user100')
        self.assertEqual(str(profile), profile.user.username)

    def test_delete_user(self):
        profile = User.objects.get(username='user100')
        profile.delete()
        with self.assertRaises(ImagerProfile.DoesNotExist):
            ImagerProfile.objects.get(user__username='user100')

    def test_attributes_save(self):
        profile = ImagerProfile.objects.get(user__username='user0')
        profile.camera = 'Most amazing camera'
        profile.address = '123 amazing drive'
        profile.website = 'www.amazing.com'
        profile.photography_type = 'amazing'
        profile.save()
        self.assertTrue(ImagerProfile.objects.count() == 1000)
        self.assertEqual('Most amazing camera', profile.camera)
