from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins

from archive.views.mixins import ExtendedGenericViewSet
from orders.models import DossierOrder
from orders.permissions import IsInOrdersGroup
from orders.serializers import orders


@extend_schema_view(
    list=extend_schema(summary='Orders list', tags=['Orders']),
    create=extend_schema(summary='Create order', tags=['Orders']),
    partial_update=extend_schema(summary='Update order', tags=['Orders']),
    retrieve=extend_schema(summary='Order detail', tags=['Orders']),
)
class OrderView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                ExtendedGenericViewSet):
    queryset = DossierOrder.objects.all().prefetch_related('dossiers')
    serializer_class = orders.OrderListSerializer
    multi_serializer_class = {
        'list': orders.OrderListSerializer,
        'retrieve': orders.OrderRetrieveSerializer,
        'create': orders.OrderCreateSerializer,
        'partial_update': orders.OrderUpdateSerializer,
    }
    http_method_names = ('get', 'post', 'patch')
    permission_classes = [IsInOrdersGroup]
