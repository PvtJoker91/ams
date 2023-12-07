from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

import archive.serializers
from archive.models import Dossier


@extend_schema_view(
    list=extend_schema(summary='Dossiers list', tags=['Units']),
    retrieve=extend_schema(summary='Dossier detail', tags=['Units']),
)
class DossierSearchView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Dossier.objects.all().select_related('contract')
    serializer_class = archive.serializers.DossierSearchSerializer
    permission_classes = [AllowAny]
    http_method_names = ('get',)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__last_name',
        'contract__client__name',
        'contract__client__middle_name',
        'contract__client__passport',
        'contract__client__birthday',
        'contract__product__id',

    ]
    search_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__passport',
    ]
