from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from bank_clients.models import Contract
from bank_clients.serializers.search import ContractSearchSerializer
from common.filters import CustomFilter


@extend_schema_view(list=extend_schema(summary='Contracts search', tags=['Clients']), )
class ContractView(mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, CustomFilter]
    filterset_fields = ['client__last_name',
                        'client__first_name',
                        'client__middle_name',
                        'client__passport',
                        'contract_number']
    search_fields = ['client__last_name',
                     'client__first_name',
                     'client__middle_name',
                     'client__passport',
                     'contract_number']

    def get_queryset(self):
        return Contract.objects.all().select_related('product', 'client')
