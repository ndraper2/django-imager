from django import forms
from .models import Photo, Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'published', 'photos', 'cover']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['photos'].queryset = Photo.objects.filter(
            user=self.request.user)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file', 'title', 'description', 'published']
