from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, ArchiveBox
from common.services.statuses import DOSSIER_CHECKING_AVAILABLE_STATUSES
from common.services.validators import validate_dossier_barcode
from logistics.permissions import IsInLogisticsGroup
from logistics.serializers.checking import DossierCheckSerializer, ABCheckSerializer


@extend_schema_view(
    partial_update=extend_schema(summary='Checking // Update dossier box, status, current_sector', tags=['Logistics']),
    retrieve=extend_schema(summary='Get dossier', tags=['Logistics']), )
class DossierCheckView(mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    serializer_class = DossierCheckSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('get', 'patch',)

    def retrieve(self, request, *args, **kwargs):
        barcode = kwargs.get('barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError({'validation_error': 'Wrong barcode format'})
        instance = self.get_object()
        if instance.status not in DOSSIER_CHECKING_AVAILABLE_STATUSES:
            raise ParseError(f"Dossier should not be on this operation. Dossier current status is {instance.status}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        barcode = kwargs.get('barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError({'validation_error': 'Wrong barcode format'})
        return super().update(request, *args, **kwargs)


@extend_schema_view(partial_update=extend_schema(summary='Box checking', tags=['Logistics']), )
class ABCheckView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCheckSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)
