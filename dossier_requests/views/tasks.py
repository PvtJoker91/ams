from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, Sector
from common.pagination import CustomPagination
from common.services.registries import registry_accepting
from common.statuses import DOSSIER_REQUEST_EXECUTION_AVAILABLE_STATUSES
from common.validators import validate_dossier_barcode, validate_dossier_status
from common.views.mixins import ExtendedGenericViewSet
from dossier_requests.models import DossierTask
from dossier_requests.permissions import IsInRequestsGroup
from dossier_requests.serializers import tasks


@extend_schema_view(
    list=extend_schema(summary='Tasks list', tags=['Tasks']),
    create=extend_schema(summary='Create multiple tasks', tags=['Tasks']),
    partial_update=extend_schema(summary='Update task', tags=['Tasks']),
    retrieve=extend_schema(summary='Task detail', tags=['Tasks']),
)
class TaskView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               ExtendedGenericViewSet):
    queryset = DossierTask.objects.all()
    serializer_class = tasks.TaskListSerializer
    multi_serializer_class = {
        'list': tasks.TaskListSerializer,
        'retrieve': tasks.TaskRetrieveSerializer,
        'create': tasks.TaskCreateSerializer,
        'partial_update': tasks.TaskUpdateSerializer,
    }
    pagination_class = CustomPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsInRequestsGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    ordering_fields = [
        'task_status',
        'request__service',
    ]
    ordering = ['-task_status', 'request__urgency', ]

    def create(self, request, *args, **kwargs):
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response


@extend_schema_view(
    list=extend_schema(summary='Tasks list to execute', tags=['Tasks']),
)
class TaskExecuteView(mixins.ListModelMixin,
                      GenericViewSet):
    queryset = DossierTask.objects.all()
    serializer_class = tasks.TaskListSerializer
    http_method_names = ('get',)
    permission_classes = [IsInRequestsGroup]

    def get_queryset(self):
        barcode = self.request.query_params.get('dossier_barcode', None)
        if barcode:
            validate_dossier_barcode(barcode)
            if not DossierTask.objects.filter(dossier=barcode).exists():
                raise ParseError('Dossier is not in any task')
            if Dossier.objects.filter(barcode=barcode).exists():
                with transaction.atomic():
                    dossier_instance = Dossier.objects.get(barcode=barcode)
                    validate_dossier_status(dossier_instance, DOSSIER_REQUEST_EXECUTION_AVAILABLE_STATUSES)
                    dossier_instance.status = 'Accepted in requests'
                    sector = Sector.objects.get(name='Запросы')
                    dossier_instance.current_sector = sector
                    dossier_instance.save()
                    registry_accepting(dossier_instance, 'lr')
        return DossierTask.objects.filter(dossier=barcode, task_status__in=('accepted', 'selected')
                                          ).select_related('request')
