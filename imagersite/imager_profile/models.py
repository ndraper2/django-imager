from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


class ActiveProfileManager(models.Manager):
    def get_query_set(self):
        return super(ActiveProfileManager, self).get_query_set().filter(
            user__is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=False)
    camera = models.CharField(
        max_length=128,
        help_text='What is the make and model of your camera?',
        blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    photography_type = models.TextField(
        help_text='What is your favorite type of photography?',
        blank=True)

    objects = models.Manager()
    active = ActiveProfileManager()

    @property
    def is_active(self):
        return self.user.is_active

    def __str__(self):
        return self.user.username
