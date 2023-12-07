from rest_framework import serializers

from orders.models import DossierOrder


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
