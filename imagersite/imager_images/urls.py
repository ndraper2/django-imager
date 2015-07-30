from django.conf.urls import url
from imager_images.views import PhotoView, AlbumView, AlbumAdd, PhotoAdd
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^photos/(?P<pk>\d+)/$',
        login_required(PhotoView.as_view()),
        name='photo_detail'),
    url(r'^library/', login_required(TemplateView.as_view(
                                     template_name='library.html')),
        name='library'),
    url(r'^album/(?P<pk>\d+)/$',
        login_required(AlbumView.as_view()),
        name='album_detail'),
    url(r'^album/add', login_required(AlbumAdd.as_view()),
        name='album_add'),
    url(r'^photos/add', login_required(PhotoAdd.as_view()),
        name='photo_add')
]
