from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters, status
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from archive.models import Dossier, Sector
from common.pagination import CustomPagination
from common.services.registries import registry_accepting
from common.services.statuses import DOSSIER_REQUEST_EXECUTION_AVAILABLE_STATUSES
from common.services.validators import validate_dossier_barcode
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
    ordering_fields = []
    ordering = ['request__urgency']

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
            if not validate_dossier_barcode(barcode):
                raise ParseError('Wrong barcode format')
            if not DossierTask.objects.filter(dossier=barcode).exists():
                raise ParseError('Dossier is not in any task')
            if Dossier.objects.filter(barcode=barcode).exists():
                dossier_instance = Dossier.objects.get(barcode=barcode)
            if dossier_instance.status not in DOSSIER_REQUEST_EXECUTION_AVAILABLE_STATUSES:
                raise ParseError(
                    f'Dossier should not be on this operation. Dossier current status is {dossier_instance.status}')
            dossier_instance.status = 'Accepted in requests'
            sector = Sector.objects.get(name='Requests')
            dossier_instance.current_sector = sector
            dossier_instance.save()
            registry_accepting('lr', dossier_instance)
        return DossierTask.objects.filter(dossier=barcode, task_status__in=('accepted', 'selected'))


@extend_schema_view(
    put=extend_schema(summary='Update multiple tasks', tags=['Tasks']),
)
class TaskListUpdateView(APIView):
    permission_classes = [IsInRequestsGroup]
    serializer_class = tasks.TaskUpdateSerializer

    def get_object(self, id):
        try:
            return DossierTask.objects.get(id=id)
        except (DossierTask.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_ids(self, id_list):
        for id in id_list:
            try:
                DossierTask.objects.get(id=id)
            except (DossierTask.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def put(self, request, *args, **kwargs):
        data = request.data
        id_list = [i['id'] for i in data]
        self.validate_ids(id_list)
        instances = []
        for temp_dict in data:
            id = temp_dict['id']
            status = temp_dict['task_status']
            obj = self.get_object(id)
            obj.task_status = status
            obj.save()
            instances.append(obj)
        serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data)
