"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
<<<<<<< HEAD
from imagersite.views import IndexView, TemplateView
=======
from django.views.generic import TemplateView
from imagersite.views import IndexView
>>>>>>> 90526c8c17e7b49ceb2f40c48b2da6015e4b07b4
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'', include('registration.auth_urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
    url(r'^profile/', login_required(TemplateView.as_view(
                                     template_name='profile.html')),
        name='profile'),
    url(r'^images/library/', login_required(TemplateView.as_view(
                                            template_name='library.html')),
        name='library'),
=======
    url(r'^profile/',
        login_required(TemplateView.as_view(template_name='profile.html')),
        name='profile'),
    # url(r'^images/', include('imager_images.urls'))
>>>>>>> 90526c8c17e7b49ceb2f40c48b2da6015e4b07b4
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
