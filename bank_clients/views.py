from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import filters, mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from bank_clients.models import Contract
from bank_clients.serializers import ContractSerializer


@extend_schema_view(list=extend_schema(summary='Contracts search', tags=['Search']), )
class ContractSearchView(mixins.ListModelMixin, GenericViewSet):
    queryset = Contract.objects.all().select_related('product').select_related('client')
    serializer_class = ContractSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport',
                        'contract_number']
    search_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport',
                     'contract_number']
