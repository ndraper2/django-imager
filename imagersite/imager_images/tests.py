from __future__ import unicode_literals
from django.test import TestCase
import factory
from django.contrib.auth.models import User
from faker import Faker as fake_factory
from models import Photo, Album
from imager_profile.models import ImagerProfile

fake = fake_factory()


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda x:
                                  '{0}@example.com'.format(x.first_name))
    username = factory.Sequence(lambda n: 'user{}'.format(n))


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo
    title = fake.sentences(nb=1)
    description = fake.text()
    file = fake.mime_type()


class AlbumFactory(factory.Factory):
    class Meta:
        model = Album
    title = fake.sentences(nb=1)
    description = fake.text()


class PhotoTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PhotoTestCase, cls).setUpClass()
        user = UserFactory.create()
        user.save()
        for i in range(100):
            _user = ImagerProfile.objects.get(user__username='user0')
            photo = PhotoFactory.create(user=_user)
            import pdb; pdb.set_trace()
            photo.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        super(PhotoTestCase, cls).tearDownClass()

    def test_photos_are_created(self):
        self.assertTrue(Photo.objects.count() == 100)

    def test_photos_belong_to_user(self):
        user = ImagerProfile.objects.get(user__username='user0')
        self.assertEqual(100, len(user.photos.all()))

    def test_photos_do_not_belong_to_other_user(self):
        new_user = UserFactory.create()
        new_user.save()
        with self.assertRaises(AttributeError):
            new_user.photos.all()


# class AlbumTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super(AlbumTestCase, cls).setUpClass()
#         _user = UserFactory.create()
#         _user.save()
#         _cover = PhotoFactory.create(user=_user.profile)
#         _cover.save()
#         import pdb; pdb.set_trace()
#         for i in range(5):
#             album = AlbumFactory.create(cover=_cover, user=_user.profile)
#             album.save()

#     @classmethod
#     def tearDownClass(cls):
#         Album.objects.all().delete()
#         super(AlbumTestCase, cls).tearDownClass()

#     def test_albums_are_created(self):
#         self.assertTrue(Album.objects.count() == 5)

    # def test_attributes_save(self):
    #     profile = ImagerProfile.objects.get(user__username='user0')
    #     profile.camera = 'Most amazing camera'
    #     profile.address = '123 amazing drive'
    #     profile.website = 'www.amazing.com'
    #     profile.photography_type = 'amazing'
    #     profile.save()
    #     self.assertTrue(ImagerProfile.objects.count() == 1000)
    #     self.assertEqual('Most amazing camera', profile.camera)
