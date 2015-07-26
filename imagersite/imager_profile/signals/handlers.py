from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from imager_profile.models import ImagerProfile


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, **kwargs):
    try:
        instance.profile
    except ImagerProfile.DoesNotExist:
        instance.profile = ImagerProfile()
        instance.profile.save()


@receiver(post_delete, sender=ImagerProfile)
def delete_profiles_user(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except ImagerProfile.DoesNotExist:
        pass
