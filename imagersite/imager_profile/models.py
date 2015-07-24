from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


class ActiveProfileManager(models.Manager):
    def get_query_set(self):
        return super(ActiveProfileManager, self).get_query_set().filter(
            user__is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=False)
    camera = models.CharField(max_length=128,
        help_text='What is the make and model of your camera?')
    address = models.TextField()
    website = models.URLField()
    photography_type = models.TextField(help_text='What is your favorite type of photography?')

    objects = models.Manager()
    active = ActiveProfileManager()

    # @property
    # def is_active(self):
    #     return self.user.is_active

    def __str__(self):
        return self.user.get_full_name() or self.user.username


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, **kwargs):
    try:
        instance.profile
    except ImagerProfile.DoesNotExist:
        instance.profile = ImagerProfile()
        instance.profile.save()


@receiver(post_delete, sender=User)
def delete_profile_for_user(sender, instance, **kwargs):
    try:
        instance.profile.delete()
    except ImagerProfile.DoesNotExist:
        pass
