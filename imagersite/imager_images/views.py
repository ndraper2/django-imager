from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from imager_images.models import Photo
from django.http import HttpResponseForbidden


class PhotoView(DetailView):
    template_name = 'photo_detail.html'

    def get_object(self, *args, **kwargs):
        obj = super(PhotoView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            return HttpResponseForbidden()
        return obj


class AlbumView(DetailView):
    template_name = 'album_detail.html'

    def get_object(self, *args, **kwargs):
        obj = super(AlbumView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            return HttpResponseForbidden()
        return obj
