from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from imager_images.models import Photo


class PhotoView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        photo = get_object_or_404(Photo, pk=kwargs['pk'])
        context['photo'] = photo
        return context
