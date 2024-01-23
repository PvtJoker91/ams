from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, DossierScan
from archive.serializers.dossiers import DossierDetailSerializer, DossierScanSerializer, DossierListSerializer
from common.filters import CustomFilter
from common.views.mixins import ExtendedGenericViewSet


@extend_schema_view(
    list=extend_schema(summary='Dossiers list', tags=['Units']),
    retrieve=extend_schema(summary='Dossier detail', tags=['Units']),
)
class DossierView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  ExtendedGenericViewSet):
    queryset = Dossier.objects.all()
    serializer_class = DossierDetailSerializer
    multi_serializer_class = {
        'list': DossierListSerializer,
        'retrieve': DossierDetailSerializer,
    }
    permission_classes = [IsAuthenticated]
    http_method_names = ('get',)
    filter_backends = (CustomFilter, filters.OrderingFilter)
    filterset_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__last_name',
        'contract__client__first_name',
        'contract__client__middle_name',
        'contract__client__passport',
        'contract__client__birthday',
        'contract__product__name',
    ]

    ordering = ('contract__client__last_name', 'contract__product__name',)

    def get_queryset(self):
        return Dossier.objects.all().select_related('contract').annotate(
            location=F('archive_box__storage_address__shelf_code'))



@extend_schema_view(
    create=extend_schema(summary='Add scan to dossier', tags=['Units']),
    list=extend_schema(summary='Dossier scan list', tags=['Units']),
    destroy=extend_schema(summary='Delete scan', tags=['Units']),
)
class DossierScanView(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    serializer_class = DossierScanSerializer
    queryset = DossierScan.objects.all()

    def get_queryset(self):
        dossier = self.request.query_params.get('dossier')
        if dossier:
            return DossierScan.objects.filter(dossier=dossier)
        return DossierScan.objects.all()
