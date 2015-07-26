from django.apps import AppConfig


class ImagerProfileAppConfig(AppConfig):

    name = 'imager_profile'
    verbose_name = 'Imager Profile'

    def ready(self):
        import imager_profile.signals.handlers
