from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied
from imager_images.models import Photo, Album
from .forms import AlbumForm, PhotoForm


class PhotoView(DetailView):
    model = Photo
    template_name = 'photo.html'

    def get_object(self, *args, **kwargs):
        obj = super(PhotoView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj


class AlbumView(DetailView):
    model = Album
    template_name = 'album.html'

    def get_object(self, *args, **kwargs):
        obj = super(AlbumView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj


class AlbumFormView(FormView):
    template_name = 'album_add.html'
    form_class = AlbumForm
    success_url = '/images/library/'

    def get_form(self, form_class=PhotoForm):
        try:
            album = Album.objects.get(user=self.request.user,
                                      pk=self.kwargs['pk'])
            return AlbumForm(instance=album, **self.get_form_kwargs())
        except (KeyError, Album.DoesNotExist):
            return AlbumForm(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(AlbumFormView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(AlbumFormView, self).form_valid(form)


class PhotoFormView(FormView):
    template_name = 'photo_add.html'
    form_class = PhotoForm
    success_url = '/images/library/'

    def get_form(self, form_class=PhotoForm):
        try:
            photo = Photo.objects.get(user=self.request.user,
                                      pk=self.kwargs['pk'])
            return PhotoForm(instance=photo, **self.get_form_kwargs())
        except (KeyError, Photo.DoesNotExist):
            return PhotoForm(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PhotoFormView, self).form_valid(form)
