from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from common_archive.models import ArchiveBox
from logistic.serializers.archive_box import ABCompletionSerializer, ABPlacementSerializer, ABCheckSerializer


@extend_schema_view(partial_update=extend_schema(summary='Box checking', tags=['Logistic']), )
class ABCheckView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCheckSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('patch',)


@extend_schema_view(partial_update=extend_schema(summary='Place archive boxes on storage', tags=['Logistic']), )
class ABPlacementView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('storage_address').select_related('current_sector')
    serializer_class = ABPlacementSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('patch',)


@extend_schema_view(
    create=extend_schema(summary='Open/create archive box to complete', tags=['Logistic']),
    destroy=extend_schema(summary='Delete empty archive box', tags=['Logistic']),
                    )
class ABCompletionView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCompletionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('post', 'delete')


