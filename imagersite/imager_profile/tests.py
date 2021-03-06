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
        self.assertEqual(str(profile),
                         user.get_full_name() or profile.user.username)

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
        PhotoFactory(title='Bobs Photo', user=user)
        AlbumFactory(title='Bobs Album', user=user)
        user.profile.save()

        user2 = UserFactory(username='usereve', email='eve@example.com')
        user2.set_password('secret')
        user2.save()

    def test_view_profile(self):
        c = Client()
        c.login(username='userbob', password='secret')
        response = c.get('/profile/')
        self.assertIn('Your camera is a Canon', response.content)
        self.assertIn('You have <strong>1</strong> albums', response.content)
        self.assertIn('You have a total of <strong>1</strong> photos',
                      response.content)

    def test_eve_doesnt_see_bob(self):
        c = Client()
        c.login(username='usereve', password='secret')
        response = c.get('/profile/')
        self.assertIn('You have <strong>0</strong> albums', response.content)

    def test_unauthenticated_redirect(self):
        c = Client()
        response = c.get('/profile/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIn('form method="post" action="/login/"',
                      response.content)


def ProfileEditTestCase(TestCase):
    def setUp(self):
        user = UserFactory(username='userbob', email='bob@example.com')
        user.set_password('secret')
        user.save()
        user.profile.camera = 'Canon'
        user.profile.address = '123 Bob Drive'
        user.profile.website = 'www.bob.com'
        user.profile.photography_type = 'portraits'
        user.profile.save()

    def test_profile_edit_view(self):
        c = Client()
        c.login(username='userbob', password='secret')
        user = User.objects.all()[0]
        response = c.get('/profile/edit/')
        self.assertIn(user.camera, response.content)
        response = c.post(
            '/profile/edit/',
            {
                'camera': 'new camera',
                'first_name': 'bob',
                'last_name': 'wehadababyitsaboy',
                'email': 'bob@example.com',
            },
            follow=True
        )
        self.assertIn('new camera', response.content)
        self.assertIn('wehadababyitsaboy', response.content)

    def test_unauthenticated_redirect(self):
        c = Client()
        response = c.get('/profile/edit/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIn('form method="post" action="/login/"',
                      response.content)
