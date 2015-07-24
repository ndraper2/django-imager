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

    @classmethod
    def setUpClass(cls):
        super(ProfileTestCase, cls).setUpClass()
        for i in range(100):
            user = UserFactory.create()
            user.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        super(ProfileTestCase, cls).tearDownClass()

    def test_profile_is_created_when_user_is_saved(self):
        self.assertTrue(ImagerProfile.objects.count() == 100)

    def test_profile_str_is_user_username(self):
        profile = ImagerProfile.objects.get(user__username='user50')
        self.assertEqual(str(profile), profile.user.username)

    def test_delete_user(self):
        profile = User.objects.get(username='user99')
        profile.delete()
        with self.assertRaises(ImagerProfile.DoesNotExist):
            ImagerProfile.objects.get(user__username='user99')

    def test_attributes_save(self):
        profile = ImagerProfile.objects.get(user__username='user0')
        profile.camera = 'Most amazing camera'
        profile.address = '123 amazing drive'
        profile.website = 'www.amazing.com'
        profile.photography_type = 'amazing'
        profile.save()
        self.assertTrue(ImagerProfile.objects.count() == 100)
        self.assertEqual('Most amazing camera', profile.camera)
