from django.db.models import F
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, DossierScan
from archive.serializers import dossiers
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
    serializer_class = dossiers.DossierDetailSerializer
    multi_serializer_class = {
        'list': dossiers.DossierListSerializer,
        'retrieve': dossiers.DossierDetailSerializer,
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
        return Dossier.objects.select_related('contract__client', 'contract__product').annotate(
            location=F('archive_box__storage_address__shelf_code')).all()


@extend_schema_view(
    retrieve=extend_schema(summary='Dossier with scans', tags=['Units']),
)
class DossierScansView(mixins.RetrieveModelMixin,
                       GenericViewSet):
    queryset = Dossier.objects.all()
    serializer_class = dossiers.DossierScansSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Dossier.objects.select_related('contract__client', 'contract__product').all()


@extend_schema_view(
    create=extend_schema(summary='Add scan to dossier', tags=['Units']),
    list=extend_schema(summary='Scan list', tags=['Units']),
    destroy=extend_schema(summary='Delete scan', tags=['Units']),
)
class ScanView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):
    serializer_class = dossiers.ScanSerializer
    queryset = DossierScan.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dossier = self.request.query_params.get('dossier')
        if dossier:
            return DossierScan.objects.filter(dossier=dossier).select_related('dossier__contract', 'uploader')
        return DossierScan.objects.select_related('dossier__contract', 'uploader').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return dossiers.ScanCreateSerializer
        return dossiers.ScanSerializer
