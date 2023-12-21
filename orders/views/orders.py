from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters
from rest_framework.generics import get_object_or_404

from common.pagination import CustomPagination
from common.views.mixins import ExtendedGenericViewSet
from orders.models import DossiersOrder
from orders.permissions import IsInOrdersGroup
from orders.serializers import orders


@extend_schema_view(
    list=extend_schema(summary='Orders list', tags=['Orders']),
    create=extend_schema(summary='Create order', tags=['Orders']),
    partial_update=extend_schema(summary='Update order', tags=['Orders']),
    retrieve=extend_schema(summary='Order detail', tags=['Orders']),
    destroy=extend_schema(summary='Delete order', tags=['Orders']),
)
class OrderView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                ExtendedGenericViewSet):
    queryset = DossiersOrder.objects.all()
    serializer_class = orders.OrderListSerializer
    multi_serializer_class = {
        'list': orders.OrderListSerializer,
        'retrieve': orders.OrderRetrieveSerializer,
        'create': orders.OrderCreateSerializer,
        'partial_update': orders.OrderUpdateSerializer,
        'destroy': orders.OrderDestroySerializer,
    }
    pagination_class = CustomPagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsInOrdersGroup]
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
        return DossiersOrder.objects.all().exclude(status='creation').prefetch_related('dossiers')

    def get_object(self):
        queryset = DossiersOrder.objects.all()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj



@extend_schema_view(list=extend_schema(summary='My orders', tags=['Orders']))
class MyOrdersView(mixins.ListModelMixin,
                   ExtendedGenericViewSet):
    queryset = DossiersOrder.objects.all()
    serializer_class = orders.OrderListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsInOrdersGroup]
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

    def get_queryset(self):
        user = self.request.user
        return DossiersOrder.objects.filter(creator=user).prefetch_related('dossiers')

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response
