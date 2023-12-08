from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from archive.models import ArchiveBox
from logistics.permissions import IsInLogisticsGroup
from logistics.serializers.archive_box import ABCompletionSerializer, ABPlacementSerializer, ABCheckSerializer


@extend_schema_view(partial_update=extend_schema(summary='Box checking', tags=['Logistics']), )
class ABCheckView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCheckSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)


@extend_schema_view(partial_update=extend_schema(summary='Place archive boxes on storage', tags=['Logistics']), )
class ABPlacementView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('storage_address').select_related('current_sector')
    serializer_class = ABPlacementSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)


@extend_schema_view(
    create=extend_schema(summary='Open/create archive box to complete', tags=['Logistics']),
    destroy=extend_schema(summary='Delete empty archive box', tags=['Logistics']),
                    )
class ABCompletionView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCompletionSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('post', 'delete')


