from rest_framework import serializers

from orders.models import DossierOrder
from orders.serializers.nested import UserOrderSerializer


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
    creator = UserOrderSerializer()

    class Meta:
        model = DossierOrder
        fields = '__all__'


class OrderDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DossierOrder
        fields = '__all__'
