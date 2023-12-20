from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated

from common.pagination import CustomPagination
from common.views.mixins import ExtendedGenericViewSet
from orders.models import DossierOrder
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
    queryset = DossierOrder.objects.all()
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
    permission_classes = [IsAuthenticated]
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

    def get_queryset(self):
        user = self.request.user
        return DossierOrder.objects.filter(creator=user).prefetch_related('dossiers')

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page'] = self.request.query_params.get('page', 1)
        return response
