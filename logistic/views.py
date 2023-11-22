from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common_archive.models import ArchiveBox
from logistic.serializers import ABPlacementSerializer, ABCompletionSerializer


@extend_schema_view(partial_update=extend_schema(summary='Place archive boxes on storage', tags=['Logistic']), )
class ABPlacementView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('storage_address').select_related('current_sector')
    serializer_class = ABPlacementSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('patch',)


@extend_schema_view(create=extend_schema(summary='Complete archive box with dossiers', tags=['Logistic']), )
class ABCompletionView(ModelViewSet):
    queryset = ArchiveBox.objects.all()
    serializer_class = ABCompletionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('post',)
