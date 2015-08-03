from __future__ import unicode_literals
from django.views.generic.edit import FormView
from imager_profile.forms import UpdateProfileForm
from imager_profile.models import ImagerProfile


class UpdateProfileView(FormView):
    success_url = '/profile/'

    def get_form(self, form_class=UpdateProfileForm):
        try:
            profile = ImagerProfile.objects.get(user=self.request.user)
            return UpdateProfileForm(instance=profile,
                                     **self.get_form_kwargs())
        except ImagerProfile.DoesNotExist:
            return UpdateProfileForm(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super(UpdateProfileView, self).form_valid(form)
