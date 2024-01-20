from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters
from rest_framework.generics import get_object_or_404

from common.pagination import CustomPagination
from common.views.mixins import ExtendedGenericViewSet
from dossier_requests.models import DossierRequest, DossierTask
from dossier_requests.permissions import IsInRequestsGroup
from dossier_requests.serializers import requests


@extend_schema_view(
    list=extend_schema(summary='Requests list', tags=['Requests']),
    create=extend_schema(summary='Create request', tags=['Requests']),
    partial_update=extend_schema(summary='Update request', tags=['Requests']),
    retrieve=extend_schema(summary='Request detail', tags=['Requests']),
    destroy=extend_schema(summary='Delete request', tags=['Requests']),
)
class RequestView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  ExtendedGenericViewSet):
    queryset = DossierRequest.objects.all()
    serializer_class = requests.RequestListSerializer
    multi_serializer_class = {
        'list': requests.RequestListSerializer,
        'retrieve': requests.RequestRetrieveSerializer,
        'create': requests.RequestCreateSerializer,
        'partial_update': requests.RequestUpdateSerializer,
        'destroy': requests.RequestDestroySerializer,
    }
    pagination_class = CustomPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsInRequestsGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status',
        'client_department',
        'service',
        'urgency',
        'time_create',
        'time_close',
    ]
    ordering_fields = [
        'status',
        'urgency',
        'time_create',
        'time_close',
    ]
    ordering = ['urgency']

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response

    def get_queryset(self):
        return DossierRequest.objects.all().exclude(status='creation').prefetch_related('dossiers')

    def get_object(self):
        """ Для получения объекта используем нефильтрованный Queryset"""

        queryset = DossierRequest.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        status = request.data.get('status', None)
        if status == 'cancelled':
            request_id = self.kwargs.get('pk')
            closer = request.data.get('closer', None)
            close_reason = request.data.get('close_reason', None)
            DossierTask.objects.filter(request=request_id).update(task_status=status,
                                                                  executor=closer,
                                                                  commentary=close_reason)
        return super().update(request, *args, **kwargs)


@extend_schema_view(list=extend_schema(summary='My requests', tags=['Requests']))
class MyRequestsView(mixins.ListModelMixin,
                     ExtendedGenericViewSet):
    queryset = DossierRequest.objects.all()
    serializer_class = requests.RequestListSerializer
    http_method_names = ('get',)
    pagination_class = CustomPagination
    permission_classes = [IsInRequestsGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status',
        'client_department',
        'service',
        'urgency',
        'time_create',
        'time_close',
    ]
    ordering_fields = [
        'status',
        'urgency',
        'time_create',
        'time_close',
    ]
    ordering = ['-time_create', '-urgency']

    def get_queryset(self):
        user = self.request.user
        return DossierRequest.objects.filter(creator=user).prefetch_related('dossiers')

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response
