from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, ArchiveBox
from common.validators import validate_dossier_barcode
from logistics.permissions import IsInLogisticsGroup
from logistics.serializers.completion import DossierCompletionSerializer, ABCompletionSerializer


@extend_schema_view(
    partial_update=extend_schema(summary='Completion // Update dossier box, status, current_sector', tags=['Logistics']),
)
class DossierCompletionView(mixins.UpdateModelMixin,
                            GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    serializer_class = DossierCompletionSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)

    def update(self, request, *args, **kwargs):
        barcode = kwargs.get('barcode', None)
        if barcode:
            validate_dossier_barcode(barcode)
        return super().update(request, *args, **kwargs)


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
