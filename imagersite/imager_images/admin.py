from django.contrib import admin
from imager_images.models import Photo
from imager_images.models import Album, Face

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Face)
