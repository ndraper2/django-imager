from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from imager_profile.models import ImagerProfile


@python_2_unicode_compatible
class Photo(models.Model):
    file = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    title = models.CharField(max_length=128,
                             help_text="What is your photo's title?")
    description = models.TextField(help_text="Describe your photo.")
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now=True)

    CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private'),
        ('Shared', 'Shared'),
    )
    published = models.CharField(max_length=8, choices=CHOICES,
                                 default='Private')

    user = models.ForeignKey(ImagerProfile, related_name='photos', null=False)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Album(models.Model):
    user = models.ForeignKey(ImagerProfile, related_name='albums', null=False)
    photos = models.ManyToManyField(Photo, related_name='albums',)
    title = models.CharField(max_length=128,
                             help_text="What is your album's title?")
    description = models.TextField(help_text="Describe your album.")
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now=True)

    CHOICES = (
        ('Public', 'Public'),
        ('Private', 'Private'),
        ('Shared', 'Shared'),
    )
    published = models.CharField(max_length=8, choices=CHOICES,
                                 default='Private')

    cover = models.ForeignKey(Photo, related_name='cover_for')

    def __str__(self):
        return self.title
