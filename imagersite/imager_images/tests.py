from __future__ import unicode_literals
from django.test import TestCase
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from faker import Faker as fake_factory
from models import Photo, Album
from imager_profile.models import ImagerProfile

fake = fake_factory()


class UserFactory(DjangoModelFactory):
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


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album
    title = fake.sentences(nb=1)[0]
    description = fake.text()


class PhotoTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='user1')
        user.save()
        for i in range(100):
            photo = PhotoFactory.create(user=user.profile)
            photo.save()

    def tearDown(self):
        User.objects.all().delete()
        Photo.objects.all().delete()

    def test_photos_are_created(self):
        self.assertTrue(Photo.objects.count() == 100)

    def test_photos_belong_to_user(self):
        user = ImagerProfile.objects.get(user__username='user1')
        self.assertEqual(100, len(user.photos.all()))

    def test_photos_do_not_belong_to_other_user(self):
        new_user = UserFactory.create(username='user2')
        new_user.save()
        self.assertEqual(len(new_user.profile.photos.all()), 0)


class AlbumTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create()
        user.save()
        cover = PhotoFactory.create(user=user.profile)
        cover.save()
        for i in range(5):
            album = AlbumFactory.create(cover=cover, user=user.profile)
            album.save()

    @classmethod
    def tearDown(self):
        Album.objects.all().delete()
        User.objects.all().delete()

    def test_albums_are_created(self):
        self.assertTrue(Album.objects.count() == 5)

    def test_add_photos_to_albums(self):
        album = Album.objects.all()[0]
        user = ImagerProfile.objects.all()[0]
        for i in range(5):
            photo = PhotoFactory.create(user=user)
            photo.save()
        photos = list(Photo.objects.all())
        album.photos.add(*photos)
        self.assertTrue(len(album.photos.all()) == 6)
        self.assertTrue(album.user == user)
