from __future__ import unicode_literals
from django.test import TestCase
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
from faker import Faker as fake_factory
from django.test import Client
from imager_images.models import Photo, Album

fake = fake_factory()


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda x:
                                  '{0}@example.com'.format(x.first_name))
    username = factory.Sequence(lambda n: 'user{}'.format(n))


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo
    title = fake.sentences(nb=1)[0]
    description = fake.text()
    file = fake.mime_type()


class AlbumFactory(DjangoModelFactory):
    class Meta:
        model = Album
    title = fake.sentences(nb=1)[0]
    description = fake.text()


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


class ProfileViewTestCase(TestCase):
    def setUp(self):
        user = UserFactory(username='userbob', email='bob@example.com')
        user.set_password('secret')
        user.save()
        user.profile.camera = 'Canon'
        user.profile.address = '123 Bob Drive'
        user.profile.website = 'www.bob.com'
        user.profile.photography_type = 'portraits'
        PhotoFactory(title='Bobs Photo', user=user.profile)
        AlbumFactory(title='Bobs Album', user=user.profile)
        user.profile.save()

        user2 = UserFactory(username='usereve', email='eve@example.com')
        user2.set_password('secret')
        user2.save()

    def tearDown(self):
        User.objects.all().delete()

    def test_view_profile(self):
        c = Client()
        c.login(username='userbob', password='secret')
        response = c.get('/profile/')
        import pdb; pdb.set_trace()
        self.assertIn('Your camera is a Canon', response.content)
        self.assertIn('You have <strong>1</strong> albums', response.content)
        self.assertIn('You have a total of <strong>1</strong> photos',
                      response.content)
