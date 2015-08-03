from django import forms
from .models import Photo, Album
from django.shortcuts import render


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'published', 'photos', 'cover']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['photos'].queryset = Photo.objects.filter(
            user=self.request.user)
        self.fields['cover'].queryset = self.instance.photos

    # def form_view(request, ob_id):
    #     obj = Album.objects.get(pk=ob_id)
    #     if request.method == 'POST':
    #         data = request.POST
    #         form = AlbumForm(data, request.Files, instance=obj)
    #         if form.is_valid():
    #             form.save()
    #     else:
    #         form = AlbumForm(instance=obj)

    #     return render('album_.html', context={'form': form})


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file', 'title', 'description', 'published']
