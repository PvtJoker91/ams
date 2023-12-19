from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier
from archive.serializers.search import DossierSearchSerializer


@extend_schema_view(
    list=extend_schema(summary='Dossiers list', tags=['Units']),
    retrieve=extend_schema(summary='Dossier detail', tags=['Units']),
)
class DossierView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = Dossier.objects.all().select_related('contract')
    serializer_class = DossierSearchSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get',)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__last_name',
        'contract__client__name',
        'contract__client__middle_name',
        'contract__client__passport',
        'contract__client__birthday',
        'contract__product__name',

    ]
    search_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__passport',
    ]
    ordering = ('contract__client__last_name', 'contract__product__name',)
