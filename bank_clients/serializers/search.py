from bank_clients.models import Contract
from bank_clients.serializers.nested import ClientSerializer, ContractSerializer, ProductSerializer


class ContractSearchSerializer(ContractSerializer):
    product = ProductSerializer()
    client = ClientSerializer()

    class Meta:
        model = Contract
        fields = 'id', 'contract_number', 'time_create', 'product', 'client'
