from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
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


class AlbumAdd(CreateView):
    template_name = 'album_add.html'
    form_class = AlbumForm
    success_url = '/images/library/'

    def get_form_kwargs(self):
        kwargs = super(AlbumAdd, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AlbumAdd, self).form_valid(form)


class PhotoAdd(CreateView):
    template_name = 'photo_add.html'
    form_class = PhotoForm
    success_url = '/images/library/'

    # def form_view(request, ob_id):
    #     obj = Album.objects.get(pk=ob_id)
    #     if request.method == 'POST':
    #         data = request.POST
    #         form = AlbumForm(data, request.Files, instance=obj)
    #         if form.is_valid():
    #             form.save()
    #     else:
    #         form = AlbumForm(instance=obj)

    #     return

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PhotoAdd, self).form_valid(form)
