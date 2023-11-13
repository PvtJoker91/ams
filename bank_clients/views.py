from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet

from bank_clients.models import Contract
from bank_clients.serializers import ContractSerializer


class ContractSearchView(mixins.ListModelMixin, GenericViewSet):
    queryset = Contract.objects.all().prefetch_related('dossiers')
    serializer_class = ContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport',
                        'contract_number']
    search_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport', 'contract_number']
    ordering_fields = ['client__last_name', 'client__name', 'client__middle_name', 'client__passport',
                       'contract_number']