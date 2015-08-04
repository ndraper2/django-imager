from __future__ import unicode_literals
from django.test import TestCase
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from faker import Faker as fake_factory
from models import Photo, Album
from django.test import Client

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
            photo = PhotoFactory.create(user=user)
            photo.save()

    def test_photos_are_created(self):
        self.assertTrue(Photo.objects.count() == 100)

    def test_photos_belong_to_user(self):
        user = User.objects.get(username='user1')
        self.assertEqual(100, len(user.photos.all()))

    def test_photos_do_not_belong_to_other_user(self):
        new_user = UserFactory.create(username='user2')
        new_user.save()
        self.assertEqual(len(new_user.photos.all()), 0)


class AlbumTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create()
        user.save()
        cover = PhotoFactory.create(user=user)
        cover.save()
        for i in range(5):
            album = AlbumFactory.create(cover=cover, user=user)
            album.save()

    def test_albums_are_created(self):
        self.assertTrue(Album.objects.count() == 5)

    def test_add_photos_to_albums(self):
        album = Album.objects.all()[0]
        user = User.objects.all()[0]
        for i in range(5):
            photo = PhotoFactory.create(user=user)
            photo.save()
        photos = list(Photo.objects.all())
        album.photos.add(*photos)
        self.assertTrue(len(album.photos.all()) == 6)
        self.assertTrue(album.user == user)


class AlbumViewTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='userbob')
        user.set_password('secret')
        user.save()
        cover = PhotoFactory.create(user=user)
        cover.save()
        album = AlbumFactory.create(cover=cover, user=user)
        album.save()
        album.photos.add(cover)

    def test_album_detail_view(self):
        album = Album.objects.all()[0]
        photo = Photo.objects.all()[0]
        c = Client()
        c.login(username='userbob', password='secret')
        response = c.get('/images/album/{}/'.format(album.id))
        self.assertIn(album.title, response.content)
        self.assertIn(album.description, response.content)
        self.assertIn(photo.title, response.content)

    def test_album_not_owner(self):
        user = UserFactory.create(username='usereve')
        user.set_password('secret')
        user.save()
        album = Album.objects.all()[0]
        c = Client()
        c.login(username='usereve', password='secret')
        response = c.get('/images/album/{}/'.format(album.id))
        assert response.status_code == 404

    def test_album_unauthenticated(self):
        album = Album.objects.all()[0]
        c = Client()
        response = c.get('/images/album/{}/'.format(album.id), follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIn('form method="post" action="/login/"',
                      response.content)


class PhotoViewTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='userbob')
        user.set_password('secret')
        user.save()
        photo = PhotoFactory.create(user=user)
        photo.save()

    def test_photo_detail_view(self):
        photo = Photo.objects.all()[0]
        c = Client()
        c.login(username='userbob', password='secret')
        response = c.get('/images/photos/{}/'.format(photo.id))
        self.assertIn(photo.title, response.content)
        self.assertIn(photo.description, response.content)

    def test_photo_not_owner(self):
        user = UserFactory.create(username='usereve')
        user.set_password('secret')
        user.save()
        photo = Photo.objects.all()[0]
        c = Client()
        c.login(username='usereve', password='secret')
        response = c.get('/images/photos/{}/'.format(photo.id))
        assert response.status_code == 404

    def test_photo_unauthenticated(self):
        photo = Photo.objects.all()[0]
        c = Client()
        response = c.get('/images/photos/{}/'.format(photo.id), follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIn('form method="post" action="/login/"',
                      response.content)


class LibraryViewTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='userbob')
        user.set_password('secret')
        user.save()
        cover = PhotoFactory.create(user=user)
        cover.save()
        album = AlbumFactory.create(cover=cover, user=user)
        album.save()
        album.photos.add(cover)

    def test_library_view(self):
        photo = Photo.objects.all()[0]
        album = Album.objects.all()[0]
        c = Client()
        c.login(username='userbob', password='secret')
        response = c.get('/images/library/')
        self.assertIn(photo.title, response.content)
        self.assertIn(album.title, response.content)

    def test_library_view_different_user(self):
        photo = Photo.objects.all()[0]
        album = Album.objects.all()[0]
        c = Client()
        c.login(username='usereve', password='secret')
        response = c.get('/images/library/')
        self.assertNotIn(photo.title, response.content)
        self.assertNotIn(album.title, response.content)

    def test_library_unauthenticated(self):
        c = Client()
        response = c.get('/images/library/', follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIn('form method="post" action="/login/"',
                      response.content)


class PhotoFormTestCase(TestCase):
    def setUp(self):
        user = UserFactory.create(username='userbob')
        user.set_password('secret')
        user.save()
        user2 = UserFactory.create(username='usereve')
        user2.set_password('secret')
        user2.save()
        cover = PhotoFactory.create(user=user)
        cover.save()
        album = AlbumFactory.create(cover=cover, user=user)
        album.save()
        album.photos.add(cover)

    def test_add_photo(self):
        c = Client()
        c.login(username='userbob', password='secret')
        with open('imager_images/thumbnail.jpg', 'rb') as fh:
            response = c.post(
                '/images/photos/add/',
                {'file': fh, 'title': 'test title', 'published': 'Private'},
                follow=True
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn('<img src=\'/media/cache/', response.content)
        self.assertIn('test title', response.content)

    def test_edit_photo(self):
        c = Client()
        c.login(username='userbob', password='secret')
        photo = Photo.objects.all()[0]
        response = c.get('/images/photos/edit/{}/'.format(photo.id))
        self.assertIn(photo.title, response.content)
        with open('imager_images/thumbnail.jpg', 'rb') as fh:
            response = c.post(
                '/images/photos/edit/{}/'.format(photo.id),
                {
                    'file': fh,
                    'title': 'new test title',
                    'published': 'Private'
                },
                follow=True
            )
        self.assertIn('new test title', response.content)
        response = c.get('/images/photos/{}/'.format(photo.id))
        # make sure we have the same photo id
        self.assertIn('new test title', response.content)

    def test_edit_other_user(self):
        # what you end up with is a create form for yourself.
        c = Client()
        c.login(username='usereve', password='secret')
        photo = Photo.objects.all()[0]
        with open('imager_images/thumbnail.jpg', 'rb') as fh:
            response = c.post(
                '/images/photos/edit/{}/'.format(photo.id),
                {
                    'file': fh,
                    'title': 'other user',
                    'published': 'Private'
                },
                follow=True
            )
        # self.assertEqual(2, len(Photo.objects.all()))
        userbob = User.objects.get(username='userbob')
        usereve = User.objects.get(username='usereve')
        import pdb; pdb.set_trace()
        self.assertEqual(photo.user, userbob)
