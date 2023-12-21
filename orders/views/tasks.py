from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters

from common.pagination import CustomPagination
from common.views.mixins import ExtendedGenericViewSet
from orders.models import DossierTask
from orders.permissions import IsInOrdersGroup
from orders.serializers import tasks


@extend_schema_view(
    list=extend_schema(summary='Tasks list', tags=['Tasks']),
    create=extend_schema(summary='Create task', tags=['Tasks']),
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

    ]
    ordering_fields = [

    ]
    ordering = ['order__urgency']

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response
