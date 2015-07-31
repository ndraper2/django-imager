from django.views.generic import DetailView, FormView
from django.http import HttpResponseForbidden
from imager_images.models import Photo, Album
from .forms import AlbumForm, PhotoForm


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


class AlbumAdd(FormView):
    template_name = 'album_add.html'
    form_class = AlbumForm
    success_url = '/profile/'

    def get_form_kwargs(self):
        kwargs = super(AlbumAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class PhotoAdd(FormView):
    template_name = 'photo_add.html'
    form_class = PhotoForm
    success_url = 'images/photos/add/'

    def form_valid(self, form):
        pass
