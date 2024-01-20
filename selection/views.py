from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier
from common.pagination import CustomPagination
from common.services.validators import validate_dossier_barcode
from dossier_requests.models import DossierTask
from logistics.permissions import IsInLogisticsGroup
from selection.models import SelectionOrder
from selection.serializers.dossiers import DossierSelectingSerializer
from selection.serializers.orders import SelectionOrderCreateSerializer, SelectionOrderSerializer
from selection.serializers.tasks import TaskSelectingSerializer


@extend_schema_view(
    list=extend_schema(summary='Task list to select', tags=['Selection']),
)
class TaskSelectingView(mixins.ListModelMixin,
                        GenericViewSet):
    queryset = DossierTask.objects.all()
    serializer_class = TaskSelectingSerializer
    permission_classes = [IsInLogisticsGroup]

    def get_queryset(self):
        return DossierTask.objects.filter(task_status='accepted').annotate(
            location=F('dossier__archive_box__storage_address__shelf_code'))


@extend_schema_view(
    partial_update=extend_schema(summary='Select dossier', tags=['Selection']),
)
class DossierSelectingView(mixins.UpdateModelMixin,
                           GenericViewSet):
    queryset = Dossier.objects.all().select_related('current_sector')
    serializer_class = DossierSelectingSerializer
    permission_classes = [IsInLogisticsGroup]
    lookup_field = 'barcode'
    http_method_names = ('patch',)

    def update(self, request, *args, **kwargs):
        barcode = kwargs.get('barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError({'validation_error': 'Wrong barcode format'})
        return super().update(request, *args, **kwargs)


@extend_schema_view(
    create=extend_schema(summary='Create selection order', tags=['Selection']),
    list=extend_schema(summary='Selection orders list', tags=['Selection']),
    retrieve=extend_schema(summary='Get selection order', tags=['Selection']),
)
class SelectionOrderView(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         GenericViewSet):
    queryset = SelectionOrder.objects.all()
    serializer_class = SelectionOrderSerializer
    permission_classes = [IsInLogisticsGroup]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'executor',
        'creator',
    ]
    ordering_fields = [
        'time_create',
        'selected'
    ]
    ordering = ['-time_create', '-selected']

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SelectionOrderCreateSerializer
        return SelectionOrderSerializer
