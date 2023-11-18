from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import  GenericViewSet

from common_archive.models import ArchiveBox
from logistic.serializers import ABPlacementSerializer


# Create your views here.
class ABPlacementView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all()
    serializer_class = ABPlacementSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('patch',)
