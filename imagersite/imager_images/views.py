from __future__ import unicode_literals
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied
from imager_images.models import Photo, Album, Face
from .forms import AlbumForm, PhotoForm
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_faces(photo):
    import Algorithmia
    import base64
    Algorithmia.apiKey = "Simple simritlrldm5w9OsZJ/L9QMifSG1"
    file_path = 'media/' + str(photo.file)
    file_path = os.path.join(BASE_DIR, file_path)

    with open(file_path, 'rb') as img:
        b64 = base64.b64encode(img.read())

    result = Algorithmia.algo("/ANaimi/FaceDetection").pipe(b64)

    faces = []
    for rect in result:
        face = Face()
        face.photo = photo
        face.name = '?'
        face.x = rect['x']
        face.y = rect['y']
        face.width = rect['width']
        face.height = rect['height']
        face.save()
        faces.append(face)

    return faces


class PhotoView(DetailView):
    model = Photo
    template_name = 'photo.html'
    detect = False

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.detect and len(self.object.faces.all()) == 0:
            get_faces(self.object)

        context['faces'] = self.object.faces.all()
        return context


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

    def get_form(self, form_class=AlbumForm):
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
