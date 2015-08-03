from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from imager_profile.views import UpdateProfileView

urlpatterns = [
    url(r'^$',
        login_required(TemplateView.as_view(template_name='profile.html')),
        name='profile'),
    url(r'^edit/$',
        login_required(UpdateProfileView.as_view(
            template_name='profile_update.html')),
        name='profile_update')
]