from rest_framework import serializers

from bank_clients.serializers import ContractSerializer
from common_archive.models import Dossier
from common_archive.serializers import DossierSerializer
from orders.models import DossierOrder


class DossierSearchSerializer(DossierSerializer):
    contract = ContractSerializer()

    class Meta:
        model = Dossier
        fields = ('barcode', 'contract')


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        exclude = 'dossiers',


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'
