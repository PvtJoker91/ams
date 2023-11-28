from bank_clients.models import Client, Product, Contract
from bank_clients.serializers import ContractSerializer, ClientSerializer, ProductSerializer


class OrderClientSerializer(ClientSerializer):
    class Meta:
        model = Client
        fields = 'last_name', 'name', 'middle_name', 'passport', 'birthday'


class OrderProductSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = 'id',


class OrdersContractSerializer(ContractSerializer):
    client = OrderClientSerializer()
    product = OrderProductSerializer()

    class Meta:
        model = Contract
        fields = 'contract_number', 'product', 'client'
