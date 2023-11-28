from bank_clients.serializers import ContractSerializer, ClientSerializer, ProductSerializer


class OrderClientSerializer(ClientSerializer):
    class Meta:
        fields = 'last_name', 'name', 'middle_name', 'passport', 'birthday'


class OrderProductSerializer(ProductSerializer):
    class Meta:
        fields = 'id',


class OrdersContractSerializer(ContractSerializer):
    client = OrderClientSerializer()
    product = OrderProductSerializer()

    class Meta:
        fields = 'contract_number', 'product', 'client'
