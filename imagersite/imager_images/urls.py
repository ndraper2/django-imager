from django.conf.urls import url
from imager_images.views import PhotoView, AlbumView
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
        name='album_detail')
]
