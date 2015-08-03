from __future__ import unicode_literals
from django import forms
from imager_profile.models import ImagerProfile


class UpdateProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", max_length=30)
    last_name = forms.CharField(label="Last Name", max_length=30)
    email = forms.EmailField(label="Email Address")

    class Meta:
        model = ImagerProfile
        fields = ['address', 'website', 'camera', 'photography_type']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        except AttributeError:
            pass

    def save(self, *args, **kwargs):
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.save()
        return super(UpdateProfileForm, self).save(*args, **kwargs)
