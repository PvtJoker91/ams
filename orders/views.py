from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from common_archive.models import Dossier
from common_archive.views.mixins import ExtendedGenericViewSet
from orders import serializers
from orders.models import DossierOrder
from orders.serializers import DossierSearchSerializer


@extend_schema_view(
    list=extend_schema(summary='Dossiers list', tags=['Orders']),
    retrieve=extend_schema(summary='Dossier detail', tags=['Orders']),
                    )
class DossierSearchView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    queryset = Dossier.objects.all().select_related('contract')
    serializer_class = DossierSearchSerializer
    permission_classes = [AllowAny]
    http_method_names = ('get',)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__last_name',
        'contract__client__name',
        'contract__client__middle_name',
        'contract__client__passport',
        'contract__client__birthday',
        'contract__product__name',

    ]
    search_fields = [
        'barcode',
        'contract__contract_number',
        'contract__client__passport',
    ]


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
    serializer_class = serializers.OrderListSerializer
    multi_serializer_class = {
        'list': serializers.OrderListSerializer,
        'retrieve': serializers.OrderRetrieveSerializer,
        'create': serializers.OrderCreateSerializer,
        'partial_update': serializers.OrderUpdateSerializer,
    }
    http_method_names = ('get', 'post', 'patch')
    permission_classes = [AllowAny]
