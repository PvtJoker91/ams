from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from archive.models import ArchiveBox
from logistics.permissions import IsInLogisticsGroup
from logistics.serializers.placement import ABPlacementSerializer


@extend_schema_view(partial_update=extend_schema(summary='Place archive boxes on storage', tags=['Logistics']), )
class ABPlacementView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('storage_address').select_related('current_sector')
    serializer_class = ABPlacementSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)
