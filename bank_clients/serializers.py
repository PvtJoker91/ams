from rest_framework.serializers import ModelSerializer

from bank_clients.models import Contract, Client, Product


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ContractSerializer(ModelSerializer):
    client = ClientSerializer()
    product = ProductSerializer()

    class Meta:
        model = Contract
        fields = '__all__'
