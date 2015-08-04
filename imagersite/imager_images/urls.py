from django.conf.urls import url
from imager_images.views import (PhotoView, AlbumView, AlbumEditView,
                                 PhotoEditView, AlbumAddView, PhotoAddView)
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
    url(r'^album/add/$', login_required(AlbumAddView.as_view()),
        name='album_add'),
    url(r'^photos/add/$', login_required(PhotoAddView.as_view()),
        name='photo_add'),
    url(r'^album/edit/(?P<pk>\d+)/$', login_required(AlbumEditView.as_view()),
        {'success_url': 'album_detail'}, name='album_edit'),
    url(r'^photos/edit/(?P<pk>\d+)/$',
        login_required(PhotoEditView.as_view()),
        {'success_url': 'photo_detail'}, name='photo_edit'),
    url(r'^photos/(?P<pk>\d+)/detect$', PhotoView.as_view(detect=True),
        name='detect_faces')
]
