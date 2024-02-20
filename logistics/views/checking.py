from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, ArchiveBox
from common.validators import validate_dossier_barcode
from logistics.permissions import IsInLogisticsGroup
from logistics.serializers.checking import DossierCheckSerializer, ABCheckSerializer


@extend_schema_view(
    partial_update=extend_schema(summary='Checking // Update dossier box, status, current_sector', tags=['Logistics'])
)
class DossierCheckView(mixins.UpdateModelMixin,
                       GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    serializer_class = DossierCheckSerializer
    permission_classes = [IsInLogisticsGroup]
    http_method_names = ('patch',)

    def update(self, request, *args, **kwargs):
        barcode = kwargs.get('pk', None)
        if barcode:
            validate_dossier_barcode(barcode)
        return super().update(request, *args, **kwargs)



@extend_schema_view(partial_update=extend_schema(summary='Box checking', tags=['Logistics']), )
class ABCheckView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCheckSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)
