from django.views.generic import DetailView
from django.http import HttpResponseForbidden
from imager_images.models import Photo, Album


class PhotoView(DetailView):
    model = Photo
    template_name = 'photo.html'

    def get_object(self, *args, **kwargs):
        obj = super(PhotoView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            return HttpResponseForbidden()
        return obj


class AlbumView(DetailView):
    model = Album
    template_name = 'album.html'

    def get_object(self, *args, **kwargs):
        obj = super(AlbumView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            return HttpResponseForbidden()
        return obj
