from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from django.db.models import Q

from imager_images.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
            model = Photo
            fields = (
                'title', 'description', 'date_uploaded', 'date_modified',
                'date_published', 'file'
            )


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        qs = super(PhotoViewSet, self).get_queryset()
        is_mine = Q(user=self.request.user)
        is_public = Q(published='Public')
        if self.request.user.is_anonymous():
            qs = qs.filter(is_public)
        else:
            qs = qs.filter(is_mine | is_public).distinct()
        return qs

router = routers.DefaultRouter()
router.register(r'photos', PhotoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))
]
