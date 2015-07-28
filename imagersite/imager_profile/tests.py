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

    def setUp(self):
        pass

    def tearDown(self):
        User.objects.all().delete()

    def test_profile_is_created_when_user_is_saved(self):
        self.assertEqual(len(ImagerProfile.objects.all()), 0)
        user = UserFactory.create()
        user.save()
        self.assertTrue(ImagerProfile.objects.count() == 1)

    def test_create_many_users(self):
        for i in range(100):
            user = UserFactory.create()
            user.save()
        self.assertEqual(len(ImagerProfile.objects.all()), 100)

    def test_profile_str_is_user_username(self):
        user = UserFactory.create(username='user1')
        user.save()
        profile = ImagerProfile.objects.get(user__username='user1')
        self.assertEqual(str(profile), profile.user.username)

    def test_attributes_save(self):
        user = UserFactory.create(username='user0')
        user.save()
        profile = ImagerProfile.objects.get(user__username='user0')
        profile.camera = 'Most amazing camera'
        profile.address = '123 amazing drive'
        profile.website = 'www.amazing.com'
        profile.photography_type = 'amazing'
        profile.save()
        profile = ImagerProfile.objects.get(user__username='user0')
        self.assertEqual('Most amazing camera', profile.camera)

    def test_delete_profile_deletes_user(self):
        user = UserFactory.create(username='user1')
        user.save()
        self.assertEqual(len(ImagerProfile.objects.all()), 1)
        user.profile.delete()
        self.assertEqual(len(User.objects.all()), 0)
