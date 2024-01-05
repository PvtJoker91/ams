import re

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters, status
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from archive.models import Registry, Dossier
from common.pagination import CustomPagination
from common.services.statuses import DOSSIER_REQUEST_EXECUTION_AVAILABLE_STATUSES
from common.services.validators import validate_dossier_barcode
from common.views.mixins import ExtendedGenericViewSet
from orders.models import DossierTask
from orders.permissions import IsInOrdersGroup
from orders.serializers import tasks


@extend_schema_view(
    list=extend_schema(summary='Tasks list', tags=['Tasks']),
    create=extend_schema(summary='Create multiple tasks', tags=['Tasks']),
    partial_update=extend_schema(summary='Update task', tags=['Tasks']),
    retrieve=extend_schema(summary='Task detail', tags=['Tasks']),
    destroy=extend_schema(summary='Delete task', tags=['Tasks']),
)
class TaskView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               ExtendedGenericViewSet):
    queryset = DossierTask.objects.all()
    serializer_class = tasks.TaskListSerializer
    multi_serializer_class = {
        'list': tasks.TaskListSerializer,
        'retrieve': tasks.TaskRetrieveSerializer,
        'create': tasks.TaskCreateSerializer,
        'partial_update': tasks.TaskUpdateSerializer,
        'destroy': tasks.TaskDestroySerializer,
    }
    pagination_class = CustomPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsInOrdersGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'dossier__barcode'
    ]
    ordering_fields = [

    ]
    ordering = ['order__urgency']

    def list(self, request, *args, **kwargs):
        barcode = request.query_params.get('dossier__barcode', None)
        if barcode:
            if not validate_dossier_barcode(barcode):
                raise ParseError(f'Wrong barcode format')
            if Dossier.objects.filter(barcode=barcode).exists():
                dossier_instance = Dossier.objects.get(barcode=barcode)
            if dossier_instance.status not in DOSSIER_REQUEST_EXECUTION_AVAILABLE_STATUSES:
                raise ParseError(
                    f"Dossier should not be on this operation. Dossier current status is {dossier_instance.status}")
            dossier_instance.status = 'Accepted in requests'
            registries = Registry.objects.filter(dossiers=dossier_instance, type='lr')
            if registries.exists():
                registry = registries.first()
                if registry.status == 'sent':
                    registry.status = 'on_acceptance'
                    registry.save()
                registry.checked_dossiers.add(dossier_instance)
                if list(registry.dossiers.values()) == list(registry.checked_dossiers.values()):
                    registry.status = 'accepted'
                    registry.save()
        return super().list(request, *args, **kwargs)


    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response

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


@extend_schema_view(
    put=extend_schema(summary='Update multiple tasks', tags=['Tasks']),
)
class TaskListUpdateView(APIView):
    permission_classes = [IsInOrdersGroup]
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
