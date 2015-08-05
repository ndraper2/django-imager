from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

PUBLIC = 'Public'
SHARED = 'Shared'
PRIVATE = 'Private'

CHOICES = (
    (PUBLIC, 'Public'),
    (SHARED, 'Shared'),
    (PRIVATE, 'Private'),
)


@python_2_unicode_compatible
class Photo(models.Model):
    file = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    title = models.CharField(max_length=128,
                             help_text="What is your photo's title?")
    description = models.TextField(help_text="Describe your photo.",
                                   blank=True)
    date_uploaded = models.DateField(auto_now_add=True,)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(max_length=8, choices=CHOICES,
                                 default=PRIVATE)

    user = models.ForeignKey(User, related_name='photos', null=False)
    location = models.PointField(null=True, blank=True)
    objects = models.GeoManager()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Album(models.Model):
    user = models.ForeignKey(User, related_name='albums', null=False)
    photos = models.ManyToManyField(Photo,
                                    related_name='albums',
                                    blank=True)
    title = models.CharField(max_length=128,
                             help_text="What is your album's title?")
    description = models.TextField(help_text="Describe your album.",
                                   blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(max_length=8, choices=CHOICES,
                                 default=PRIVATE)

    cover = models.ForeignKey(Photo, related_name='cover_for', blank=True,
                              null=True)

    objects = models.GeoManager()

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Face(models.Model):
    photo = models.ForeignKey(Photo,
                              related_name='faces',
                              null=False,
                              )
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self):
        return 'Face: ' + self.photo.title + ' : ' + self.name
