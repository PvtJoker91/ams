from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common_archive.models import ArchiveBox, Dossier
from logistic.serializers import ABPlacementSerializer, ABCompletionSerializer, DossierCompletionSerializer
from services.validators import validate_dossier_barcode


@extend_schema_view(partial_update=extend_schema(summary='Place archive boxes on storage', tags=['Logistic']), )
class ABPlacementView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = ArchiveBox.objects.all().select_related('storage_address').select_related('current_sector')
    serializer_class = ABPlacementSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('patch',)


@extend_schema_view(
    create=extend_schema(summary='Open/create archive box to complete', tags=['Logistic']),
    partial_update=extend_schema(summary='Close archive box', tags=['Logistic']),
                    )
class ABCompletionView(ModelViewSet):
    queryset = ArchiveBox.objects.all().select_related('current_sector')
    serializer_class = ABCompletionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('post', 'patch')


@extend_schema_view(
    partial_update=extend_schema(summary='Update dossier box, status, current_sector', tags=['Logistic']),
                    )
class DossierCompletionView(mixins.UpdateModelMixin,
                            GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    serializer_class = DossierCompletionSerializer
    permission_classes = [AllowAny]
    lookup_field = 'barcode'
    http_method_names = ('patch',)

    def update(self, request, *args, **kwargs):
        barcode = kwargs.get('barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError({'validation_error': 'Wrong barcode format'})
        return super().update(request, *args, **kwargs)

